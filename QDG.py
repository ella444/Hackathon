import pandas as pd
import numpy as np

from utils import Utils


class QDG():
    def __init__(self, midi_sample: pd.DataFrame):
        '''
        Quantitative Digitography class.
        contains three methods to extract statistics from a given piano session.
        midi_sample: DataFrame containing midi events with the following order -
                    col 1 - date string (example:"28/05/2021")
                    col 2 - time string (example:"14:33:54.104"
                    col 3 - event type (1 - key press, 2 - key release)
                    col 4 - ignore
                    col 5 - key number
                    col 6 - press/release velocity
        '''
        assert isinstance(midi_sample, pd.DataFrame)

        self.midi_sample, self.header_names = Utils.df_convert_time(midi_sample)

    def extract_note_duration(self):
        '''
        function that calculates note duration defined as time difference between consecutive press and release events of the same key.
        note: if press event is not followed by release event, press event is ignored.
        return: note duration - dictionary with the following keys:
                    total - list of all note durations, in seconds.
                    mean - average note duration for a given segment.
                    std - standard deviation of note duration in a given segment.
                    CV - coefficient of variance as defined in the QDG paper.
        '''
        note_duration = {'total': []}
        for index, row in self.midi_sample.iterrows():
            if getattr(row, self.header_names[2]) != 1:
                continue
            row_key = getattr(row, self.header_names[4])
            press_time = getattr(row, self.header_names[6])
            counter = 0
            while True:
                counter += 1
                try:
                    next_row = self.midi_sample.iloc[index + counter, :]
                except IndexError:
                    release_time = None
                    break
                next_row_event = getattr(next_row,self.header_names[2])
                next_row_key = getattr(next_row,self.header_names[4])
                if next_row_event == 2 and next_row_key == row_key:
                    release_time = getattr(next_row,self.header_names[6])
                    break
            if release_time is None:
                print("couldn't locate corresponding release event...\nignoring press event")
                continue
            duration = release_time - press_time
            note_duration['total'].append(duration.total_seconds())
        note_duration['mean'] = np.mean(note_duration['total'])
        note_duration['std'] = np.std(note_duration['total'])
        note_duration['CV'] = note_duration['std'] / note_duration['mean']
        return note_duration

    def extract_press_velocity(self):
        '''
        function that calculates velocity of press events in a given segment.
        note: release events are ignored.
        return: press velocity - dictionary with the following keys:
                    total - list of press velocity values for all events.
                    mean - average press velocity for a given segment.
                    std - standard deviation of press velocity in a given segment.
                    CV - coefficient of variance as defined in the QDG paper.
        '''
        press_velocity = {'total':[]}
        for index, row in self.midi_sample.iterrows():
            if getattr(row,self.header_names[2]) != 1:
                continue
            press_velocity['total'].append(getattr(row,self.header_names[5]))
        press_velocity['mean'] = np.mean(press_velocity['total'])
        press_velocity['std'] = np.std(press_velocity['total'])
        press_velocity['CV'] = press_velocity['std'] / press_velocity['mean']
        return press_velocity

    def extract_press_frequency(self):
        '''
        function that calculates press frequency in a given segment.
        note: release events are ignored.
        return: events_per_second - dictionary with the following keys:
                    mean - average number of press events per second for a given segment.
                    std - standard deviation of number of press events per second in a given segment.
                    CV - coefficient of variance as defined in the QDG paper.
        '''
        events_per_second = {}
        midi_sample = self.midi_sample[self.midi_sample[self.header_names[2]] == 1]
        events_agg = midi_sample.groupby(pd.Grouper(key='datetime', freq='S')).count()
        events_per_second['mean'] = events_agg.iloc[:, 0].mean()
        events_per_second['std'] = events_agg.iloc[:, 0].std()
        events_per_second['CV'] = events_per_second['std'] / events_per_second['mean']
        return events_per_second


    def get_stats(self):
        stats = {}
        note_duration = self.extract_note_duration()
        stats['note duration'] = {}
        for name, value in note_duration.items():
            if name == 'total':
                continue
            stats['note duration'][name] = value

        press_velocity = self.extract_press_velocity()
        stats['press velocity'] = {}
        for name, value in press_velocity.items():
            if name == 'total':
                continue
            stats['press velocity'][name] = value
        press_frequency = self.extract_press_frequency()
        stats['press frequency'] = {}
        for name, value in press_frequency.items():
            stats['press frequency'][name] = value

        return stats

    def to_string(self):
        stats = self.get_stats()
        stat_str = ''
        for stat_name, stats in stats.items():
            stat_str += f'{stat_name}\n'
            for stat, val in stats.items():
                stat_str += f'\t{stat}: {val:.3f}\n'
        return stat_str

if __name__=='__main__':
    df = Utils.get_plot_data('./data/sub1/28062021.CSV')
    stats = QDG(df)
    print(stats.to_string())


