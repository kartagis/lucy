# asistan olaylarının döndüğü yer
import speech_recognition as speech
from gtts import gTTS
import os
import time
import mutagen

from numbers import number
from filop import Filop
from abouturl import General,Youtube

def help():
    cds="""
    # you can check or run with talking

     commands that can be executed by the program
     ---------

      use as follow
      -----

      ```python
      from assis import lucy,record_data
      lucy(record_data())
      ```
     - and you can speak

      example speak ;
      ------
      - hey lucy
      - help
      + you can learn the time
        - what time is it
      + you can search
        - search drivers #to find the all drivers from pc
        - search folder name new file
        + search file name readme
          - open 6
        - search all folder # to find the all folder from pc
        + search on web python
          - open 10
      + you can open drivers of your computer
        - open d driver
        - open d c drivers
      + you can run defined applications on your desktop
        - open application google chrome
        - open application media player


    # you can check with commands instead of talking

    example ;
     ------
    ```python

    from assis import lucy,record_data,Search

    lucy("open d c drivers") # open drivers d:\ or c:\
    lucy("search folder name python")
    lucy("hey lucy")
    lucy("search drivers")
    lucy("search file name django")
    lucy("open chrome applications")
    lucy("search on web face")
    lucy("search on web python programming")

    lucy(record_data())

    Search("search on web face")
    Search("driver")
    Search("folder name python")
    Search("file name python")
    Search("all folder")
     ```

    """
    print(cds)

class Search(): # arama işlemleri
    def __init__(self,data):
        self.data = data.replace("search ","")
        self.folders_=[]
        self.number=1
        self.files_=[]
        if "driver" in self.data:
            self.drivers()
        elif "folder" in data:
            self.folder()
        elif "file" in data:
            self.file()
        elif "web" in data:
            self.web()

    def file(self): # dosya arama işlemi
        data = self.data.replace("file name ","").replace(" ","")
        speak("I started searcing for you, sir ,file searched   "+data,False)
        for files in Filop().searchfile(data):
            print((str(self.number)+" <<< found files >>> "+files).encode("utf-8"))
            self.number+=1
            self.files_.append(files)
        if self.files_!=[]:
            speak("the file search is over, sir")
            while True:
                data=record_data("open folder or file")
                if "open" in data:
                    try:
                        Open(urls,data)
                        break
                    except:
                        pass
                elif data != "":
                    lucy(record_data())
                    break

    def folder(self): # klasör arama işlemi
        if "all folder" in self.data:
            speak("I started searcing for you sir ,searcing all folders",sleep=False)
            for all_folder in Filop().isdir():
                print(all_folder,file = open("all_folder.txt","a"),flush = True)
            speak("I saved all the files for you in a text file name all_folder")
        elif "folder name" in self.data:
            data = self.data.replace("folder name","").replace(" ","")
            speak("I started searcing for you sir ,folder searched   "+data,False)
            for folder in Filop().searchfolder(data):
                print((str(self.number)+" <<< found folders >>> "+folder).encode("utf-8"))
                self.number+=1
                self.folders_.append(folder)
            if self.folders_!=[]:
                speak("the folder search is over, sir")
                while True:
                    data=record_data("open folder or file")
                    if "open" in data:
                        try:
                            Open(urls,data)
                            break
                        except ValueError as error:
                            print(error)
                    elif data != "":
                        lucy(record_data())
                        break

    def drivers(self): # sürücü arama işlemi
        drivers = [x for x in Filop().drivers()]
        speak("drivers on your computer,"+str(drivers))

    def web(self): # web arama işlemi
        if "on web" in self.data:
            self.data=self.data.replace("on web ","").replace(" ","+")
            url="https://www.yandex.com.tr/search/?text="+self.data
            urls=[]
            for url in General(url).urls():
                self.number+=1
                urls.append(url[0])
                print((str(self.number)+". <<< >>> "+url[1]).encode("utf-8"))
            while True:
                data = record_data("do you want open these urls, chose number or say sameting...")
                if "open" in data:
                    try:
                        Open(urls,data)
                        break
                    except:
                        pass
                else:
                    lucy(record_data())
                    break


class Open(): # uygulama klasör vs açma işlemleri
    def __init__(self,list_to_be_opened,data):
        self.data = data.replace("open ","")
        self.list = list_to_be_opened
        self.desktop_path=os.environ["HOMEDRIVE"]+os.environ["HOMEPATH"]+"\Desktop"
        if "driver" in self.data:
            for x in Filop().drivers(): # sürücüler ile eşleşme olursa açar
                for y in self.data.split():
                    y+=":\\"
                    if x == y:
                        self.dopen(x)
        elif "application" in self.data:
            for x in os.listdir(self.desktop_path): # masaüstünde bir program ismi ile
            # eşleşirse açar
                x=x.lower()
                for y in self.data.split():
                    y=y.lower()
                    if y in x:
                        self.path_open(self.desktop_path+"\\"+x,y)
        elif self.list != None: # arama -tarama işlemi bittikten sonra seçilen dosya açılır
            self.fof()

    def fof(self): # file or folder open
        data = self.data.replace(" ","")
        try:
            numb=int(data)
        except:
            numb = int(number[data])
        try:
            os.startfile(self.list[numb-1])
            try:
                title=General(self.list[numb-1]).title()
            except:
                title=self.list[numb-1]
            print(title.encode("utf-8"))
            speak(title+" , is opened , sir")
        except:
            speak("error opening file")

    def dopen(self,driver): # sürücülerden birini açmak isterse
        os.startfile(driver)
        speak(driver+ ", driver , is opened sir")

    def path_open(self,path,name): # yolu girilen dosya açılır
        os.startfile(path)
        print(path)
        speak(name+" is open , sir")

def speak(audioString,sleep=True): # bir yazıyı okutmak için
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    duration_voice=mutagen.File("audio.mp3").info.length
    print(duration_voice)
    os.system("audio.mp3")
    if sleep:
        time.sleep(duration_voice)

def record_data(explain="Say something!"): # dinleyip söylenini anlamak için
    r = speech.Recognizer()
    with speech.Microphone() as source:
        print(explain.encode("utf-8"))
        data = ""
        audio = r.listen(source)
        try:
            data = r.recognize_google(audio)
            print(r.recognize_google(audio).encode("utf-8"))
        except speech.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except speech.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return data.lower()

def lucy(data):
    if data in ["hey lucy","lucy"]:
        speak("yes sir")
        lucy(record_data())
    elif "what time is it" in data:
        speak(time.asctime(time.localtime(time.time())))
    elif "search" in data:
        Search(data)
    elif "open" in data:
        Open(None,data)
    elif "help" == data:
        help()
