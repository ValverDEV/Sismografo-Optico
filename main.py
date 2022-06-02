# Definición de librerías
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np
from read import read_serial
from scipy.optimize import curve_fit

# Variables para determinar sensibilidad

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

# Genera gráfico en interfaz gráfica

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# Función para regresión senoidal

def func(x, a, f):
    return a * np.sin((x/(2*f))*2*np.pi)

# Preocesamiento de los datos

def process_data(packet): # toma el paquete que recibe del serial
    t0, tf, goTimes, backTimes = packet.split('/') # separa por /
    t0 = int(t0)/1000 # convierte de milisegundos a segundos
    tf = int(tf)/1000
    goTimes = goTimes.split(',')[:-1] # separa valores tiempo ida y guarda en un arreglo
    backTimes = backTimes.split(',')[:-1] # lo mismo pero para regreso
    goTimes = [int(i)/1000 for i in goTimes] # convierte a segundos
    backTimes = [int(i)/1000 for i in backTimes]

    # eliminamos los 0s

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

    x = np.array(x) # arreglo de numpy para eficiencia y operaciones avanzadas
    y = np.array(y)

    freq = tf - t0 # cálculo de frecuencia del semiperiodo

    return x, y, freq, t0, tf


def clear_graph(): 
    # limpia la gráfica y los datos guardados
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


layout = [ # elementos de la interfaz gráfica
    [sg.Canvas(size=(640, 480), key='-CANVAS-')],
    [sg.Text(f'Sensibilidad: {senses[sense]}', key='-SENSE-')],
    [sg.Button('Alta', disabled=True, key='-HIGH-'),
     sg.Button('Media', key='-MID-'), sg.Button('Baja', key='-LOW-')],
    [sg.Text('Amplitud: '), sg.Text('', key='-AMP-')],
    [sg.Button('Pausa', key='-PAUSE-')],
    [sg.Button('Limpiar'), sg.Button('Salir')]
]

window = sg.Window('Sismografo', layout, finalize=True) # genera la ventana

canvas_elem = window['-CANVAS-'] # obtiene el canvas para la gráfica
canvas = canvas_elem.TKCanvas

fig = Figure() # genera la gráfica de 
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Amplitud (°)')
fig_agg = draw_figure(canvas, fig) # la dibujamos en la interfaz


# Almacen de los datos a través del tiemop
X = np.zeros(0)
Y = np.zeros(0)
X_scatter = np.zeros(0)
Y_scatter = np.zeros(0)

# Variable para saber si estamos en pausa
pause = False

# Ciclo infinito
while True:

    event, values = window.read(timeout=1000) # Lectura de eventos en la ventana
    if event in ('Salir', None): # si se presiona Salir o se cierra la ventana
        exit() #salimos

    # cambio de sensibilidad
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
        clear_graph() # limpiamos la gráfica

    if event == '-PAUSE-': # si presionamos pausa/resumir
        if pause: # si estamos en pausa
            pause = False # resumimos
            window['-PAUSE-'].Update('Pausar')
        else: # si no está pausado
            pause = True # pausamos
            window['-PAUSE-'].Update('Resumir')

    data = read_serial() # lectura de datos seriales
    if data and not pause: # si hay datos nuevos y no estamos en pausa
        ax.cla() 
        ax.grid()
        x, y, freq, t0, tf = process_data(data) # procesamos los datos
        amp, f_approx = curve_fit(func, x, y, p0=[1, freq])[0] # hacemos la regresión senoidal
        x_int = np.linspace(t0, tf, 100)
        X = np.append(X, x_int)
        Y = np.append(Y, func(x_int, amp, f_approx))
        # guardamos los datos nuevos con los anteriores
        X_scatter = np.append(X_scatter, x)
        Y_scatter = np.append(Y_scatter, y)
        # agregamos los datos nuevos a la gráfica
        ax.plot(X, Y)
        ax.scatter(X_scatter, Y_scatter, color='r')
        ax.set_xlabel('Tiempo (s)') 
        ax.set_ylabel('Amplitud (°)')
        # graficamos
        fig_agg.draw()

        # Actualizamos la amplitud aproxmimada
        window['-AMP-'].Update(round(amp, 3))
        # i += 1

windows.close() # terminamos el programa
