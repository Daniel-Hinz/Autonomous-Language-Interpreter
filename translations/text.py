from __future__   import division
from bs4          import BeautifulSoup
from google.cloud import translate_v2 as translate

import os

# Get service key and set path for audio file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r".\\ServiceKey.json"   
path = r".\\ALI-Output\\output.mp3" 

# Global audio recording parameters
RATE = 24000 
CHUNK = int(RATE / 10)  

# Instantiate clients for translate and T2S
translate_client = translate.Client()

#################################################################################
# Main driver function to provide text translation   
def translateText(var1, text):
    with open('templates/translate.html', 'rb') as file:
        soup = BeautifulSoup(file.read(), "lxml") 
        output = translate_client.translate(text, target_language=var1)
        soup.find("textarea", {"id": "t1"}).append(text)
        soup.find("textarea", {"id": "t2"}).append(output['translatedText'])
        file.close()
        

    savechanges = soup.prettify("utf-8")
    with open("templates/translate.html", "wb") as file:
        file.write(savechanges)
        file.close()

# clears textarea in takehome.html page
def clearTextTags(): 
    with open('templates/translate.html', 'rb') as file:
        soup = BeautifulSoup(file.read(), "lxml") 
        soup.find("textarea", {"id": "t1"}).clear()
        soup.find("textarea", {"id": "t2"}).clear()
        file.close()

    savechanges = soup.prettify("utf-8")
    with open("templates/translate.html", "wb") as file:
        file.write(savechanges)
        file.close()

# clears text area in home.html
def clearHomeTags(): 
    with open('templates/home.html', 'rb') as file:
        soup = BeautifulSoup(file.read(), "lxml") 
        soup.find("textarea", {"id": "t1"}).clear()
        soup.find("textarea", {"id": "t2"}).clear()
        file.close()

    savechanges = soup.prettify("utf-8")
    with open("templates/home.html", "wb") as file:
        file.write(savechanges)
        file.close()

if __name__ == "__main__":
    main()