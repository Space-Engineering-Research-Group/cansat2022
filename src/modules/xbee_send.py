from digi.xbee.devices import XBeeDevice

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM1"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

REMOTE_NODE_ID = "REMOTE"


def send_message(data):

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        # Obtain the remote XBee device from the XBee network.
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        device.send_micropython_data(data.encode("utf8"))

    finally:
        if device is not None and device.is_open():
            device.close()

def recieve_data(data):

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        def micropython_data_callback(data_call_back = data):
            print("Data received from MicroPython >> '%s'" % data_call_back.decode("utf-8"))

        device.add_micropython_data_received_callback(micropython_data_callback)

    finally:
        if device is not None and device.is_open():
            device.close()
