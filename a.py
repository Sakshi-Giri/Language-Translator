from pytube import YouTube
from gtts import gTTS
import os
import pygame
import time
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
# Initialize Pygame for audio playback
from pytube import YouTube
from gtts import gTTS
import os
import pygame
import time
import speech_recognition as sr
from googletrans import Translator

# Initialize Pygame for audio playback
pygame.init()
pygame.mixer.init()

# Function to play audio file
def play_audio(file_path):
    try:
        pygame.mixer.music.load(file_path)
        print(f"Playing {file_path}")
        pygame.mixer.music.play()

        # Allow time for the audio to play
        while pygame.mixer.music.get_busy():
            time.sleep(2)

    except pygame.error as e:
        print(f"Error: {e}")

# Function to convert audio speech to text
def audio(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        print("Text from video speech:", text)
    return text

# Link of the YouTube video
link = "https://www.youtube.com/watch?v=5xYDXp7fkY4"

# Where to save the downloaded audio
SAVE_PATH = "D://code//frontend part//video"

try:
    video = YouTube(link)
    # filtering the audio. File extension can be mp4/webm
    # You can see all the available streams by print(video.streams)
    audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
    audio.download(SAVE_PATH)
    print('Download Completed!')
    print('Audio downloaded successfully!')
except Exception as e:
    print("Error:", e)

# Path to the downloaded audio file
audio_path = os.path.join(SAVE_PATH, f"{video.title}.mp4")

# Debugging: Print audio_path to verify the path
print("Audio path:", audio_path)

# Extract text from the audio file
extracted_text = audio(audio_path)

# Translate the extracted text
language = "en"  # Replace with the desired language code
translator = Translator()
translated = translator.translate(extracted_text, dest=language)
translated_text = translated.text
print("Translated text:", translated_text)

# Save translated text to an audio file
tts = gTTS(text=translated_text, lang=language, slow=False)
audio_output_path = "video//audio_text.mp4"
#tts.save(audio

tts.save(audio_output_path)

# Play the audio file
play_audio(audio_output_path)
