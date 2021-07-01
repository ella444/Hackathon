import matplotlib.pyplot as plt

import PySimpleGUI as sg
import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

from zoom import ZoomPan


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def gui_window():
    sg.ChangeLookAndFeel('GreenTan')

    frame1 =    [
        [sg.Input('Input Text', do_not_clear=True, size=(20, 35), tooltip='Input', key="main_dir",enable_events=True), sg.FolderBrowse()],
        [sg.Combo([''], size=(20,35), key='subject', disabled=True, enable_events=True),
        sg.Combo([''], size=(20, 35), key='day', disabled=True, enable_events=True),
        sg.Combo([''], size=(20, 35), key='session', disabled=True, enable_events=True)]
                ]

    fig = matplotlib.figure.Figure(figsize=(15, 8), dpi=100)

    ax = fig.add_subplot(111)
    # t = np.arange(0, 3, .01)
    # ax.plot(t, 2 * np.sin(2 * np.pi * t))



    frame2 =    [
        [sg.Canvas(key='-CANVAS-')]
                ]
    # stats frame
    frame3 = [
        [sg.Text('note-mean', size=(20, 20))],
        # [sg.Text('note-std', size=(20, 20))],
        # [sg.Text('note-cv', size=(20, 20))],
        # [sg.Text('press-vel-mean', size=(20, 20))],
        # [sg.Text('press-vel-std', size=(20, 20))],
        # [sg.Text('press-vel-cv', size=(20, 20))],
        # [sg.Text('press-freq-mean', size=(20, 20))],
        # [sg.Text('press-freq-std', size=(20, 20))]
    ]

    layout = [
        [sg.Frame('Select Session:', frame1, title_color='green')],
        [sg.Frame('', frame2, title_color='red'), sg.Frame('Stats:', frame3, title_color='red')],
        [sg.Button('Play', key='play', disabled=False, enable_events=True), sg.Button('Exit')],
             ]

    window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True,
                       element_justification='center', font='Helvetica 18')
    fig_canvas_agg = draw_figure(window.find_element('-CANVAS-').TKCanvas, fig)

    return window, ax, fig_canvas_agg

def draw_graph(canvas, ax, df):
    t = df.time[:100]# .apply(lambda x: x.split('.')[0])
    ax.cla()
    ax.scatter(t, df.note[:100])
    ax.set_xticks(t[0:-1:10])
    zp = ZoomPan()
    figZoom = zp.zoom_factory(ax, base_scale=1.1)
    figPan = zp.pan_factory(ax)
    canvas.draw()

