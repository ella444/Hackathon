# Hackathon

## The research:
The research this project was created for is taking place in Dr Jason Friedman's Lab. 
The aim of this research is to determine whether musical practice on the piano helps to improve motor symptoms in PD patients. 
The patients will go through 6 weeks of piano practice (guided and unguided), as well as some examinations to test their motor abilities. 
The examinations will take place at the beginning and the end of the 6-week session, except one (QDG) that will be preformed weekly.
During this time the patients will have a keyboard at home, connected to an arduino device that will record their playing and store it as csv files of midi data. 
There will be a new file each day.

## The Project:
The aim of this project was to provide a tool to read and analyze the data from the piano.
It includes dividing the data into several playing sessions that were held in the same day, 
show statistical measures for the QDG test and play a chosen part, all this in an accesible gui.

## Project components:
- GUI: allows dynamic display of the recorded data, the graph element can be zoomed in and out and panned. 
* Browse for subjects data folder
* Choose between different subjects, days and sessions (defined as a minimum of 30 minutes break)
* Zoom and Pan
* Display the chosen session on the graph
* In the chosen range:
  ** Display Statistical analysis data and updated in real time.
  ** Play selected range
  ** Export the chosen data to a csv file of the specific data

- Statistical analysis: calculates 3 important measures of the QDG test: note duration, press velocity (intensity, how strong was the keyboard pressed) and frequency (taps per minute).

- Play Data: use the Play button to convert the data back to midi and play it.

- Test: use pytest to run 'run_test.py'. It tests the statistics calculations and the midi play module.  

#installation and Run
- In Windows run the 'run.bat' file. it will first install the requirements using pip and then run the Gui.
- Note: It might be necessary to adjust the file according to the python installed on the machine.
- python >= 3.8 is required. 