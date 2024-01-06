__author__ = "Terry Caviness"
__version__ = "1.0"
__data__ = "12-2-23"
__copywrite__ = "2023 Copywrite"

"""
Author: Terry Caviness
Date: 12-2-23
Version: 1.0
Descripstion: This is a program that work with any radio automation that will give verse of the day from bible gateway and a random verse from a 
configeration file. Then turn it into a mp3 file for the automation to play it on the radio. 
"""

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

