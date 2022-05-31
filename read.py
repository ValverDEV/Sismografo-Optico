import serial

serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = 'COM7'
serialInst.open()


def read_serial():
    packet = serialInst.readline()
    packet = packet.decode('utf')
    if packet:
        return packet
    return None


# read_serial()
