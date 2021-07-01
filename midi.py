from datetime import datetime

import pygame
import pandas as pd
import numpy as np
from midiutil.MidiFile import MIDIFile
from utils import Utils


def main_playmidi(csv_midi: pd.DataFrame):

    midi_file = csv_to_midi(csv_midi)
  
    freq = 44100  # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024   # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)


    pygame.mixer.music.set_volume(0.4)

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

''''''

def csv_to_midi(csvdata):

    csvdata, _ = Utils.df_convert_time(csvdata)
    csvdata['timestamp'] = csvdata.datetime.apply(lambda x: datetime.timestamp(x))

    notes_data = pd.DataFrame(np.zeros(shape=[96, 3]), index=np.arange(1, 97), columns=['starttime', 'duration', 'velocity'])

    track = 0
    channel = 0
    time = 0
    tempo = 60  # In BPM -  use 60 so that time is just in seconds

    mymidi = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # automatically)
    mymidi.addTempo(track, time, tempo)
    nullify = pd.DataFrame(np.zeros(shape=[1, 3]))
    startsong = csvdata['timestamp'][0]-0.001

    for index, row in csvdata.iterrows():
        note = row['note']
        if row['action'] == 1:
            if int(notes_data.loc[note,'starttime']) == 0:
                notes_data.loc[note,'starttime'] = row['timestamp']-startsong
                notes_data.loc[note,'velocity'] = row['velocity']
        elif row['action'] == 2:
            if int(notes_data.loc[note,'starttime'] != 0):
                notes_data.loc[note,'duration'] = row['timestamp']-startsong-notes_data.loc[note,'starttime']
                volume = (notes_data.loc[note,'velocity'])
                starttime = (notes_data.loc[note,'starttime'])
                duration = (notes_data.loc[note,'duration'])
                mymidi.addNote(track, channel, note, starttime, duration, volume)
                notes_data.loc[note,:] = np.zeros(shape=(1,3))
                notes_data[note] = nullify

    with open("output.mid", 'wb') as outf:
        mymidi.writeFile(outf)
    return "output.mid"
''''''
# =======
#     startsong = csvdata['timestamp'][0]
#     nullify = pd.DataFrame(np.zeros(shape=[1, 3]))
#
#     for index, row in csvdata.iterrows():
#         note = row['note']
#         if row['action'] == 1 and notes_duration.iloc[note, 0] == 0:
#             notes_duration[note, 'starttime'] = row['timestamp']-startsong
#             notes_duration[note, 'velocity'] = row['velocity']
#         elif row['action'] == 2 and notes_duration.iloc[note, 0] != 0:
#             notes_duration[note,'duration'] = row['timestamp']-startsong-notes_duration[note, 'starttime']
#             volume = notes_duration[note,'velocity']
#             starttime = notes_duration[note, 'starttime']
#             duration = notes_duration[note, 'duration']
#             mymidi.addNote(track, channel, note, starttime, duration, volume)
#             notes_duration[note] = nullify
#
#     with open("output.mid", 'wb') as outf:
#         mymidi.writeFile(outf)
#     return "output.mid"
#
# >>>>>>> Stashed changes

def play_music(midi_file):
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(midi_file)
        print ("Music file %s loaded!" % midi_file)
    except pygame.error:
        print ("File %s not found! (%s)" % (midi_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)

if __name__ == '__main__':
    csvdata = pd.read_csv('data/Sub1/28062021.CSV', names=Utils.header_names)
    main_playmidi(pd.DataFrame(csvdata[10:400]))