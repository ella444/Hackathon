import pathlib
import subprocess

import pandas as pd

from QDG import QDG
from gui import gui_window, draw_graph
from utils import Utils
from zoom import zoom_args

user_args = {}
midi_exe = 'midi_temp.py'

def run_gui():
    window, ax, canvas = gui_window()
    i = 0
    while True:  # Event Loop
        event, values = window.Read(timeout=30)

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
            df = Utils.get_plot_data(selected_file)
            # divide into sessions
            sessions_df = Utils.get_sessions(df)
            user_args['sessions_df'] = {sess.time[0]: sess for sess in sessions_df}
            window.find_element("session").update(disabled=False)
            window.find_element("session").update(values=[sess_time for sess_time in user_args['sessions_df']])
        if event == 'session':
            chosen_session = user_args['sessions_df'][values[event]]
            user_args['chosen_session'] = chosen_session
            draw_graph(canvas, ax, chosen_session)
            window.find_element("play").update(disabled=False)
            # get_stats for df
            stats = QDG(chosen_session)
            window.find_element("stats").update(stats.to_string())

        if event == 'play':
            if window.find_element("play").ButtonText == 'Stop':
                user_args['midi_pay_pid'].kill()
                window.find_element("play").update('Play')
            else:
                try:
                    user_args['midi_pay_pid'] = subprocess.Popen(f'python {midi_exe}'.split())
                except:
                    user_args['midi_pay_pid'] = subprocess.Popen(f'python3 {midi_exe}'.split())
                window.find_element("play").update('Stop')

        if zoom_args.get('zoom_event'):
            zoom_args['zoom_event'] = False
            xmin, xmax = zoom_args.get('axis', [0, user_args['chosen_session'].shape[0]])
            stats = QDG(pd.DataFrame(user_args['chosen_session'][max(0, xmin):min(xmax, user_args['chosen_session'].shape[0])]))
            window.find_element("stats").update(stats.to_string())

    window.Close()


if __name__ == '__main__':
    run_gui()

