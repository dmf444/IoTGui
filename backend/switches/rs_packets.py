# remote_switch packets

from packety.packets import Packet
from packety.packets.schema import String, Boolean, UnsignedByte
from packety.packets.validate import IsOneOf, Smaller, InRange

VALID_KEYS = [
    "\x0b\x8c\x95\xb3(&n\",)\xc2\x8d\xaeZ=\\B\xea\xd6\x893\x8f+\xc0?j\xe1\x92_\xfe;\xe0"
]  # each client gets its own


class Authenticate(Packet):
    packet_id = 1
    key = String()


class AuthenticationResult(Packet):
    packet_id = 2
    auth_ok = Boolean()


class SetSwitchState(Packet):
    packet_id = 3

    switch_number = UnsignedByte(validators=[InRange(1, 9)])
    switch_state = Boolean()


class SwitchStateRequest(Packet):
    packet_id = 4

    switch_number = UnsignedByte(validators=[InRange(1, 9)])


class SwitchStateResponse(Packet):
    packet_id = 5

    switch_state = Boolean()


class Ok(Packet):
    packet_id = 6

    ok = Boolean()
    error = String()


Authenticate.register()
AuthenticationResult.register()
SetSwitchState.register()
SwitchStateRequest.register()
SwitchStateResponse.register()
Ok.register()
