import pywemo

DEVICES = []
WEMO_NAME_MAP = {}


def scan_for_devices():
    global DEVICES
    DEVICES = pywemo.discover_devices()
    set_local_names()


def set_local_names():
    for device in DEVICES:
        WEMO_NAME_MAP[device.name] = device

