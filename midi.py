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

    # volume (0 to 1.0)
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

''''''

def csv_to_midi(csvdata):

    csvdata, headers = Utils.df_convert_time(csvdata)
    csvdata['timestamp'] = csvdata[['datetime']].apply(lambda x: x[0].timestamp(), axis=1)

    notes_data = pd.DataFrame(np.zeros(shape=[96,3]), index=[np.arange(1,97)], columns=['starttime','duration','velocity'])

    track = 0
    channel = 0
    time = 0
    tempo = 60  # In BPM -  use 60 so that time is just in seconds

    mymidi = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # automatically)
    mymidi.addTempo(track, time, tempo)

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
                volume = int(notes_data.loc[note,'velocity'])
                starttime = float(notes_data.loc[note,'starttime'])
                duration = float(notes_data.loc[note,'duration'])
                mymidi.addNote(track, channel, note, starttime, duration, volume)
                notes_data.loc[note,:] = np.zeros(shape=(1,3))
    
    return mymidi
''''''

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