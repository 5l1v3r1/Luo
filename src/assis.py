#-*-coding:utf-8-*-
# asistan olaylarının döndüğü yer
import speech_recognition as speech
import os
import time
import re
from numbers_ import number
from filop import Filop
from abouturl import General
from time import gmtime, strftime
import pyttsx3
from google import search

fi = Filop(True) # gerçek zamanlı dosya taraması yapması için
r = speech.Recognizer()
os_name = os.name
os_sep = os.sep
os_environ = os.environ
desktop_path  = []
if os_name == "posix":
    for path in os.listdir(os_sep+"home"):
        desktop_path.append(os_sep+"home"+os_sep+path+"Desktop")
elif os_name == "nt":
    desktop_path.append(os_environ["HOMEDRIVE"]+os_environ["HOMEPATH"]+os_sep+"Desktop")


class Search(): # arama işlemleri
    def __init__(self,data):
        self.data = data
        self.folders_=[]
        self.number=1
        self.files_=[]
        search_folder = re.search("^search (folder name .*|all folder|all folders)$",self.data)
        search_file = re.search("^search (file name|file) (.*)$",self.data)
        search_web = re.search("^search on web (.*)$",self.data)
        if re.search("^search (driver|drivers)$",self.data):
            self.drivers()
        elif search_folder != None:
            self.folder(search_folder.group(1))
        elif search_file != None :
            self.file(search_file.group(2))
        elif search_web != None:
            self.web(search_web.group(1))

    def file(self,file_name): # dosya arama işlemi
        Lucy().talk("I started searcing for you, sir ,file searched   "+file_name)
        for files in fi.searchfile(file_name):
            print(str(self.number)+"    "+files)
            self.number+=1
            self.files_.append(files)
        if self.files_!=[]:
            data = Lucy().read(self.files_,talk = "the file search is over, sir")
            """talk de yazan metin söylendikten sonra isteğe bağlı files_ listesini okutuyorum istemez ise ne yapma istiyosa
            söylüyor bende söylenen veriyi alıp devam ediyorum"""
            num = re.search("^open ([0-9])$",data)
            if num != None:
                Open(self.files_,num.group(1))

    def folder(self,search_folder): # klasör arama işlemi
        search_selection = re.search("folder name (.*)",search_folder)
        if search_selection == None:
            Lucy().talk("I started searcing for you sir ,searcing all folders")
            with open("all_folder.txt","a") as file_:
                for all_folder in fi.isdir():
                    file_.write(all_folder)
            Lucy().talk("I saved all the files for you in a text file name all_folder")
        elif search_selection != None:
            folder_name = search_selection.group(1)
            Lucy().talk("I started searcing for you sir ,folder searched "+folder_name)
            for folder in fi.searchfolder(folder_name):
                print(str(self.number)+"     "+folder)
                self.number+=1
                self.folders_.append(folder)
            if self.folders_!=[]:
                data = Lucy().read(self.folders_,talk = "the folder search is over, sir")
                num = re.search("^open ([0-9].*)$",data)
                if num != None:
                    Open(self.folders_,num.group(1))
            else:
                Lucy().talk("the folder search is over, sir match not found")

    def drivers(self): # sürücü arama işlemi
        drivers = [x for x in fi.drivers()]
        Lucy().talk(("drivers on your computer,").split()+drivers)

    def web(self,search_web): # web arama işlemi
        urls = []
        self.number = 0
        for url in search(search_web, lang='es', stop=24):
            self.number+=1
            urls.append(url)
            print(str(self.number)+"    "+url)
        data = Lucy().read(urls,talk = "the web search is over, sir")
        num = re.search("^open ([0-9])$",data)
        if num != None:
            Open(urls,num.group(1))


class Open():
    "uygulama klasör vs açma işlemleri"
    def __init__(self,o_list,data):
        if os_name == "posix":
            Lucy().talk("This feature is only available for windows systems")
            return None
        elif os_name == "nt": # açma çalıştırma olayları sadece windows da var
            self.data = data
            self.o_list = o_list
            driver = re.search("^open (.) (driver|drivers)$",self.data)
            application = re.search("^open (.*) (application|applications)$",self.data)
            "hafızasında kalan en son şeyi yani ekranda gördüğü listeyi açtırmak isterse"
            if driver != None:
                self.dopen(driver.group(1)+":"+os_sep)
            elif application != None:
                self.open_application(application.group(1))
            elif o_list != None: # arama -tarama işlemi bittikten sonra seçilen dosya açılır
                self.fof()


    def fof(self): #
        "file or folder open"
        try:
            numb=int(self.data)
        except:
            numb = int(number[self.data])
        try:
            os.startfile(self.o_list[numb-1])
            try:
                title=General(self.o_list[numb-1]).title()
            except:
                title=self.o_list[numb-1]
            print(title)
            Lucy().talk(title+" , is opened sir")
        except:
            Lucy().talk("error opening file")

    def dopen(self,driver):
        " sürücülerden birini açmak isterse "
        drivers = [d for d in fi.drivers()]
        if driver in drivers:
            os.startfile(driver)
            Lucy().talk(driver+ ", driver , is opened sir")
        else:
            Lucy().talk(driver+" driver is not in your computer ")

    def open_application(self,application):
        "istenilen uygulama masaüstünde varsa çalıştırır"
        print(application)
        for x in os.listdir(desktop_path):
            x=x.lower()
            if application in x:
                os.startfile(desktop_path+"\\"+x)
                print(desktop_path+"\\"+x)
                Lucy().talk(application+" is open , sir")


class Lucy():
    def __init__(self,data = None):
        "Bildiği şeyler ve diğer organlarına yönlendirmeleri - beyin ve omurilik"
        self.data = data
        self.r = r
        if self.data != None:
            if re.search("^(what time is it|what time|time)",self.data) != None:
                self.talk(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            elif re.search("^search (driver|drivers|folder name .*|all folder|all folders|file name .*|on web .*)$",self.data) != None:
                Search(self.data)
            elif re.search("^open (. driver|drivers)|[0-9]|.* applications|.* application$",self.data) != None:
                Open(None,self.data)
            elif re.search("^(help|help me|lucy help|lucy help me|hey lucy help me|hey lucy|hey lucy help)",self.data) != None:
                self.read(explain())

    def talk(self,text):
        "bu yazıları okutmak için - konuşmak"
        print("-"*30+"\n"+"preparing to read ;\n"+"-"*30)
        if type(text) == list:
            m_text = ""
            for i in text:
                m_text += i+" "
            text = m_text
        elif type(text) == str:
            pass
        else:
            return
        print(text)
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait();

    def listen(self,explain="Say something!"):
        "dinleyip söylenini anlamak için - duymak"
        print("-"*30)
        print(explain)
        print("-"*30)
        with speech.Microphone() as source:
            while True:
                data = ""
                audio = self.r.listen(source)
                try:
                    data = self.r.recognize_google(audio)
                    print(data.lower())
                    break
                except speech.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except speech.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return data.lower()

    def read(self,text,talk = False):
        """ istenilen metni okutmak - konuşmak

        print yapılan verileri eğer okutmak isterse read this veya
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
                Lucy().talk("yes sir,"+text)
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
