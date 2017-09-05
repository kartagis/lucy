# asistan olaylarının döndüğü yer
import speech_recognition as speech
from gtts import gTTS
import os
import time
import mutagen
import re
from numbers import number
from filop import Filop
from abouturl import General,Youtube

class Search(): # arama işlemleri
    def __init__(self,data):
        self.data = data
        self.folders_=[]
        self.number=1
        self.files_=[]
        search_folder = re.search("^search (folder name .*|all folder|all folders)$",self.data)
        search_file = re.search("^search file name (.*)$",self.data)
        search_web = re.search("^search on web (.*)$",self.data)
        if re.search("^search (driver|drivers)$",self.data):
            self.drivers()
        elif search_folder != None:
            self.folder(search_folder.group(1))
        elif search_file != None :
            self.file(search_file.group(1))
        elif search_web != None:
            self.web(search_web.group(1))

    def file(self,file_name): # dosya arama işlemi
        speak("I started searcing for you, sir ,file searched   "+file_name,False)
        for files in Filop().searchfile(file_name):
            print((str(self.number)+" <<< found files >>> "+files).encode("utf-8"))
            self.number+=1
            self.files_.append(files)
        if self.files_!=[]:
            speak("the file search is over, sir")
            while True:
                data=record_data("open folder or file")
                num = re.search("^open ([0-9])$",data)
                if num != None:
                    try:
                        Open(self.files_,num.group(1))
                        break
                    except:
                        pass
                elif data != "":
                    lucy(record_data())
                    break

    def folder(self,search_folder): # klasör arama işlemi
        search_selection = re.search("folder name (.*)",search_folder)
        if search_selection == None:
            speak("I started searcing for you sir ,searcing all folders",sleep=False)
            for all_folder in Filop().isdir():
                print(all_folder,file = open("all_folder.txt","a"),flush = True)
            speak("I saved all the files for you in a text file name all_folder")
        elif search_selection != None:
            folder_name = search_selection.group(1)
            speak("I started searcing for you sir ,folder searched   "+folder_name,False)
            for folder in Filop().searchfolder(folder_name):
                print((str(self.number)+" <<< found folders >>> "+folder).encode("utf-8"))
                self.number+=1
                self.folders_.append(folder)
            if self.folders_!=[]:
                speak("the folder search is over, sir")
                while True:
                    data=record_data("open folder or file")
                    num = re.search("^open ([0-9])$",data)
                    if num != None:
                        try:
                            Open(self.folders_,num.group(1))
                            break
                        except:
                            pass
                    elif data != "":
                        lucy(record_data())
                        break

    def drivers(self): # sürücü arama işlemi
        drivers = [x for x in Filop().drivers()]
        speak("drivers on your computer,"+str(drivers))

    def web(self,search_web): # web arama işlemi
        search_web=search_web.replace(" ","+")
        url="https://www.yandex.com.tr/search/?text="+search_web
        urls=[]
        for url in General(url).urls():
            self.number+=1
            urls.append(url[0])
            print((str(self.number)+". <<< >>> "+url[1]).encode("utf-8"))
        while True:
            data = record_data("do you want open these urls, chose number or say sameting...")
            num = re.search("^open ([0-9])$",data)
            if num != None:
                try:
                    Open(urls,num.group(1))
                    break
                except:
                    pass
            elif data != "":
                lucy(record_data())
                break


class Open():
    "uygulama klasör vs açma işlemleri"
    def __init__(self,list_to_be_opened,data):
        self.data = data
        self.list = list_to_be_opened
        self.desktop_path=os.environ["HOMEDRIVE"]+os.environ["HOMEPATH"]+os.sep+"Desktop"
        driver = re.search("^open (.) (driver|drivers)$",self.data)
        application = re.search("^open (.*) (application|applications)$",self.data)
        if driver != None:
            self.dopen(driver.group(1)+":\\")
        elif application != None:
            self.open_application(application.group(1))
        elif self.list != None: # arama -tarama işlemi bittikten sonra seçilen dosya açılır
            self.fof()

    def fof(self): #
        "file or folder open"
        try:
            numb=int(self.data)
        except:
            numb = int(number[self.data])
        try:
            os.startfile(self.list[numb-1])
            try:
                title=General(self.list[numb-1]).title()
            except:
                title=self.list[numb-1]
            print(title.encode("utf-8"))
            speak(title+" , is opened sir")
        except:
            speak("error opening file")

    def dopen(self,driver):
        " sürücülerden birini veya bir kaçını açmak isterse "
        drivers = [d for d in Filop().drivers()]
        if driver in drivers:
            os.startfile(driver)
            speak(driver+ ", driver , is opened sir")
        else:
            speak(driver+" driver is not in your computer ")

    def open_application(self,application):
        "istenilen uygulama masaüstünde varsa çalıştırır"
        print(application)
        for x in os.listdir(self.desktop_path):
            x=x.lower()
            if application in x:
                os.startfile(self.desktop_path+"\\"+x)
                print(self.desktop_path+"\\"+x)
                speak(application+" is open , sir")

def speak(audioString,sleep=True):
    "bir yazıyları okutmak için"
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
        print("-"*30)
        print(explain.encode("utf-8"))
        print("-"*30)
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

def explain():
    cds="""
       # you can check or run with talking
       commands that can be executed by the program
       use as follow

      from assis import lucy,record_data
      lucy(record_data())

     - and you can speak

      example speak ;

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
    """
    return cds

def lucy(data):
    if re.search("what time is it|what time|time",data) != None:
        speak(time.asctime(time.localtime(time.time())))
    elif re.search("^search (driver|drivers|folder name .*|all folder|all folders|file name .*|on web .*)$",data) != None:
        Search(data)
    elif re.search("^open (. driver|drivers)|[0-9]|.* applications|.* application$",data) != None:
        Open(None,data)
    elif re.search("^help$",data) != None:
        print(explain())
