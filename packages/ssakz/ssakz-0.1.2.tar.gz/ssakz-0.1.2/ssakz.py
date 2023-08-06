import zmq
import json

SERVER_PUBLIC_KEY = b"82M+$O0^qkJRj8/nWi[cma-4916*miCcALuf2-&e"


class ssaError(Exception):
    pass


def ssa_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except zmq.error.ZMQError:
            raise ConnectionError("Failed to connect to SSA server")
    return wrapper


class Client(object):
    def __init__(self, api_key):
        self.client_public_key = api_key[:40].encode('ascii')
        self.client_secret_key = api_key[40:].encode('ascii')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.curve_secretkey = self.client_secret_key
        self.socket.curve_publickey = self.client_public_key
        self.socket.curve_serverkey = SERVER_PUBLIC_KEY
        try:
            self.socket.connect("tcp://ssa.fai.kz:5555")
        except zmq.error.ZMQError:
            raise ConnectionError("Cannot connect to SSA server")

    def __del__(self):
        self.socket.close()
        self.context.term()

    @ssa_error
    def get_nme(self, rlow=None, rhigh=None, since=None, until=None, id=None, id2=None, name=None, name2=None):
        request = {
            "type": "nme",
            "filter": {
                "rlow": rlow,
                "rhigh": rhigh,
                "since": since,
                "until": until,
                "id": id,
                "id2": id2,
                "name": name,
                "name2": name2
            }
        }
        self.socket.send_string(json.dumps(request))
        return json.loads(self.socket.recv_string())
    
    @ssa_error
    def get_sw_solar(self, since, until=None, rate=None):
        request = {
            "type": "sw_solar",
            "filter": {
                "since": since,
                "until": until,
                "rate": rate
            }
        }
        self.socket.send_string(json.dumps(request))
        return json.loads(self.socket.recv_string())

    @ssa_error
    def get_sw_neutrons(self, since, until=None, rate=None):
        request = {
            "type": "sw_neutrons",
            "filter": {
                "since": since,
                "until": until,
                "rate": rate
            }
        }
        self.socket.send_string(json.dumps(request))
        return json.loads(self.socket.recv_string())

    @ssa_error
    def get_sw_geomag(self, since, until=None, rate=None):
        request = {
            "type": "sw_geomag",
            "filter": {
                "since": since,
                "until": until,
                "rate": rate
            }
        }
        self.socket.send_string(json.dumps(request))
        return json.loads(self.socket.recv_string())

    @ssa_error
    def get_sw_geomag_x(self, since, until=None, rate=None):
        request = {
            "type": "sw_geomag_x",
            "filter": {
                "since": since,
                "until": until,
                "rate": rate
            }
        }
        self.socket.send_string(json.dumps(request))
        return json.loads(self.socket.recv_string())

    @ssa_error
    def get_sw_geomag_y(self, since, until=None, rate=None):
        request = {
            "type": "sw_geomag_y",
            "filter": {
                "since": since,
                "until": until,
                "rate": rate
            }
        }
        self.socket.send_string(json.dumps(request))
        return json.loads(self.socket.recv_string())

    @ssa_error
    def get_sw_geomag_z(self, since, until=None, rate=None):
        request = {
            "type": "sw_geomag_z",
            "filter": {
                "since": since,
                "until": until,
                "rate": rate
            }
        }
        self.socket.send_string(json.dumps(request))
        return json.loads(self.socket.recv_string())

    @ssa_error
    def get_sw_k_index(self, since, until=None, rate=None):
        request = {
            "type": "sw_k_index",
            "filter": {
                "since": since,
                "until": until,
                "rate": rate
            }
        }
        self.socket.send_string(json.dumps(request))
        return json.loads(self.socket.recv_string())

