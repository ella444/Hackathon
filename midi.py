import pygame
import pandas as pd
import numpy as np
from midiutil.MidiFile import MIDIFile


def main_playmidi(csv_midi: pd.DataFrame):
    '''


        parameters: dataframe of the quantitive data
        output: playing the midi file
        '''
    csv_to_midi(csv_midi)
    midi_file = 'midifile.mid'

    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024  # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)

    pygame.mixer.music.set_volume(0.8)

    # listen for interruptions
    try:
        # use the midi file you just saved
        play_music(midi_file)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit


def csv_to_midi(csvdata):
    """
    converts the data from the csv file into a midi file.
    checks the time, duration and sound volume (velocity) of each note
    and generates a new midi file containing this information
        parameters: dataframe of the quantitive data
        returns: a midi file
    """

    midi_data = calculate_duration(csvdata)

    track = 0
    channel = 0
    time = 0
    tempo = 60  # In BPM -  use 60 so that time is just in seconds

    mymidi = MIDIFile(1)  # One track, defaults to format 1
    mymidi.addTempo(track, time, tempo)

    for index, row in midi_data.iterrows():
        note = int(row['note'])
        volume = int(row['velocity'])
        starttime = row['starttime_utc']
        duration = row['duration']
        mymidi.addNote(track, channel, note, starttime, duration, volume)

    with open('midifile.mid', "wb") as output_file:
        mymidi.writeFile(output_file)


def play_music(midi_file):
    '''

    except pygame.error:
        print("File %s not found! (%s)" % (midi_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)


def calculate_duration(csvdata: pd.DataFrame):
    '''
    allows the rearange the quantitive midi data;
    in the original file, there are different rows to pressing and releasing the keyboard.
    this function creates one row of data for each note played including the start time and duration.
    it also converts the start time to UTC time, which is the only way a midi file can be generated.
        parameters: dataframe with the original data
        returns: new dataframe contaning the above-mentioned data.
    '''
    csvdata, headers = Utils.df_convert_time(csvdata)
    csvdata['timestamp'] = csvdata[['datetime']].apply(lambda x: x[0].timestamp(), axis=1) # UTC time
    # dataframe to hold data of each note before the we have data of the releasing time.
    notes_data = pd.DataFrame(np.zeros(shape=[88,5]), index=[np.arange(21,109)], columns=['starttime','starttime_utc','note','duration','velocity']) 
    # dataframe to save the new data into
    new_data = pd.DataFrame(columns=['starttime','starttime_utc','note','duration','velocity'])

    startsong = csvdata['timestamp'][0]-0.001

    for index, row in csvdata.iterrows():
        # on each iteration, the loop either adds a new line to notes_data with the start time data
        # (action = 1), or calculates the duration and adds a new line to the new_data df.
        # in notes_data, the info is stored according to the note midi symbol (numbered 21 to 108)
        # so it'll be easy to recognize each note's closer.
        note = row['note']
        if row['action'] == 1:
            if int(notes_data.loc[note,'starttime_utc']) == 0:
                notes_data.loc[note,'starttime'] = row['time']
                notes_data.loc[note,'starttime_utc'] = row['timestamp']-startsong
                notes_data.loc[note,'note'] = row['note']
                notes_data.loc[note,'velocity'] = row['velocity']
        elif row['action'] == 2:
            if int(notes_data.loc[note,'starttime_utc'] != 0):
                notes_data.loc[note,'duration'] = row['timestamp']-startsong-notes_data.loc[note,'starttime_utc']
                new_line = notes_data.loc[note]
                new_data = new_data.append(new_line,ignore_index=True)
                notes_data.loc[note,:] = np.zeros(shape=(1,5))
    new_data = new_data.sort_values('starttime').reindex()
    return new_data

def calculate_duration(csvdata: pd.DataFrame):
        allows the rearange the quantitive midi data;
        in the original file, there are different rows to pressing and releasing the keyboard.
        this function creates one row of data for each note played including the start time and duration.
        it also converts the start time to UTC time, which is the only way a midi file can be generated.
            parameters: dataframe with the original data
            returns: new dataframe contaning the above-mentioned data.
        '''
    notes_data = pd.DataFrame(np.zeros(shape=[88, 5]), index=[np.arange(21, 109)],
                              columns=['starttime', 'starttime_utc', 'note', 'duration', 'velocity'])
    new_data = pd.DataFrame(columns=['starttime', 'starttime_utc', 'note', 'duration', 'velocity'])

    startsong = csvdata['timestamp'].iloc[0] - 0.001

    for index, row in csvdata.iterrows():
        note = row['note']
        if row['action'] == 1:
            if int(notes_data.loc[note, 'starttime_utc']) == 0:
                notes_data.loc[note, 'starttime'] = row['time']
                notes_data.loc[note, 'starttime_utc'] = row['timestamp'] - startsong
                notes_data.loc[note, 'note'] = row['note']
                notes_data.loc[note, 'velocity'] = row['velocity']
        elif row['action'] == 2:
            if int(notes_data.loc[note, 'starttime_utc'] != 0):
                notes_data.loc[note, 'duration'] = row['timestamp'] - startsong - notes_data.loc[note, 'starttime_utc']
                new_line = notes_data.loc[note]
                new_data = new_data.append(new_line, ignore_index=True)
                notes_data.loc[note, :] = np.zeros(shape=(1, 5))
    new_data = new_data.sort_values('starttime').reindex()
    return new_data


if __name__ == '__main__':
    csvdata = pd.read_csv('test_data/session_1.csv')
    main_playmidi(csvdata)
