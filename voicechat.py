import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
# Audio prompts
# from gtts import gTTS
from playsound import playsound
import os
import pyttsx3
from collections import defaultdict
import requests
import python_weather
import asyncio


#Initiаlize  reсоgnizer
r = sr.Recognizer()

# Audio to File
def audio_File():    
    fs = 44100  # Sample rate
    seconds = 7  # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype='int32', blocking=True)
    status = sd.get_status()
    print(status)
    sd.wait()  # Wait until recording is finished
    write(r'PUT AUDIO FILE LOCATION HERE, USE SAME FOLDER', fs, myrecording)  # Save as WAV file 
audio_File()

#  Audio to Text
def file_Text():
    with sr.AudioFile(r'PUT AUDIO FILE LOCATION HERE, USE SAME FOLDER') as source:
        audio_text = r.listen(source)
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    try:
        # using google speech recognition
        text = r.recognize_google(audio_text)
        file = open(r'PUT TEXT FILE LOCATION HERE, USE SAME FOLDER', 'w')
        file.write(text)
        print('Converting audio transcripts into text ...')
        print('Question', text)
    except:
         print('Convert Failed')
file_Text()


# Text File to Audio
def audio_prompt(): 

    text_file = open(r'PUT TEXT FILE LOCATION HERE, USE SAME FOLDER', 'r')    
    myText = text_file.read() 

    ## PUT CONDITIONAL WORD PROMPTS HERE
    fullString = myText   
    bitcoinPriceString = 'Bitcoin'
    weatherString = 'weather'
    googleString = 'Google'  
    priceString = 'price of'         
   

    if priceString in fullString:
        symbolText = myText.replace('is the price of', '')
        symbolFiltered = symbolText.replace('what', '')
        symbolFilteredSpace = symbolFiltered.replace(' ', '')
        print(symbolFiltered)
        symbol = symbolFilteredSpace
        base_url = 'https://api.binance.com/api/v3'                  
        url = base_url + f'/avgPrice?symbol={symbol}USDT'
        print(url)
        r = requests.get(url) 
        response = r.json()
        priceFloat = response['price']        
        print('Answer:', priceFloat)
        
        computerResponse = str(priceFloat)
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        rate = engine.getProperty('rate')   # getting details of current speaking rate        
        engine.say(computerResponse + 'USDT')
        engine.runAndWait()
    # General Google search to Json NOT working
    elif googleString in fullString:
        try:
            from googlesearch import search
        except ImportError:
            print('No module named google found')
        
        # to search
        query = fullString
        
        for j in search(query, tld='co.in', num=10, stop=10, pause=2):
            print(j)
    #Weather Prompt Working
    elif weatherString in fullString:
        import bs4                
        url = 'https://google.com/search?q=weather+in+' + myText        
        request_result = requests.get( url )
        
        # Pulling HTTP data from internet 
        soup = bs4.BeautifulSoup( request_result.text 
                                , 'html.parser' )
        # The temperature is stored inside the class 'BNeawe'. 
        temp = soup.find( 'div' , class_='BNeawe' ).text 
            
        print( temp )
        inMyText = myText.replace('weather','')
        weatherMyText = inMyText.replace('in','')         
        computerResponse = 'It is ' + temp + ' in ' + weatherMyText
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        rate = engine.getProperty('rate')   # getting details of current speaking rate
        engine.say(computerResponse)
        engine.runAndWait()
    else: 
        computerResponse = 'Im sorry, I dont understand' + myText
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        rate = engine.getProperty('rate')   # getting details of current speaking rate
        print (rate) 
        engine.say(computerResponse)
        engine.runAndWait()
   
audio_prompt()


### working above