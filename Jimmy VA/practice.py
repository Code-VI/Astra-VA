from gtts import gTTS
import pygame
import io

def speak_text(text):
    # Convert text to speech
    tts = gTTS(text=text, lang='en')
    
    # Create an in-memory file
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)  # Reset file pointer to the start

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fp, "mp3")  # Load from the in-memory file
    pygame.mixer.music.play()

    # Keep the program running until the audio is done
    while pygame.mixer.music.get_busy():
        continue

# Example usage
speak_text("Hello, I am Astra. How can I assist you?")
