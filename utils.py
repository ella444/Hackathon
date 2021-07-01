import pathlib
import pandas as pd
from datetime import datetime

class Utils:
    header_names = ['date', 'time', 'action', 'channel', 'note', 'velocity']

    @staticmethod
    def get_dirs(path):
        p = pathlib.Path(path)
        if not p.exists():
            return []
        return [x.name for x in p.iterdir() if x.is_dir()]

    @staticmethod
    def get_files(path, suffix='.csv'):
        p = pathlib.Path(path)
        if not p.exists():
            return []
        return [x.name for x in p.iterdir() if x.is_file() and x.suffix.lower() == suffix]

    @staticmethod
    def get_sessions(df, time_const_min=30):
        '''
        split df into sessions defined by a break time of 'time_const_min'
        :param df: input data frame
        :param time_const_min: time gap in minutes between sessions
        :return:
        '''
        # split df into section by time diff
        df['timestamp'] = df.datetime.apply(lambda x: datetime.timestamp(x))
        session_end_indexes = list(df[df['timestamp'].diff() > time_const_min * 60].index) + [df.shape[0]]
        if not any(session_end_indexes):
            return [df]
        sessions = []
        prev_index = 0
        for index in session_end_indexes:
            sess = df.iloc[prev_index:index]
            prev_index = index
            sessions.append(sess.reset_index())
        return sessions

    @staticmethod
    def get_plot_data(path):
        '''
        reaf csv to dataframe and create a datetime column
        :param path: path to csv file
        :return: DataFrame with datetime column
        '''
        midi_sample = pd.read_csv(path, names=list(Utils.header_names))
        midi_sample_with_datetime, _ = Utils.df_convert_time(midi_sample)
        return midi_sample_with_datetime

    @staticmethod
    def df_convert_time(midi_sample):
        '''
        create a datetime column and add to csv
        :param midi_sample:
        :return:
        '''
        date_format = "%d/%m/%Y"
        time_format = "%H:%M:%S.%f"
        datetime_format = date_format + ' ' + time_format
        header_names = Utils.header_names
        midi_sample['datetime'] = midi_sample[header_names[0]] + ' ' + midi_sample[header_names[1]]
        midi_sample['datetime'] = pd.to_datetime(midi_sample['datetime'], format=datetime_format)
        if 'datetime' not in header_names:
            header_names.append('datetime')
        return midi_sample, header_names


if __name__ == '__main__':
    print(Utils.get_dirs("./data"))
