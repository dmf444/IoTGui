import datetime
from time import sleep

from gevent.socket import create_connection
from packety.client import SimpleClient
from backend.switches import rs_packets
import pytz


# example
#
# a = SimpleClient(create_connection(("192.168.1.", 14441)))
# a.send(rs_packets.Authenticate(key=rs_packets.VALID_KEYS[0]))
# b = a.read()
# a.send(rs_packets.SwitchStateRequest(switch_number=1));
# b = a.read()
# b.switch_state
#
# a.send(rs_packets.SetSwitchState(switch_number=1,switch_state=True))
# a.send(rs_packets.SwitchStateRequest(switch_number=1))
# b = a.read()
# b.switch_state

class UnableToAuthenticateError(Exception):
    pass


class RemoteRelay():

    def __init__(self, connection, key):
        self._connection = SimpleClient(create_connection((connection, 14441)))
        self.authenticate() # auth once
        self._secret = key

    def get_today_password(self):
        secrets = ["THEBEGINING", "bEt@", "gaMM@", "d3LtA", "EPSILON", "ZeyT@", "eVa", "TheYt@", "IoT@", "K@77A", "LAMBDA", "Mu", "Nu", "xI", "OMNICRON", "3.14", "Rh0", "+.+.+", "T2U", "YOU-up-silon?", "DEATH", "l1fe", "Tr1d3nt", "THEENDING"]
        d = datetime.datetime.now(pytz.timezone("America/Toronto"))
        day = d.day
        return str(day + 444) + secrets[day % len(secrets)] # i will change this in the future... for now though

    def check_auth_type(self, d):
        if type(d) == rs_packets.AuthenticationResult:
            if not d.auth_ok:
                self.authenticate()
                return False
            return d
        else:
            return d

    def authenticate(self):
        self._connection.send(rs_packets.Authenticate(key=self.get_today_password()))
        response = self._connection.read()
        is_ok = response.auth_ok
        if not is_ok:
            raise UnableToAuthenticateError()

    def get_state(self, switch):
        try:
            self._connection.send(rs_packets.SwitchStateRequest(switch_number=switch))
            state = self.check_auth_type(self._connection.read())
            if not state:
                self._connection.send(
                    rs_packets.SwitchStateRequest(switch_number=switch))
                state = self._connection.read()
            return state.switch_state
        except UnableToAuthenticateError:
            return -1

    def set_state(self, switch: int, state: bool):
        try:
            self._connection.send(rs_packets.SetSwitchState(switch_number=switch,switch_state=state))
            state = self.check_auth_type(self._connection.read())
            if not state:
                self._connection.send(rs_packets.SetSwitchState(switch_number=switch,switch_state=state))
        except UnableToAuthenticateError:
            pass

    def turn_on(self, switch: int):
        self.set_state(switch, True)

    def turn_off(self, switch: int):
        self.set_state(switch, False)

    def toggle(self, switch: int):
        curr = self.get_state(switch)
        if isinstance(curr, bool):
            self.set_state(switch, not curr)

    def short_pulse(self, switch: int):
        self.set_state(switch, True)
        sleep(1)
        self.set_state(switch, False)



if(__name__ == "__main__"):
    relay = RemoteRelay("192.168.1.179", rs_packets.VALID_KEYS[0])
    # print(relay.get_state(8))
    relay.short_pulse(8)
    relay.short_pulse(7)
