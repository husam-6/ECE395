""" Husam Almanakly & Michael Bentivegna

ECE395 
Test script to use Whisper Open AI to transcribe audio to text

To do:
+ Get castling work
+ pawn captures
+ when two pieces of the same kind can both access a square

"""
import whisper
import pyaudio
import wave
from pydub import AudioSegment
import re
import speech_recognition as sr
import time

def getMoveFromAudio():
    """Function to use python script to read in an audio recording
    
    and transcribe it using OpenAI Whisper Model
    """

    # Bring in Whisper model (pre-trained)
    # options = whisper.DecodingOptions(fp16=False)
    model = whisper.load_model("base")

    """ Code to record audio real time - obtained from 

    https://realpython.com/playing-and-recording-sound-python/?
    fbclid=IwAR0uPIZmDCBPcaJoAT_g3jTU0UH9Oj-3J3BZw7jDsIwRIeHttc0GCxY7BKg

    """

    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 3
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))

    # Convert to MP3 file
    sound = AudioSegment.from_wav(filename)
    sound.export('output.mp3', format='mp3')

    wf.close()

    result = model.transcribe("output.mp3", fp16=False)

    return parse_text(result["text"])


def parse_text(text: str):
    if len(text) == 0:
        return text

    if text[-1] == '.':
        text = text[:-1]
    
    process_string = text.split()
    
    # print(process_string)

    pieces = {"pawn" : "", 
            "rook" : "R",
            "bishop" : "B", 
            "knight": "N", 
            "night": "N", 
            "king" : "K",
            "king's": "K",
            "queen's": "Q", 
            "queen" : "Q"}

    # print(process_string)

    move = ""

    for item in process_string:
        # If the word is a piece...
        if re.match("^(?=.*[a-zA-Z])", item) and len(item) == 1:
            move += item.lower()
        if item.lower() in pieces:
            move += pieces[item.lower()]
        # If the word is the square to move to...
        if (item.lower() == "takes"):
            move += 'x'
        if(re.match("^(?=.*[a-zA-Z])(?=.*[0-9])", item) and len(item) == 2):
            move += item.lower()
        
        if item.lower() == "castle":
            if move == "Q":
                move = "O-O-O"
            else:
                move = "O-O"

    print(move)
    return move


def callback(recognizer, audio):  # this is called from the background thread
    # Words that sphinx should listen closely for. 0-1 is the sensitivity
    # of the wake word.
    keywords = [("chessboard", 1), ("hey chessboard", 1), ("rook D6", 1)]
    try:
        speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
        print(speech_as_text)

        # Look for your "Ok Google" keyword in speech_as_text
        if "chessboard" in speech_as_text or "hey chessboard":
            getMoveFromAudio()

    except sr.UnknownValueError:
        print("Oops! Didn't catch that")


def start_recognizer():
    print("Listening in background")
    r = sr.Recognizer()
    source = sr.Microphone(0)
    with source as s:
        r.adjust_for_ambient_noise(s)  
    r.listen_in_background(source, callback)
    time.sleep(1000000)


if __name__ == "__main__":
    start_recognizer()
    # getMoveFromAudio()
