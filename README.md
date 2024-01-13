# TTS
 TTS Bible Reader 
 
 This program uses request to get bible verses for web sites like biblegateway.com and then uses a python package to read the verse that converts it to .mp3 file 
 that can be used in Radio or anyother media.
## config.ini
~~~ 
 [string_config]
 ; This will genrate ramdom verise for each day. 
 Scriptures:  john 3:16,Romans 10:9,Psm 22:8,Psalm 118:22-25

 [verceoftheday]
 version = KJV
~~~

## BibleRd.py
~~~ 
import schedule as sch
import configparser as ini
import os
import time
import requests
import json as j
import random as rd
from gtts import gTTS



def verseoftheday(): 
    cwd = os.getcwd()
    config = ini.ConfigParser()
    config.read_file(open(cwd+'\config.ini'))
    version = config['verceoftheday']['version']
    
    page = requests.get('https://www.biblegateway.com/votd/get/?format=json&version='+version)
    print(page.status_code)
    doc = j.loads(page.text)

     
    content = doc["votd"]["content"] 
    refvers =  doc["votd"]["reference"]+' '+ doc["votd"]["version"]
    text_string = f'{content}{refvers}'
      
    print(text_string)
    tts= gTTS(text_string, lang='en', tld='us')
    tts.save('biblegateway.mp3')
    
    page.close()
    
def randomverse(): 
   cwd = os.getcwd()
   config = ini.ConfigParser()
   config.read_file(open(cwd+'\config.ini'))
   biblev = config['string_config']['Scriptures']
   lst = biblev.split(',')
   print(lst)
   url = rd.choice(lst)
   print(url)
   page = requests.get('https://bible-api.com/'+url+'?translation=kjv')
   print(page.status_code)
   text = j.loads(page.text)
   string = f'{text["text"]}--{text["reference"]} {text["translation_name"]}'
   print(string)
   tts= gTTS(string, lang='en', tld='us')
   tts.save('randverse.mp3')

    
def main(): 
  verseoftheday()
  randomverse()
  sch.every().day.do(verseoftheday)
  sch.every().day.do(randomverse)
  
   
    
if __name__ == "__main__":
 main()
 print("press ctrl c to exit program")
 try:
   while True:
    sch.run_pending()
    time.sleep(1)
 except KeyboardInterrupt:
     print("You have exit the program")
~~~

## [Back](https://tcaviness.github.io/#code)
