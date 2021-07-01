# Hackathon

The research:
The research this project was created for is taking place in Dr Jason Friedman's Lab. The aim of this research is to determine wethear musical practice on the piano helps to improve motor symptoms in PD patients. The patients will go through 6 weeks of piano practice (guided and unguided), as well as some examinations to test their motor abilities. the examinations will take place at the begining and the end of the 6-week session, except one (QDG) that will be preformed weekly.
during this time the patients will have a keyboard at home, connected to an arduino device that will record their playing and store it as csv files of midi data. there will be a new file each day.

The project:
The aim of this project was to provide a tool to read and analyze the data from the piano, including divide  several playing sessions that were held in the same day, show statistical measures for the QDG test and play a chosen part, all this in an accesible gui.

Project components:
- Notes diaplay: allows dinamic display of the playing data (bars representing time and duration of each note that was played), that can be zoomed in and out. in the chosen range, it's possible to export a csv file of the specific data and statistical analysis.
- Statistical analysis: calculates 3 importent measures of the QDG test: note duration, press velocity (intensity, how strong was the keybord pressed) and frequency (taps per minute).
- playing: converts the data back to midi and allows to play a chosen part.

The gui itself was designed so that the user can navigate between the different subjects, days and sessions easily. once a seesion is chosen, the gui presents the notes display. there are dedicated buttons to play the music displayed and to export the data as described.