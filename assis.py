# asistan olaylarının döndüğü yer
import speech_recognition as speech
from gtts import gTTS
import os
import time
import mutagen
import filop as fi
from numbers import number

def commands_ex():
    cds="""
    + what time is it
    + search
      - web search
      + file search
        - search drivers #to find the all drivers from pc
        - search all folder # to find the all folder from pc
        - search folder name ....
        + search file name ....

    """
    #- search file name ... format text and picture and video ...
    #- open  # This function will open files or folders
    #- size
    print(cds)

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    duration_voice=mutagen.File("audio.mp3").info.length
    print(duration_voice)
    os.system("audio.mp3")
    time.sleep(duration_voice)

def record_data(explain="Say something!"):
    r = speech.Recognizer()
    with speech.Microphone() as source:
        print(explain)
        data = ""
        audio = r.listen(source)
        try:
            data = r.recognize_google(audio)
            print(r.recognize_google(audio))
        except speech.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except speech.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return data.lower()

def fofopen(fof,data): # dosya ve klasörleri açmak için kullanılıyor
    if "open" in data:
        data = data.replace("open","").replace(" ","")
        try:
            numb=int(data)
        except:
            numb = int(number[data])
        os.startfile(fof[numb-1])
        speak("file is opened sir")
        print(fof[numb-1])

def search(data):
    data = data.replace("search","")
    if "drivers" in data:
        drivers = fi.Filop(False).drivers
        speak("drivers on your computer,"+str(drivers))
    elif "all folder" in data:
        speak("I started searcing for you, sir")
        all_folder = fi.Filop().isdir
        print(all_folder,file = open("all_folder.txt","a"),flush = True)
        speak("I saved all the files for you in a text file name all_folder")
    elif "folder name" in data:
        data = data.replace("folder name","").replace(" ","")
        speak("I started searcing for you, sir ,folder searched >>> "+data)
        folder=fi.Filop().searchfolder(data)
        print("found folders >>>")
        folders_=[]
        number=1
        for fo in folder:
            print(str(number)+">>> "+fo)
            number+=1
            folders_.append(fo)
        if folders_!=[]:
            speak("the folder search is over, sir")
            speak("do you want open any folder ,exaple say open two or don't open")
            while True:
                data=record_data("open folder or file")
                if data:
                    fofopen(fof=folders_,data=data)
                    break

    elif "file name" in data:
        data = data.replace("file name","").replace(" ","")
        speak("I started searcing for you, sir ,file searched >>> "+data)
        files=fi.Filop().searchfile(data)
        print("found files >>>")
        for fo in files:
            print(fo)
        speak("the file search is over, sir")

def websearch():
    pass

def lucy(data):
    if data in ["hey lucy","lucy"]:
        speak("yes sir")
        lucy(record_data())
    elif "what time is it" in data:
        speak(time.asctime(time.localtime(time.time())))
    elif "search" in data:
        search(data)

speak("Hi, I am lucy, what can I do for you?")
commands_ex() # şuanlık yapabildiği şeyleri gösteriyor
while True:
    lucy(record_data())
