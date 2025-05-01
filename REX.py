# Fixed version of your REX GUI Voice Assistant Code
import logging
import builtins

# Patch logging issues (for pyttsx3/comtypes)
if not hasattr(logging, 'error') or not callable(logging.error):
    import importlib
    importlib.reload(logging)
if not hasattr(builtins, 'logging') or builtins.logging is None:
    builtins.logging = logging
logging.basicConfig(level=logging.ERROR)

import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QThread
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from REXUI import Ui_REXUI

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                print("Listening timed out, please speak again.")
                return "none"

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")
        except Exception as e:
            speak("Say that again please...")
            return "none"

        return query

    def TaskExecution(self):
        wish()
        while True:
            self.query = self.takecommand().lower()

            if "open notepad" in self.query:
                os.startfile("C:\\Windows\\system32\\notepad.exe")

            elif "open adobe reader" in self.query:
                os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Adobe Reader XI.lnk")

            elif "open command prompt" in self.query:
                os.system("start cmd")

            elif "open camera" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow("webcam", img)
                    if cv2.waitKey(50) == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()

            elif "play music" in self.query:
                music_dir = "C:\\Users\\student\\Music"
                songs = os.listdir(music_dir)
                for song in songs:
                    if song.endswith('.mp3'):
                        os.startfile(os.path.join(music_dir, songs[0]))

            elif "what is my ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP address is {ip}")

            elif "wikipedia" in self.query:
                speak("Searching Wikipedia...")
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to Wikipedia")
                speak(results)

            elif "open youtube" in self.query:
                webbrowser.open("https://www.youtube.com")

            elif "open stackoverflow" in self.query:
                webbrowser.open("https://www.stackoverflow.com")

            elif "open facebook" in self.query:
                webbrowser.open("https://www.facebook.com")

            elif "open google" in self.query:
                speak("What should I search on Google?")
                cm = self.takecommand().lower()
                webbrowser.open(f"https://www.google.com/search?q={cm}")

            elif "send message" in self.query:
                kit.sendwhatmsg("+919306006827", "HELLO HOW ARE YOU", 10, 50)

            elif "play songs on youtube" in self.query:
                kit.playonyt("night changes")

            elif "email to vikram" in self.query:
                try:
                    speak("What should I say?")
                    content = self.takecommand().lower()
                    to = "varchasva2210@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been sent to Vikram")
                except Exception as e:
                    print(e)
                    speak("Sorry, I am not able to send this email to Vikram")
            
            elif "email to yashika" in self.query:
                try:
                    speak("What should I say?")
                    content = self.takecommand().lower()
                    to = "sharmay0805@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been sent to yashika")
                except Exception as e:
                    print(e)
                    speak("Sorry, I am not able to send this email to yashika")

            elif "no thanks" in self.query:
                speak("Thanks you, have a good day.")
                sys.exit()

            speak("Do you have any other work?")

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning Ma'am")
    elif hour > 12 and hour <= 18:
        speak("Good Afternoon Ma'am")
    else:
        speak("Good Evening Ma'am")
    speak("I am REX. Please tell me how can I help you")

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('garvitsharmagamer@gmail.com', 'jtem uypk buzf zlpg')
    server.sendmail('garvitsharmagamer@gmail.com', to, content)
    server.close()

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_REXUI()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QMovie("../../Downloads/rex_voice_assistant_ui_fixed.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie2 = QMovie("../../Downloads/T8bahf.gif")
        self.ui.label_2.setMovie(self.ui.movie2)
        self.ui.movie2.start()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
REX = Main()
REX.show()
sys.exit(app.exec_())