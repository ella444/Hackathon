import pathlib
import PySimpleGUIQt as sg
from utils import Utils

user_args = {}

def gui_window():
    sg.ChangeLookAndFeel('GreenTan')

    dir_names = Utils.get_dirs(".\data")

    frame1 =    [
        [sg.Input('Input Text', do_not_clear=True, size=(250, 35), tooltip='Input', key="main_dir",enable_events=True), sg.FolderBrowse(), sg.Stretch()],
        [sg.Combo([''], size=(200,35), key='subject', disabled=True, enable_events=True),
        sg.Combo([''], size=(200, 35), key='day', disabled=True, enable_events=True),
        sg.Combo([''], size=(200, 35), key='session', disabled=True, enable_events=True)]
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
        if event == 'main_dir':
            user_args[event] = values[event]
            dir_names = Utils.get_dirs(values[event])
            window.find_element("subject").update(disabled=False)
            window.find_element("subject").update(values=dir_names)
        if event == 'subject':
            user_args[event] = values[event]
            path = pathlib.PurePath(user_args['main_dir'], values[event])
            file_names = Utils.get_files(path)
            window.find_element("day").update(disabled=False)
            window.find_element("day").update(values=file_names)
        if event == 'day':
            user_args[event] = values[event]
            selected_file = pathlib.PurePath(user_args['main_dir'], user_args['subject'], values[event])
            sessions = Utils.get_session(selected_file)
            window.find_element("session").update(disabled=False)
            window.find_element("session").update(values=sessions)

        # sg.TimerStop()
    window.Close()


if __name__ == '__main__':
    run_gui()