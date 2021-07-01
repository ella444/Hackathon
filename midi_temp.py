import pygame
# import py_midicsv as pm
import pandas as pd
# from midiutil.MidiFile import MIDIFile
import json


def main_playmidi(csv_midi: pd.DataFrame):
    midi_file = csv_to_midi(csv_midi)

    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024  # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)

    # volume (0 to 1.0)
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
    trials = csvdata['trials']

    track = 0
    channel = 0
    time = 0
    tempo = 60  # In BPM -  use 60 so that time is just in seconds

    mymidi = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # automatically)
    mymidi.addTempo(track, time, tempo)

    for trial in trials:
        notes = trial.find("notes").text
        notesArray = json.loads(notes)
        startsongtime = notesArray[0][2]
        for m in notesArray:
            note = m[0]
            volume = m[1]
            starttime = m[2] - startsongtime
            endtime = m[3] - startsongtime
            duration = endtime - starttime
            mymidi.addNote(track, channel, note, starttime, duration, volume)

    return mymidi


''''''


def play_music(midi_file):
    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024  # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)

    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.4)

    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(midi_file)
        print("Music file %s loaded!" % midi_file)
    except pygame.error as e:
        print(e)
        print("File %s not found! (%s)" % (midi_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)


play_music('output.mid')
# play_music('FishPolka.mid')