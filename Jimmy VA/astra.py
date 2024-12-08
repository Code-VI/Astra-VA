import speech_recognition as sr
import webbrowser
from gtts import gTTS
import keyboard
import pygame
import pyaudio,sys,time
import pyautogui
import io
import subprocess
from music import songs  # Ensure 'songs' is a valid dictionary

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

recognizer = sr.Recognizer()

def opening(text):
    text_split=text.split()
    speak_text(f'opening {text_split[1]}')
    

def taking_command(c):

    if 'astra' in c.lower():
         speak_text('Yes, How may i help You?')
    elif 'type following' in c.lower():
         speak_text('ready when you are')
         while True:
            try:
                with sr.Microphone() as source:
                    print('Listening...')
                    audio = recognizer.listen(source)
                    data = recognizer.recognize_google(audio)
                    if 'hit enter' in data:
                        keyboard.press_and_release('enter')
                        speak_text('As you wish')
                        break
                    elif 'new line' in data:
                        keyboard.press_and_release('enter')
                    elif 'done' in data:
                        speak_text('Hope that helps')
                        break
                    print(f'You said:\n {data}')
                    final = data + ' '
                    pyautogui.typewrite(final)
            except sr.UnknownValueError:
                speak_text('come again')
                continue
            except   sr.RequestError:
                speak_text('Please check your connection')
                continue
    elif 'hit enter' in c.lower():
        keyboard.press_and_release('enter')
#sometimes all you new line sometimes new line new line hit enter 

    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
        opening(c)
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com")
        opening(c)
    elif "open google" in c.lower():
        webbrowser.open("https://www.google.com")
        opening(c)
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
        opening(c)
    elif "open chatgpt" in c.lower():
        webbrowser.open("https://www.chatgpt.com")
        opening(c)
    elif "open replit" in c.lower():
        webbrowser.open("https://www.replit.com")
        opening(c)
    elif 'shutdown' in c.lower():
        subprocess.run("shutdown /s /t 1", shell=True)
    elif 'open calculator' in c.lower():
        subprocess.run('calc', shell=True)   
    elif 'suspend' in c.lower():
        speak_text('see you in 60 minutes')
        time.sleep(3600)  
        speak_text('I am back')
    elif 'deactivate' in c.lower():
        speak_text('bye') 
        sys.exit()       
    elif c.lower().startswith('play'):
        speak_text('name the song you want to play')
        song = c.lower().split(' ')
        song_name = '_'.join(song)
        if song in songs:
            speak_text(f'playing {song}')
            
            link = songs[song]
            webbrowser.open(link)
        else:
            speak_text(f"Song {song} not found")

if __name__ == "__main__":
    speak_text('Hello! I\'m Astra. what can i assist you with?')

    # while True:
    #     try:
    #         with sr.Microphone() as source:
    #             print('Listening for wake word...')
    #             audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
    #             word = recognizer.recognize_google(audio)
    #             if word.lower() == 'astra':
    #                 speak_text('yes?')
while True:
                        try:
                            with sr.Microphone() as source:
                                print('Listening...')
                                audio = recognizer.listen(source, timeout=3600, phrase_time_limit=2)
                                command = recognizer.recognize_google(audio)
                                taking_command(command)
                                if taking_command == False:
                                    break
                        except sr.UnknownValueError:
                            print("Couldn't understand audio")
                            continue
                        except sr.RequestError as e:
                            print(f"Could not request results; {e}")
                            continue
                        except Exception as e:
                            print(f"An error occurred: {e}")
                            continue
        
        # except sr.UnknownValueError:
        #     print("Couldn't understand audio")
        # except sr.RequestError as e:
        #     print(f"Could not request results; {e}")
        # except Exception as e:
        #     print(f"An error occurred: {e}")
