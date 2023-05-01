""" Husam Almanakly & Michael Bentivegna

ECE395 
Test script to use Whisper Open AI to transcribe audio to text

To do:
+ Get castling work
+ pawn captures
+ when two pieces of the same kind can both access a square

"""
# import whisper
import pyaudio
import wave
#from pydub import AudioSegment
import re
import speech_recognition as sr
import time
import chess
import chess.svg
import rules_engine
import arduino_control
from pocketsphinx import LiveSpeech
import numpy as np
import time
import logging
from whispercpp import Whisper


logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)

# Bring in Whisper model (pre-trained)
logging.info("Loading in whisper model")
# board = chess.Board()
# board = chess.Board(fen="r1bqk2r/2p1bpp1/p1n1p2p/1p1p4/3Pn3/NQPRBNP1/PP2PP1P/2K2B1R b kq - 0 1")
model = Whisper.from_pretrained("tiny.en")
# model = Whisper.from_pretrained("base.en")


def get_move_from_audio():
    """Function to use python script to read in an audio recording
    
    and transcribe it using OpenAI Whisper Model
    """


    """ Code to record audio real time - obtained from 

    https://realpython.com/playing-and-recording-sound-python/?
    fbclid=IwAR0uPIZmDCBPcaJoAT_g3jTU0UH9Oj-3J3BZw7jDsIwRIeHttc0GCxY7BKg

    """
    
    #time.sleep(1);
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    # fs = 44100  # Record at 44100 samples per second
    fs = 16000  # Record at 44100 samples per second
    seconds = 3
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    logging.info('Recording')
    arduino_control.board.send_sysex(arduino_control.STRING_DATA, arduino_control.util.str_to_two_byte_iter('RECORDING'))
    # for i in range(p.get_device_count()):
    #     logging.info(p.get_device_info_by_index(i))

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    input_device_index=1,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(np.frombuffer(data, dtype=np.int16))

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    logging.info('Finished recording')
    arduino_control.board.send_sysex(arduino_control.STRING_DATA, arduino_control.util.str_to_two_byte_iter('DONE RECORDING'))

    start_time = time.time()
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))

    arduino_control.board.send_sysex(arduino_control.STRING_DATA, arduino_control.util.str_to_two_byte_iter('TRANSCRIBING'))
    result = model.transcribe_from_file(filename)
    logging.info(f"{result}")
    end_time = time.time()
    logging.info(f"Time taken to transcribe move: {end_time - start_time}")
    move = parse_text(result)
    logging.info(f"Parsed: {move}")
    arduino_control.board.send_sysex(arduino_control.STRING_DATA, arduino_control.util.str_to_two_byte_iter(f'PARSED: {move}'))
    global board
    rules_engine.make_move(board, move)
    # rules_engine.make_move(board, move)


def parse_text(text: str):
    if len(text) == 0:
        return text

    if text[-1] == '.':
        text = text[:-1]
    
    process_string = text.split()
    
    # logging.info(process_string)

    pieces = {"pawn" : "", 
            "rook" : "R",
            "bishop" : "B", 
            "knight": "N", 
            "night": "N", 
            "9": "N", 
            "ninth": "N", 
            "king" : "K",
            "king's": "K",
            "queen's": "Q", 
            "queen" : "Q",
            "see":  "c",
            "be":   "b",
            "bee":  "b",
            "9":    "N",
            "nine":    "N",
            "ninth":    "N",
            "nice":    "N",
            }

    # logging.info(process_string)

    move = ""
    logging.info(process_string)
    for item in process_string:
        # If the word is a piece...
        if item.lower() in pieces:
            move += pieces[item.lower()]
        elif re.match("^([a-hA-H])", item) and len(item) == 1:
            move += item.lower()
        elif(re.match("^([a-hA-H])", item) and len(item) == 2):
            move += item.lower()
        # If the word is the square to move to...
        elif (item.lower() == "takes"):
            move += 'x'
        elif(re.match("^([a-hA-H])([0-9])", item) and len(item) == 2):
            move += item.lower()
        elif item.lower() == "castle":
            if move == "Q":
                move = "O-O-O"
            else:
                move = "O-O"

    # Figure out if its a pawn promotion
    if move != '':
        if not move[0].isupper() and (move[-1]=='8' or move[-1]=='1'):  
            move = move + "=Q"

    return move


def callback(recognizer, audio):  # this is called from the background thread
    # Words that sphinx should listen closely for. 0-1 is the sensitivity
    # of the wake word.
    keywords = [("hey chess", 1), ("chess", 1)]
    try:
        speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords).lower()
        logging.info(speech_as_text)

        if ("chess" in speech_as_text) or ("hey chess" in speech_as_text):
            get_move_from_audio()

    except sr.UnknownValueError:
        logging.info("Oops! Didn't catch that")


def start_recognizer():
    logging.info("Listening in background")
    r = sr.Recognizer()
    source = sr.Microphone(1)
    with source as s:
        r.adjust_for_ambient_noise(s)  
    r.listen_in_background(source, callback)
    time.sleep(1000000)


if __name__ == "__main__":
    logging.info(f"\n{board}")
    logging.info(sr.Microphone.list_microphone_names())
    if board.turn:
        arduino_control.board.send_sysex(arduino_control.STRING_DATA, arduino_control.util.str_to_two_byte_iter('WHITES TURN!'))
    else:
        arduino_control.board.send_sysex(arduino_control.STRING_DATA, arduino_control.util.str_to_two_byte_iter('BLACKS TURN!'))

    start_recognizer()
    # get_move_from_audio()
