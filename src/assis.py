# asistan olaylarının döndüğü yer
import speech_recognition as speech
from gtts import gTTS
import os
import time
import mutagen
import re
from numbers_ import number
from filop import Filop
from abouturl import General
from time import gmtime, strftime

class Search(): # arama işlemleri
    def __init__(self,data):
        self.data = data
        self.folders_=[]
        self.number=1
        self.files_=[]
        search_folder = re.search("^search (folder name .*|all folder|all folders)$",self.data)
        search_file = re.search("^search (file name|file) (.*)$",self.data)
        search_web = re.search("^(search on web) (.*)$",self.data)
        if re.search("^search (driver|drivers)$",self.data):
            self.drivers()
        elif search_folder != None:
            self.folder(search_folder.group(1))
        elif search_file != None :
            self.file(search_file.group(2))
        elif search_web != None:
            self.web(search_web.group(1))

    def file(self,file_name): # dosya arama işlemi
        Lucy().talk("I started searcing for you, sir ,file searched   "+file_name,False)
        for files in Filop().searchfile(file_name):
            print((str(self.number)+"    "+files).encode("utf-8"))
            self.number+=1
            self.files_.append(files)
        if self.files_!=[]:
            data = Lucy().read(self.files_,talk = "the file search is over, sir")
            """talk de yazan metin söylendikten sonra isteğe bağlı files_ listesini okutuyorum istemez ise ne yapma istiyosa
            söylüyor bende söylenen veriyi alıp devam ediyorum"""
            if re.search("^open ([0-9])$",data) != None:
                Open(self.files_,num.group(1))
            #Lucy(Lucy().listen())

    def folder(self,search_folder): # klasör arama işlemi
        search_selection = re.search("folder name (.*)",search_folder)
        if search_selection == None:
            Lucy().talk("I started searcing for you sir ,searcing all folders",sleep=False)
            for all_folder in Filop().isdir():
                print(all_folder,file = open("all_folder.txt","a"),flush = True)
            Lucy().talk("I saved all the files for you in a text file name all_folder")
        elif search_selection != None:
            folder_name = search_selection.group(1)
            Lucy().talk("I started searcing for you sir ,folder searched   "+folder_name,False)
            for folder in Filop().searchfolder(folder_name):
                print((str(self.number)+"     "+folder).encode("utf-8"))
                self.number+=1
                self.folders_.append(folder)
            if self.folders_!=[]:
                data = Lucy().read(self.folders_,talk = "the folder search is over, sir")
                if re.search("^open ([0-9])$",data) != None:
                    Open(self.folders_,num.group(1))
                    #Lucy(Lucy().listen())

    def drivers(self): # sürücü arama işlemi
        drivers = [x for x in Filop().drivers()]
        Lucy().talk("drivers on your computer,"+str(drivers))

    def web(self,search_web): # web arama işlemi
        search_web=search_web.replace(" ","+")
        url="https://www.yandex.com.tr/search/?text="+search_web
        urls=[]
        names = []
        for url in General(url).urls():
            self.number+=1
            urls.append(url[0])
            names.append(url[1])
            print((str(self.number)+"    "+url[1]).encode("utf-8"))
        data = Lucy().read(names,talk = "the web search is over, sir")
        if re.search("^open ([0-9])$",data) != None:
            Open(urls,num.group(1))
        #Lucy(Lucy().listen())


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
            Lucy().talk(title+" , is opened sir")
        except:
            Lucy().talk("error opening file")

    def dopen(self,driver):
        " sürücülerden birini açmak isterse "
        drivers = [d for d in Filop().drivers()]
        if driver in drivers:
            os.startfile(driver)
            Lucy().talk(driver+ ", driver , is opened sir")
        else:
            Lucy().talk(driver+" driver is not in your computer ")

    def open_application(self,application):
        "istenilen uygulama masaüstünde varsa çalıştırır"
        print(application)
        for x in os.listdir(self.desktop_path):
            x=x.lower()
            if application in x:
                os.startfile(self.desktop_path+"\\"+x)
                print(self.desktop_path+"\\"+x)
                Lucy().talk(application+" is open , sir")


class Lucy():
    def __init__(self,data = None):
        "Bildiği şeyler ve diğer organlarına yönlendirmeleri - beyin ve omurilik"
        self.data = data
        if self.data != None:
            if re.search("what time is it|what time|time",self.data) != None:
                self.talk(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            elif re.search("^search (driver|drivers|folder name .*|all folder|all folders|file name .*|on web .*)$",self.data) != None:
                Search(self.data)
            elif re.search("^open (. driver|drivers)|[0-9]|.* applications|.* application$",self.data) != None:
                Open(None,self.data)
            elif re.search("^(help|help me|lucy help|lucy help me|hey lucy help me|hey lucy|hey lucy help)",self.data) != None:
                self.read(explain())

    def talk(self,audioString,sleep=True):
        "bu yazıları okutmak için - konuşmak"
        print("-"*30+"\n"+"preparing to read ;\n"+"-"*30)
        print(audioString.encode("utf-8"))
        tts = gTTS(text=audioString, lang='en')
        tts.save("audio.mp3")
        os.system("audio.mp3")
        duration_voice=mutagen.File("audio.mp3").info.length
        print(("-"*30+"\n"+"lucy will talk for {} seconds\n"+"-"*30).format(duration_voice))
        if sleep:
            time.sleep(duration_voice)

    def listen(self,explain="Say something!"):
        "dinleyip söylenini anlamak için - duymak"
        r = speech.Recognizer()
        with speech.Microphone() as source:
            print("-"*30)
            print(explain.encode("utf-8"))
            print("-"*30)
            data = ""
            audio = r.listen(source)
            try:
                data = r.recognize_google(audio)
                print(data.lower())
            except speech.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except speech.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return data.lower()

    def read(self,text,talk = False):
        " istenilen metni okutmak - konuşmak"
        """print yapılan verileri eğer okutmak isterse read this veya
        read gibi komutları vermesi bu fonksiyonun çalışması için yeter,
        ayrıca talk = False değeri print yapıldıktan sonra ekrandakileri okutmak için yapılır ,
        talk = True değeri ise talk değerine girilen metin önce okutulur daha sonra
         text değerine girilen metin isteğine göre okutulur burdaki amaç talk olarak
         çalışan yerlerden önceki büyük metinleride isterse okumasını sağlamaktır"""
        if type(text) == type(list(text)): # yani bir liste ise
            open_list = ""
            for i in text:
                if i == text[-1]:
                    open_list += i
                else:
                    open_list += i+","
            text = open_list
            if talk:
                Lucy().talk(talk)
            else:
                pass
        if talk == False:
            print(text)
        while True:
            data = Lucy().listen()
            if re.search("^(read this|read|yes read|yeah read|yes read this)",data) != None:
                Lucy().talk("yes sir,"+text,sleep = False)
                return data
            elif data !="":
                return data # eğer lazım olursa söylenen cümleyi kullanırım ,olmaz ise kullanmam

def explain():
    cds="""
       # you can check or run with talking

        commands that can be executed by the program
        ---------

         use as follow
         -----

         ```python
         from assis import Lucy
         Lucy(Lucy().listen())
         ```
        - and you can speak

         example speak ;
         ------
         + help
           - help me
           - lucy help
           - lucy help me
           - hey lucy help me
           - hey lucy
           - hey lucy help

         + you can learn the time
           - what time is it
           - what time
           - time

         + you can search
           - search drivers #to find the all drivers from pc
           - search folder name new file
           - search all folder # to find the all folder from pc
           - search file name readme
           - search on web python

         + you can open drivers of your computer
           - open d driver

         + you can run defined applications on your desktop
           - open google chrome application
           - open media player application

         + lucy can read the text on the screen
           - read this
           - read
           - yes read
           - yes read this
           - yeah read

         + lucy can open or run on the screen
           - open 3
           - open 5


       # you can check with commands instead of talking

       example ;
        ------
       ```python

       from assis import Lucy,Search

       Lucy("open d drivers")
       Lucy("search folder name python")
       Lucy("search drivers")
       Lucy("search file name django")
       Lucy("open chrome applications")
       Lucy("search on web face")
       Lucy("search on web python programming")

       while True:
           Lucy(Lucy().listen())

       Search("search driver")
       Search("search folder name python")
       Search("search file name python")
       Search("search all folder")

        ```
        """
    return cds
