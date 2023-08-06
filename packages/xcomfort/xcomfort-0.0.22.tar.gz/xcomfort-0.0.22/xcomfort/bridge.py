from unicodedata import numeric
import aiohttp
import asyncio
import string
import time
import rx
import rx.operators as ops
from enum import Enum
from .connection import SecureBridgeConnection, setup_secure_connection
from .messages import Messages
from .devices import (BridgeDevice, Light, RcTouch, Heater, Shade)


class State(Enum):
    Uninitialized = 0
    Initializing = 1
    Ready = 2
    Closing = 10

class RctMode(Enum):
    Cool = 1
    Eco = 2
    Comfort = 3

class RctState(Enum):
    NotApplicable = -1
    Idle = 0
    Auto = 1
    Active = 2

class RctModeRange:
    def __init__(self, min:float, max:float):
        self.Min = min
        self.Max = max

class CompState:
    def __init__(self, raw):
        self.raw = raw

    def __str__(self):
        return f"CompState({self.raw})"

    __repr__ = __str__

class Comp:
    def __init__(self, bridge, comp_id, comp_type, name: str, payload: dict):
        self.bridge = bridge
        self.comp_id = comp_id
        self.comp_type = comp_type
        self.name = name
        self.payload = payload

        self.state = rx.subject.BehaviorSubject(None)

    def handle_state(self, payload):
        self.state.on_next(CompState(payload))

    def __str__(self):
        return f'Comp({self.comp_id}, "{self.name}", comp_type: {self.comp_type}, payload: {self.payload})'

    __repr__ = __str__

class RoomState:
    def __init__(self, setpoint, temperature, humidity, power, mode:RctMode, state:RctState,  raw):
        self.setpoint = setpoint
        self.temperature = temperature
        self.humidity = humidity
        self.power = power
        self.mode = mode
        self.raw = raw
        self.rctstate = state

    def __str__(self):
        return f"RoomState({self.setpoint}, {self.temperature}, {self.humidity},{self.mode},{self.rctstate} {self.power})"

    __repr__ = __str__

class Room:
    def __init__(self, bridge, room_id, name: str):
        self.bridge = bridge
        self.room_id = room_id
        self.name = name
        self.state = rx.subject.BehaviorSubject(None)
        self.modesetpoints = dict()

    def handle_state(self, payload):
        print(f"Room.handle_state: {payload}")

        old_state = self.state.value

        if old_state is not None:
            old_state.raw.update(payload)
            payload = old_state.raw

        setpoint = payload.get('setpoint', None)
        temperature = payload.get('temp', None)
        humidity = payload.get('humidity', None)
        power = payload.get('power', 0.0)
        if 'currentMode' in payload:                # When handling from _SET_ALL_DATA
            mode = RctMode(payload.get('currentMode', None))
        if 'mode' in payload:                       # When handling from _SET_STATE_INFO
            mode = RctMode(payload.get('mode', None))

        # When handling from _SET_ALL_DATA, we get the setpoints for each mode/preset
        # Store these for later use
        if 'modes' in payload:
            for mode in payload["modes"]:
                self.modesetpoints[RctMode(mode["mode"])] = float(mode["value"])

        currentstate = RctState(payload.get('state', -1))

        self.state.on_next(RoomState(setpoint,temperature,humidity,power,mode,currentstate,payload))

    async def set_target_temperature(self, setpoint: float):

        # Validate that new setpoint is within allowed ranges.
        # if above/below allowed values, set to the edge value
        setpointrange = self.bridge.rctsetpointallowedvalues[RctMode(self.state.value.mode)]

        if setpointrange.Max < setpoint:
            setpoint = setpointrange.Max

        if setpoint < setpointrange.Min:
            setpoint = setpointrange.Min

        # Store new setpoint for current mode
        self.modesetpoints[self.state.value.mode.value] = setpoint

        await self.bridge.send_message(Messages.SET_HEATING_STATE, {"roomId":self.room_id,"mode":self.state.value.mode.value,"state":self.state.value.rctstate.value,"setpoint":setpoint,"confirmed":False})

    async def set_mode(self, mode:RctMode):

        #Find setpoint for the mode we are about to set, and use that
        #When transmitting heating_state message.
        newsetpoint = self.modesetpoints.get(mode)
        await self.bridge.send_message(Messages.SET_HEATING_STATE, {"roomId":self.room_id,"mode":mode.value,"state":self.state.value.rctstate.value,"setpoint":newsetpoint,"confirmed":False})

    def __str__(self):
        return f"Room({self.room_id}, \"{self.name}\")"

    __repr__ = __str__

class Bridge:
    def __init__(self, ip_address: str, authkey: str, session=None):
        self.ip_address = ip_address
        self.authkey = authkey

        if session is None:
            session = aiohttp.ClientSession()
            closeSession = True
        else:
            closeSession = False

        self._session = session
        self._closeSession = closeSession

        # Values determined from using setpoint slider in app.
        self.rctsetpointallowedvalues = dict({
            RctMode.Cool: RctModeRange(5.0,20.0),
            RctMode.Eco: RctModeRange(10.0,30.0),
            RctMode.Comfort: RctModeRange(18.0,40.0)
        })
        self._comps = {}
        self._devices = {}
        self._rooms = {}
        self.state = State.Uninitialized
        self.connection = None
        self.connection_subscription = None
        self.logger = lambda x: None

    async def run(self):
        if self.state != State.Uninitialized:
            raise Exception("Run can only be called once at a time")

        self.state = State.Initializing

        while self.state != State.Closing:
            try:
                #self.logger(f"Connecting...")
                await self._connect()
                await self.connection.pump()

            except Exception as e:
                self.logger(f"Error: {repr(e)}")
                await asyncio.sleep(5)

            if self.connection_subscription is not None:
                self.connection_subscription.dispose()

        self.state = State.Uninitialized

    async def switch_device(self, device_id, message):
        payload = {"deviceId": device_id}
        payload.update(message)
        await self.send_message(Messages.ACTION_SWITCH_DEVICE, payload)

    async def slide_device(self, device_id, message):
        payload = {"deviceId": device_id}
        payload.update(message)
        await self.send_message(Messages.ACTION_SLIDE_DEVICE, payload)

    async def send_message(self, message_type: Messages, message):
        await self.connection.send_message(message_type, message)

    def _add_comp(self, comp):
        self._comps[comp.comp_id] = comp

    def _add_device(self, device):
        self._devices[device.device_id] = device

    def _add_room(self, room):
        self._rooms[room.room_id] = room

    def _handle_SET_DEVICE_STATE(self, payload):
        try:
            device = self._devices[payload['deviceId']]

            device.handle_state(payload)
        except KeyError:
            return

    def _handle_SET_STATE_INFO(self, payload):
        for item in payload['item']:
            if 'deviceId' in item:
                deviceId = item['deviceId']
                device = self._devices[deviceId]
                device.handle_state(item)

            elif 'roomId' in item:
                roomId = item['roomId']
                room = self._rooms[roomId]
                room.handle_state(item)

            elif 'compId' in item:
                compId = item['compId']
                comp = self._comps[compId]
                comp.handle_state(item)

            else:
                self.logger(f"Unknown state info: {payload}")

    def _create_comp_from_payload(self, payload):
        comp_id = payload['compId']
        name = payload['name']
        comp_type = payload["compType"]

        return Comp(self, comp_id, comp_type, name, payload)

    def _create_device_from_payload(self, payload):
        device_id = payload['deviceId']
        name = payload['name']
        dev_type = payload["devType"]
        comp_id = payload["compId"]

        if dev_type == 100 or dev_type == 101:
            dimmable = payload['dimmable']
            return Light(self, device_id, name, dimmable)

        if dev_type == 102:
            return Shade(self, device_id, name, comp_id, payload)

        if dev_type == 440:
            return Heater(self, device_id, name, comp_id)

        if dev_type == 450:
            return RcTouch(self, device_id, name, comp_id)

        return BridgeDevice(self, device_id, name)

    def _create_room_from_payload(self, payload):
        room_id = payload['roomId']
        name = payload['name']

        return Room(self, room_id, name)

    def _handle_comp_payload(self, payload):
        comp_id = payload['compId']

        comp = self._comps.get(comp_id)

        if comp is None:
            comp = self._create_comp_from_payload(payload)

            if comp is None:
                return

            self._add_comp(comp)

        comp.handle_state(payload)

    def _handle_device_payload(self, payload):
        device_id = payload['deviceId']

        device = self._devices.get(device_id)

        if device is None:
            device = self._create_device_from_payload(payload)

            if device is None:
                return

            self._add_device(device)

        device.handle_state(payload)

    def _handle_room_payload(self, payload):
        room_id = payload['roomId']

        room = self._rooms.get(room_id)

        if room is None:
            room = self._create_room_from_payload(payload)

            if room is None:
                return

            self._add_room(room)

        room.handle_state(payload)

    def _handle_SET_ALL_DATA(self, payload):
        if 'lastItem' in payload:
            self.state = State.Ready

        if 'devices' in payload:
            for device_payload in payload['devices']:
                try:
                    self._handle_device_payload(device_payload)
                except Exception as e:
                    self.logger(f"Failed to handle device payload: {str(e)}")

        if 'comps' in payload:
            for comp_payload in payload["comps"]:
                try:
                    self._handle_comp_payload(comp_payload)
                except Exception as e:
                    self.logger(f"Failed to handle comp payload: {str(e)}")

        if 'rooms' in payload:
            for room_payload in payload["rooms"]:
                try:
                    self._handle_room_payload(room_payload)
                except Exception as e:
                    self.logger(f"Failed to handle room payload: {str(e)}")

        if 'roomHeating' in payload:
            for room_payload in payload["roomHeating"]:
                try:
                    self._handle_room_payload(room_payload)
                except Exception as e:
                    self.logger(f"Failed to handle room payload: {str(e)}")

    def _handle_UNKNOWN(self, message_type, payload):
        self.logger(f"Unhandled package [{message_type.name}]: {payload}")
        pass

    def _onMessage(self, message):

        if 'payload' in message:
            # self.logger(f"Message: {message}")
            message_type = Messages(message['type_int'])
            method_name = '_handle_' + message_type.name

            method = getattr(self, method_name,
                             lambda p: self._handle_UNKNOWN(message_type, p))
            try:
                method(message['payload'])
            except Exception as e:
                self.logger(f"Unknown error with: {method_name}: {str(e)}")
        else:
            self.logger(f"Not known: {message}")

    async def _connect(self):
        self.connection = await setup_secure_connection(self._session, self.ip_address, self.authkey)
        self.connection_subscription = self.connection.messages.subscribe(
            self._onMessage)

    async def close(self):
        self.state = State.Closing

        if isinstance(self.connection, SecureBridgeConnection):
            self.connection_subscription.dispose()
            await self.connection.close()

        if self._closeSession:
            await self._session.close()

    async def wait_for_initialization(self):
        if self.state == State.Uninitialized:
            await asyncio.sleep(0.1)

        while self.state == State.Initializing:
            await asyncio.sleep(0.1)

        return

    async def get_comps(self):
        await self.wait_for_initialization()

        return self._comps

    async def get_devices(self):
        await self.wait_for_initialization()

        return self._devices

    async def get_rooms(self):
        await self.wait_for_initialization()

        return self._rooms
