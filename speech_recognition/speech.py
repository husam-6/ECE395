""" Husam Almanakly & Michael Bentivegna

ECE395 
Test script to use Whisper Open AI to transcribe audio to text
"""

import whisper
import pyaudio
import wave
from pydub import AudioSegment


# Bring in Whisper model (pre-trained)
options = whisper.DecodingOptions(fp16=False)
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

result = model.transcribe("output.mp3")
print(result["text"])