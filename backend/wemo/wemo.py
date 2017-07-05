import pywemo

DEVICES = []
LOCAL_NAMES = {}


def scan_for_devices():
    global DEVICES
    DEVICES = pywemo.discover_devices()
    set_local_names()

def set_local_names():
    for device in DEVICES:
        LOCAL_NAMES[device.name] = device
