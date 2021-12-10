from __future__   import division
from playsound    import playsound
from six.moves    import queue
from bs4          import BeautifulSoup
from google.cloud import speech
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from google.cloud import texttospeech_v1

import keyboard
import pyaudio
import os
import re
import sys
import pandas as pd


# Get service key and set path for audio file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r".\\ServiceKey.json"   
path = r".\\ALI-Output\\output.mp3" 

# Global audio recording parameters
RATE = 24000 
CHUNK = int(RATE / 10)  

# Instantiate clients for translate and T2S
translate_client = translate.Client()
client = texttospeech_v1.TextToSpeechClient()


#################################################################################
# Class to provide speech translation 
class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    # Create a thread safe audio buffer
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    # Run the audio stream asynchronously to fill the buffer object.
    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False
        return self

    # Signal the generator to terminate
    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    # Fill the buffer
    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    # Ensure there's at least one chunk of data and stop iteration otherwise
    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


##########################################################################
## Speech Translation function
def listen_print_loop(responses, var1, var2):
    with open('templates/home.html', 'rb') as file: 
        soup = BeautifulSoup(file.read(), "lxml") 
        soup.find("textarea", {"id": "t1"}).clear()
        soup.find("textarea", {"id": "t2"}).clear()
        file.close()
    
    savechanges = soup.prettify("utf-8")
    with open("templates/home.html", "wb") as file:
        file.write(savechanges)
        file.close()

    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()
            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)

            text = (transcript)
            target = var2

            output = translate_client.translate(text, target_language=target)
            print(output['translatedText'])
            speechString = output['translatedText']
            
            #print input and output
            with open('templates/home.html', 'rb') as file: 
                soup = BeautifulSoup(file.read(), "lxml") 
                soup.find("textarea", {"id": "t1"}).append(output['input'])
                soup.find("textarea", {"id": "t2"}).append(output['translatedText'])

                file.close()

            savechanges = soup.prettify("utf-8")
            with open("templates/home.html", "wb") as file:
                file.write(savechanges)
                file.close()

            # Set the text input to be synthesized
            quote = output['translatedText']
            synthesis_input = texttospeech_v1.SynthesisInput(text=quote)
            voice = texttospeech_v1.VoiceSelectionParams(
                language_code=var2, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )

            # Set the voice/accent the output speaks in
            voice = texttospeech_v1.VoiceSelectionParams(
                name='en-US-Standard-A,en-US,1,15000', language_code=var2
            )

            # Select the type of audio file you want returned
            audio_config = texttospeech_v1.AudioConfig(
                audio_encoding=texttospeech_v1.AudioEncoding.MP3
            )

            # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
        
            # The response's audio_content is binary
            with open(path, "wb") as out:

                # Write the response to the output file
                out.write(response.audio_content)
                print('Audio content written to file "output.mp3"')
                out.close()
            
            # Play and remove the audio file
            playsound(path) 
            os.remove(path) 
        
            # Terminate loop if user says stop in any language
            if re.search(r"\b(stop|exit|dejar|parada|توقف|停止|arrêter|quitter|halt|विराम|止まる|멈추다|zatrzymać|Pare|Parar|останавливаться|ఆపు|ఆపండి|Dur|ngừng lại|thôi)\b", transcript, re.I):
                print("Exiting..")
                break
            
            if keyboard.is_pressed("space"):
                break

            num_chars_printed = 0


#################################################################################
# Main driver function to provide speech translation       
def main(var1, var2):
    open(path, "a")

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=var1,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:

        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)
        listen_print_loop(responses, var1, var2)


#################################################################################
# Main driver function to provide text translation   
def takeHomeTranslate(var1, text):
    with open('templates/takeHome.html', 'rb') as file:
        soup = BeautifulSoup(file.read(), "lxml") 
        output = translate_client.translate(text, target_language=var1)
        soup.find("textarea", {"id": "t1"}).append(text)
        soup.find("textarea", {"id": "t2"}).append(output['translatedText'])
        file.close()
        

    savechanges = soup.prettify("utf-8")
    with open("templates/takeHome.html", "wb") as file:
        file.write(savechanges)
        file.close()

# clears textarea in takehome.html page
def clearTextTags(): 
    with open('templates/takeHome.html', 'rb') as file:
        soup = BeautifulSoup(file.read(), "lxml") 
        soup.find("textarea", {"id": "t1"}).clear()
        soup.find("textarea", {"id": "t2"}).clear()
        file.close()

    savechanges = soup.prettify("utf-8")
    with open("templates/takeHome.html", "wb") as file:
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