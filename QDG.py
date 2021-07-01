import pandas as pd
import numpy as np

from utils import Utils


class QDG():
    def __init__(self, midi_sample: pd.DataFrame):
        assert isinstance(midi_sample, pd.DataFrame)

        self.midi_sample, self.header_names = Utils.df_convert_time(midi_sample)

    def extract_note_duration(self):
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
        events_per_second = {}
        midi_sample = self.midi_sample[self.midi_sample[self.header_names[2]] == 1]
        events_agg = midi_sample.groupby(pd.Grouper(key='datetime', freq='S')).count()
        events_per_second['mean'] = events_agg.iloc[:, 0].mean()
        events_per_second['std'] = events_agg.iloc[:, 0].std()
        return events_per_second


if __name__=='__main__':
    df = Utils.get_plot_data('./data/sub1/28062021.CSV')
    a = QDG(df)
    note_duration = a.extract_note_duration()
    for name,value in note_duration.items():
        print('note duration - {}:\n{}'.format(name,value))
    press_velocity = a.extract_press_velocity()
    for name, value in press_velocity.items():
        print('press velocity - {}:\n{}'.format(name, value))
    press_frequency = a.extract_press_frequency()
    for name, value in press_frequency.items():
        print('press frequency - {}:\n{}'.format(name, value))

