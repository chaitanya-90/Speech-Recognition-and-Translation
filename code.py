import tkinter as tk
from tkinter import messagebox, ttk
import speech_recognition as sr
from googletrans import Translator
import pyttsx3 as ts
from gtts import gTTS
import os
import webbrowser as wb
from PIL import Image, ImageTk


engine = ts.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 for male, 1 for female
engine.setProperty('rate', 150)

def recognize_and_translate():
    recognizer = sr.Recognizer()
    translator = Translator()
    target_lang = languages[language_var.get()]

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source) 
            print("Listening...")
            audio = recognizer.listen(source)

        text = recognizer.recognize_google(audio).lower()
        # print("You said:", text)

        if text.startswith('open'):
            recognized_text_var.set(text)
            website = text.split()[1]
            url = 'https://www.' + website + '.com'
            engine.say('opening ' + website)
            engine.runAndWait()
            wb.open(url)  
        else:
            recognized_text_var.set(text)
            engine.say(text)
            engine.runAndWait()
            trans = translator.translate(text, src='en', dest=target_lang)
            translated = trans.text
            translated_text_var.set(translated)
            # print('\nTranslated text: ', translated)
            tts = gTTS(text=translated, lang=target_lang, slow=False)
            tts.save("output.mp3")
            play_audio_button.config(state=tk.NORMAL) 
             

    except sr.WaitTimeoutError:
        messagebox.showerror("Error", "Input not received for a long time.")
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Sorry, could not understand the audio.")
    except sr.RequestError as e:
        messagebox.showerror("Error", f"Could not request results; {e}")

def play_audio():
    os.system("start output.mp3")

win = tk.Tk()
win.title("Voice Assistant")
win.geometry("300x500")  

header_font = ("Helvetica", 20, "bold")
text_font = ("Helvetica", 16)
label_font = ("Helvetica", 14)
bg_color = "#100720"
fg_color = "#61dafb"
button_color = "#21a1f1"
button_fg_color = "#ffffff"

win.configure(bg=bg_color)


recognized_text_var = tk.StringVar()
translated_text_var = tk.StringVar()

p1 = Image.open('Web Dev\IMG\mic.png')
mic = ImageTk.PhotoImage(p1)
p2 = Image.open("Web Dev\IMG\speaker.png")
speak = ImageTk.PhotoImage(p2)


# tk.Label(win, text="Press the button and start speaking", font=header_font, bg=bg_color, fg=fg_color).pack(pady=20)
tk.Button(win, image=mic, command=recognize_and_translate,bg=bg_color,border=0,activebackground='grey').pack(pady=10)

tk.Label(win, text="Recognized Text", font=label_font, bg=bg_color, fg='#FFBF61').pack(pady=10)
tk.Label(win, textvariable=recognized_text_var, wraplength=600, font=text_font, bg=bg_color, fg='#F36886').pack(pady=10)

language_var = tk.StringVar(value='None')
languages = {
    'Telugu': 'te',
    'Tamil':'ta',
    'Malayalam':'ml',
    'Kannada':'kn',
    'Hindi': 'hi',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de'
}
tk.Label(win, text="Select Language", font=label_font, bg=bg_color, fg=fg_color).pack(pady=10)
language_menu = ttk.Combobox(win, textvariable=language_var, values=list(languages.keys()), font=("Helvetica", 10),width=10)
language_menu.pack(pady=10)

tk.Label(win, text="Translated Text", font=label_font, bg=bg_color, fg='#FFBF61').pack(pady=10)
tk.Label(win, textvariable=translated_text_var, wraplength=600, font=text_font, bg=bg_color, fg='#F36886').pack(pady=10)


play_audio_button = tk.Button(win, image=speak, command=play_audio,bg=bg_color,state=tk.DISABLED,border=0,activebackground='grey')
play_audio_button.pack(pady=20)

win.mainloop()
