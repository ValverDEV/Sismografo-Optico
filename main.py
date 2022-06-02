import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np
from read import read_serial
from scipy.optimize import curve_fit

senses = {
    0: 'Alta',
    1: 'Media',
    2: 'Baja'
}

grads = {
    0: [5*i for i in range(6)],
    1: [3*i for i in range(6)],
    2: [1*i for i in range(6)]
}

sense = 0


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def func(x, a, f):
    return a * np.sin((x/(2*f))*2*np.pi)


def process_data(packet):
    t0, tf, goTimes, backTimes = packet.split('/')
    t0 = int(t0)/1000
    tf = int(tf)/1000
    goTimes = goTimes.split(',')[:-1]
    backTimes = backTimes.split(',')[:-1]
    goTimes = [int(i)/1000 for i in goTimes]
    backTimes = [int(i)/1000 for i in backTimes]
    x = []
    y = []
    for i in range(len(goTimes)):
        if goTimes[i]:
            y.append(grads[sense][i])
            x.append(goTimes[i])
    for i in range(len(goTimes)):
        if backTimes[i]:
            y.append(grads[sense][i])
            x.append(backTimes[i])

    # x = [t - t0 for t in x]
    x = np.array(x)
    y = np.array(y)

    freq = tf - t0

    return x, y, freq, t0, tf


def clear_graph():
    global X, Y, X_scatter, Y_scatter
    X = np.zeros(0)
    Y = np.zeros(0)
    X_scatter = np.zeros(0)
    Y_scatter = np.zeros(0)
    ax.cla()
    ax.grid()
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Amplitud (°)')
    fig_agg.draw()


layout = [
    [sg.Canvas(size=(640, 480), key='-CANVAS-')],
    [sg.Text(f'Sensibilidad: {senses[sense]}', key='-SENSE-')],
    [sg.Button('Alta', disabled=True, key='-HIGH-'),
     sg.Button('Media', key='-MID-'), sg.Button('Baja', key='-LOW-')],
    [sg.Text('Amplitud: '), sg.Text('', key='-AMP-')],
    [sg.Button('Pausa', key='-PAUSE-')],
    [sg.Button('Limpiar'), sg.Button('Salir')]
]

window = sg.Window('Sismografo', layout, finalize=True)

canvas_elem = window['-CANVAS-']
canvas = canvas_elem.TKCanvas

fig = Figure()
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Amplitud (°)')
fig_agg = draw_figure(canvas, fig)
# i = 0

X = np.zeros(0)
Y = np.zeros(0)
X_scatter = np.zeros(0)
Y_scatter = np.zeros(0)


pause = False


while True:

    event, values = window.read(timeout=1000)
    if event in ('Salir', None):
        exit()

    if event == '-HIGH-':
        sense = 0
        window['-HIGH-'].Update(disabled=True)
        window['-MID-'].Update(disabled=False)
        window['-LOW-'].Update(disabled=False)
        window['-SENSE-'].Update(f'Sensibilidad: {senses[sense]}')

    if event == '-MID-':
        sense = 1
        window['-HIGH-'].Update(disabled=False)
        window['-MID-'].Update(disabled=True)
        window['-LOW-'].Update(disabled=False)
        window['-SENSE-'].Update(f'Sensibilidad: {senses[sense]}')

    if event == '-LOW-':
        sense = 2
        window['-HIGH-'].Update(disabled=False)
        window['-MID-'].Update(disabled=False)
        window['-LOW-'].Update(disabled=True)
        window['-SENSE-'].Update(f'Sensibilidad: {senses[sense]}')

    if event == 'Limpiar':
        clear_graph()

    if event == '-PAUSE-':
        if pause:
            pause = False
            window['-PAUSE-'].Update('Pausar')
        else:
            pause = True
            window['-PAUSE-'].Update('Resumir')

    data = read_serial()
    if data and not pause:
        ax.cla()
        ax.grid()
        x, y, freq, t0, tf = process_data(data)
        amp, f_approx = curve_fit(func, x, y, p0=[1, freq])[0]
        x_int = np.linspace(t0, tf, 100)
        X = np.append(X, x_int)
        Y = np.append(Y, func(x_int, amp, f_approx))
        X_scatter = np.append(X_scatter, x)
        Y_scatter = np.append(Y_scatter, y)
        ax.plot(X, Y)
        ax.scatter(X_scatter, Y_scatter, color='r')
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Amplitud (°)')
        fig_agg.draw()

        window['-AMP-'].Update(round(amp, 3))
        # i += 1

windows.close()
