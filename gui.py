import pathlib
import PySimpleGUIQt as sg
from path_utils import PathUtils


def gui_window():
    sg.ChangeLookAndFeel('GreenTan')

    dir_names = PathUtils.get_dirs(".\data")

    frame1 =    [
        [sg.Combo(dir_names, size=(200,35), key='subject', enable_events=True),
        sg.Combo([''], size=(200, 35), key='day', disabled=True),
        sg.Combo([''], size=(200, 35), key='session', disabled=True)]
                ]


    frame2 =    [

                ]

    layout = [
        [sg.Frame('Select Session:', frame1, title_color='green')],
        [sg.Frame('', frame2, title_color='red'), ],
        [sg.Button('Button'), sg.Button('Exit')],
             ]


    window = sg.Window('Window Title',
                       font=('Helvetica', 13),
                       default_button_element_size=(100,30),
                       auto_size_buttons=False,
                       default_element_size=(200,22)
                       ).Layout(layout).Finalize()
    return window

def run_gui():
    window = gui_window()
    i = 0
    while True:  # Event Loop
        # sg.TimerStart()
        event, values = window.Read()#timeout=0)

        if event is None or event == 'Exit':
            break
        if event == 'Button':
            print(event, values)
        if event == 'subject':
            path = pathlib.PurePath(".\data", "sub")
            dir_names = PathUtils.get_dirs(path)
        # sg.TimerStop()
    window.Close()



if __name__ == '__main__':
    run_gui()