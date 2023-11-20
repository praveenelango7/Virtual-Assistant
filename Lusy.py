import pyttsx3
import datetime
import speech_recognition as sr
import os
import sys
import webbrowser as wb
import wikipedia
from time import sleep
import pywhatkit
import requests
import json
import smtplib
from sys import platform
from newsapi import NewsApiClient


engine = pyttsx3.init()

def speak(audio):
 engine.say(audio)
 engine.runAndWait()

def getvoices(voice):
    voices = engine.getProperty("voices")
    #print(voices[1].id)
    if voice == 1:
        engine.setProperty("voice", voices[0].id)
    if voice == 2:
        engine.setProperty("voice", voices[1].id)
    speak("hello this is lucy")

def time():
    Time = datetime.datetime.now().strftime("%I:%M")
    speak("the time is")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("the date is")
    speak(date)
    speak(month)
    speak(year)

def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 4 and hour <12:
        speak("good morning boss!")
    elif hour >= 12 and hour <15:
        speak("good afternoon boss!")
    elif hour >= 15 and hour <21:
        speak("good evening boss!")
    elif hour >= 21 and hour <3:
        speak("good night boss!")
def wishme():
    speak("welcome back boss")
    time()
    date()
    greeting()
    speak("waiting to help you!")

def takeCommandCMD():
    query = input("waiting to help you!")
    return query

def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
         print("Listening...")
         r.pause_threshold = 1
         audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio , language="en-in")
        print(query)
    except Exception as e:
        print(e)
        speak('Please, could you say again!')
        return "None"
    return query


def searchgoogle():
    speak('what should i search for boss?')
    search = takeCommandMic()
    wb.open('https://www.google.com/search?q='+search)

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('virtualassistant192@gmail.com', 'Virtualassistant@192')
    server.sendmail('email', to, content)
    server.close()

def news():
    newsapi = NewsApiClient(api_key='5fe649059cfe4bd99437feb4355e33d8')
    speak('which tyoe of news do you want boss?')
    topic = takeCommandMic()
    data = newsapi.get_top_headlines(q=topic,
                                     language='en',
                                     page_size=5)
    
    newsdata = data['articles']
    for x,y in enumerate(newsdata):
        print(f'{x}{y["description"]}')
        speak(f'{x}{y["description"]}')
        
    speak('thats it for now boss, I will update you in sometime')

if __name__ == "__main__":
          getvoices(2)
          wishme()
          while True:
              query = takeCommandMic().lower()

              if 'time' in query:
                   time()

              elif 'date' in query:
                   date()
              
              elif 'wikipedia' in query:
                  speak('searching on wikipedia boss ...')
                  query = query.replace('wikipedia' , '')
                  result = wikipedia.summary(query , sentences = 2)
                  print(result)
                  speak(result)
              elif 'search' in query:
                  searchgoogle()
              elif 'youtube' in query:
                  speak('what should I search in youtube boss')
                  topic = takeCommandMic()
                  pywhatkit.playonyt(topic)
              elif 'weather' in query:
                  url = 'https://api.openweathermap.org/data/2.5/weather?q=trichy&units=imperial&appid=a8507dbc0297d4eb1dddcf0762f55fec'
                  res = requests.get(url)
                  data = res.json()
                  weather = data['weather'] [0] ['main']
                  temp = data['main']['temp']
                  desp =data['weather'][0]['description']
                  temp = round((temp -32)*5/9)
                  print(weather)
                  print(temp)
                  print(desp)
                  speak('Temperature : {} degree celcius'.format(temp))
                  speak('weather is {}'.format(desp))
              elif 'news' in query:
                  news()
              elif 'email to pravin' in query:
                    speak('What should I say?')
                    content = takeCommandMic()
                    to = 'praveenlovely301@gmail.com'
                    sendEmail(to, content)
                    speak('Email has been sent!')
              elif 'offline' in query:
                speak('have a nice day boss')
                quit()