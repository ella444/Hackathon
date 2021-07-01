import os.path
import pathlib
import subprocess
from multiprocessing import Process

import pandas as pd

from midi import main_playmidi
from qdg import QDG
from gui import gui_window, draw_graph
from utils import Utils
from zoom import zoom_args

user_args = {}
midi_exe = 'midi_temp.py'

def run_gui():
    '''
    main loop - handling all GUI events and behavior
    :return:
    '''
    window, ax, canvas = gui_window()
    i = 0
    while True:  # Event Loop
        event, values = window.Read(timeout=20)

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
            window.find_element("export").update(disabled=False)
            # get_stats for df
            stats = QDG(chosen_session)
            window.find_element("stats").update(stats.to_string())
        if event == 'play':
            if window.find_element("play").ButtonText == 'Stop':
                user_args['midi_pay_pid'].terminate()
                window.find_element("play").update('Play')
            else:
                df = get_chosen_data()
                user_args['midi_pay_pid'] = Process(target=main_playmidi, args=(df,))
                user_args['midi_pay_pid'].start()
                window.find_element("play").update('Stop')

        if event == 'export':
            df = get_chosen_data()
            if not os.path.isdir('sessions'):
                os.mkdir('sessions')
            i = 0
            while True:
                out_path = f'sessions/session_{i}.csv'
                if os.path.exists(out_path):
                    i += 1
                    continue
                break
            with open(out_path, 'w') as outfile:
                outfile.write(df.reset_index().to_csv(index=False))

        if zoom_args.get('zoom_event'):
            zoom_args['zoom_event'] = False
            df = get_chosen_data()
            stats = QDG(df)
            window.find_element("stats").update(stats.to_string())

    window.Close()


def get_chosen_data():
    '''
    get a slice of the loaded dataframe according to the selected view
    :return: selected slice of dataframe
    '''
    xmin, xmax = zoom_args.get('axis', [0, user_args['chosen_session'].shape[0]])
    df = pd.DataFrame(user_args['chosen_session'][max(0, xmin):min(xmax, user_args['chosen_session'].shape[0])])
    return df


if __name__ == '__main__':
    run_gui()

