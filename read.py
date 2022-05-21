import serial

serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = 'COM7'
serialInst.open()

while True:
    packet = serialInst.readline()
    packet = packet.decode('utf')
    print(packet)
