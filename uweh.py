import pyttsx3 as sp
import speech_recognition as sr
import wikipedia as wiki
import time
import pvporcupine as pv
import pyaudio
import struct
import os
import subprocess
import signal
from playsound import playsound
import weather
import processControl



engine=sp.init('espeak')
voices=engine.getProperty('voices')
engine.setProperty('rate',155)
r=sr.Recognizer()

pa=pyaudio.PyAudio()
porcupine=pv.create(keywords=["jarvis"])
audioStream=pa.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)

minecraftRunning=False

playsound("welcome.mp3")
try:
    while True:
        while True:
            prompt=None
            pcm=audioStream.read(porcupine.frame_length)
            pcm=struct.unpack_from("h"*porcupine.frame_length,pcm)
            result=porcupine.process(pcm)
            if result>=0:
                playsound('acknowledge.mp3')
                break
        with sr.Microphone() as source:
            try:
                audio=r.listen(source,timeout=10)
                playsound('finish.mp3')
                try:
                    prompt=r.recognize_google(audio)
                except:
                    engine.say("Sorry, I did not catch that")
                    engine.runAndWait()

            except:
                playsound('finish.mp3')
        print(prompt)
        if prompt:
            prompt=prompt.lower()
            answered=False
            
            #####################ANSWER QUESTION##################################
            questionWords=['who is', 'who are', 'what is', 'what are', 'where is', 'where are', 'why is', 'why are', 'when is', 'where are', 'research',"what's"] #consider adding contractions what's ect.
            question=False
            phrase=None      
            for words in questionWords:
                if words in prompt:
                    question=True
                    phrase=words
            if question:
                try:
                    if 'weather' in prompt or 'whether' in prompt or 'temperature' in prompt:
                        engine.say(weather.get_weather(prompt))
                        engine.runAndWait()
                        answered=True
                    else:
                        engine.say(wiki.summary(prompt.replace(phrase,''),sentences=3))
                        engine.runAndWait()
                        answered=True
                except:
                    engine.say("sorry I do not know that")
                    engine.runAndWait()
            #####################ANSWER QUESTION##################################
   
            #################MINECRAFT##############################################
            if 'minecraft' in prompt or 'mindcraft' in prompt or 'mind craft' in prompt or 'mine craft' in prompt:
                # os.system("/home/ubuntu/.local/share/applications/minecraft.desktop")
                if 'quit' in prompt or 'close' in prompt or 'exit' in prompt or 'home' in prompt or minecraftRunning==True:
                    try:
                        minecraftProcess=processControl.filterMinecraft()
                        for process in minecraftProcess:
                            os.kill(process,signal.SIGTERM) ### terminate minecraft
                        # print(craftingDawg.pid)
                        ###look into psutil then do os kill pid, signal.sigterm
                        answered=True
                        minecraftRunning=False
                    except:
                        pass
                # os.system("xdotool windowsize $(xdotool getactivewindow) 75% 75%")
                else:
                    craftingDawg=subprocess.Popen("/home/ubuntu/.local/share/applications/minecraft.desktop",shell=True) ###start minecraft
                    minecraftRunning=True
                    time.sleep(10)
                    os.system("xdotool windowsize $(xdotool getactivewindow) 100% 100%")
                    answered=True
            #################MINECRAFT##############################################

            #################Nevermind##############################################
            if 'nevermind' in prompt:
                answered=True
            #################Nevermind##############################################

            if answered==False:
                engine.say("I am sorry I do not know how to respond to that")
                engine.runAndWait()

except:
    print("error")
finally:
    if porcupine:
        porcupine.delete()
    if audioStream:
        audioStream.close()
    if pa:
        pa.terminate()

