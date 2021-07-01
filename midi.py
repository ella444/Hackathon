import pygame
import pandas as pd
import numpy as np
from midiutil.MidiFile import MIDIFile
from utils import Utils


def main_playmidi(csv_midi: pd.DataFrame):

    csv_to_midi(csv_midi)
    midi_file = 'midifile.mid'
  
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


def csv_to_midi(csvdata):

    midi_data = calculate_duration(csvdata)

    track = 0
    channel = 0
    time = 0
    tempo = 60  # In BPM -  use 60 so that time is just in seconds

    mymidi = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # automatically)
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

def calculate_duration(csvdata: pd.DataFrame):
    csvdata, headers = Utils.df_convert_time(csvdata)
    csvdata['timestamp'] = csvdata[['datetime']].apply(lambda x: x[0].timestamp(), axis=1)
    notes_data = pd.DataFrame(np.zeros(shape=[88,5]), index=[np.arange(21,109)], columns=['starttime','starttime_utc','note','duration','velocity'])
    new_data = pd.DataFrame(columns=['starttime','starttime_utc','note','duration','velocity'])

    startsong = csvdata['timestamp'][0]-0.001

    for index, row in csvdata.iterrows():
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