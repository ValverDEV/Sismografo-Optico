import serial
from statistics import mean

# largo partes = 7.6cm

distances = [(7.6/6)*i for i in range(7)]

serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = 'COM7'
serialInst.open()

while True:
    packet = serialInst.read_until()
    packet = packet.decode('utf')
    if packet:
        t0, tf, goTimes, backTimes = packet.split('/')
        t0 = int(t0)
        tf = int(tf)
        goTimes = goTimes.split(',')[:-1]
        backTimes = backTimes.split(',')[:-1]
        print(f't0: {t0}')
        print(f'Ida')
        for i in range(len(goTimes)):
            print(f'Sensor {i+1}: {goTimes[i]}')
        print('Regreso')
        for i in list(range(len(goTimes)))[::-1]:
            print(f'Sensor {i+1}: {backTimes[i]}')
        print(f'tf: {tf}')
