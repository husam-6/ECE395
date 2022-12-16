# ECE395
Repo for Senior Projects work


## Outline

This repository contains software intended for use in the senior project "Checkmate": A Voice-Controlled
Chess board. The software can be broken up into 2 main components (currently speaking). The 
speech recognition portion, in which we test and implement a framework that is capable of beginning
a recording on command, and then subsequently recording and transcribing a users move. The relevant code
can be found in the folder *speech_recognition*

The second portion of the software portion of our project is the rules engine. This involves keeping track
of a boards state, inputting a move and testing whether or not it is valid for the given players turn. For 
this, we opt to leverage the Python-Chess library that provides us with many resources we can use to keep a 
free flowing game running. The relevant code for testing can be found in the folder *rules_engine*

Additionally, this repo may evolve to include any miscellaneous code relevant to our project. Currently, the 
gantt.py file contains a script to create a Gantt Chart to help us plan out a structured project across 2 
semesters.  


