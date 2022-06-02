from turtle import back
import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = 'COM7'
serialInst.open()


def func(x, a, f):
    return a * np.sin((x/(2*f))*2*np.pi)


while True:
    packet = serialInst.read_until()
    packet = packet.decode('utf')
    if packet:
        break

t0, tf, goTimes, backTimes = packet.split('/')
t0 = int(t0)
tf = int(tf)
goTimes = goTimes.split(',')[:-1]
backTimes = backTimes.split(',')[:-1]
goTimes = [int(i) for i in goTimes]
backTimes = [int(i) for i in backTimes]
x = []
y = []
for i in range(len(goTimes)):
    if goTimes[i]:
        y.append(i)
        x.append(goTimes[i])
for i in range(len(goTimes)):
    if backTimes[i]:
        y.append(i)
        x.append(backTimes[i])

x = [t - t0 for t in x]
x = np.array(x)
y = np.array(y)

freq = tf - t0

amp, f_approx = curve_fit(func, x, y, p0=[1, freq])[0]

print(freq)

X = np.linspace(0, 2*freq, 100)
Y = func(X, amp, f_approx)

print(x, y)

plt.plot(X, Y)
plt.scatter(x, y, color='r')
plt.show()
