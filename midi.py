from datetime import datetime

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
        note = row['note']
        volume = row['velocity']
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


  if __name__ == '__main__':
    csvdata = pd.read_csv('data/Sub1/28062021.CSV', names=Utils.header_names)
    main_playmidi(pd.DataFrame(csvdata[10:400]))
