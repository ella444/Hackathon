import pathlib

from QDG import QDG
from gui import gui_window, draw_graph
from utils import Utils

user_args = {}


def run_gui():
    window, ax, canvas = gui_window()
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
            df = Utils.get_plot_data(selected_file)
            # divide into sessions
            sessions_df = Utils.get_sessions(df)
            user_args['sessions_df'] = {sess.time[0]: sess for sess in sessions_df}
            window.find_element("session").update(disabled=False)
            window.find_element("session").update(values=[sess_time for sess_time in user_args['sessions_df']])
        if event == 'session':
            chosen_session = user_args['sessions_df'][values[event]]
            draw_graph(canvas, ax, chosen_session)
            # get_stats for df
            # a = QDG(chosen_session, names)
            # note_duration = a.extract_note_duration()
            # for name, value in note_duration.items():
            #     print('note duration - {}:\n{}'.format(name, value))
            # press_velocity = a.extract_press_velocity()
            # for name, value in press_velocity.items():
            #     print('press velocity - {}:\n{}'.format(name, value))
            # press_frequency = a.extract_press_frequency()
            # for name, value in press_frequency.items():
            #     print('press frequency - {}:\n{}'.format(name, value))

        # sg.TimerStop()
    window.Close()


if __name__ == '__main__':
    run_gui()

