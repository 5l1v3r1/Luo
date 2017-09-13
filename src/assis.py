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
import random
from google import search
from colorama import Fore
from  kalbur import kelimelerine_ayir as k_a

# Yazıları renklendirmek için colors sözlüğü eklendi: 11/10/2017: Fexyler

colors = {
    "":        "",
    "red":     Fore.RED,
    "cyan":    Fore.CYAN,
    "blue":    Fore.BLUE,
    "green":   Fore.GREEN,
    "white":   Fore.WHITE,
    "yellow":  Fore.YELLOW,
    "magenta": Fore.MAGENTA
}

# Kullanıcıyı yazılar hakkında bilgilendirmek için types sözlüğü eklendi: 11/10/2017: Fexyler
types = {"info" : "[INFO] ", "error" : "[ERROR] ","heard" : "[HEARD] ","search" : "[SEARCH] ","ask" : "[ASK] "}


class Settings():
    "luo için gereken ayarların sınıfıdır bütün ayarlar buradan yapılacaktır"
    def __init__(self):
        self.fi = Filop(True) # gerçek zamanlı dosya taraması yapması için/db ye ihtiyac duymaması için true
        self.r = speech.Recognizer() # bağlanıyor dinlemek için
        self.talk_engine = pyttsx3.init()
        self.os_name = os.name
        self.os_sep = os.sep
        self.os_environ = os.environ
        self.desktop_path  = [] # masaüstü yol adresi
        if self.os_name == "posix":
            for path in os.listdir(self.os_sep+"home"):
                self.desktop_path.append(self.os_sep+"home"+self.os_sep+path+"Desktop")
        elif self.os_name == "nt":
            self.desktop_path.append(self.os_environ["HOMEDRIVE"]+self.os_environ["HOMEPATH"]+self.os_sep+"Desktop")
            print(self.desktop_path)

set_luo = Settings()

class Search(): # arama işlemleri
    def __init__(self,data):
        self.data = data
        self.folders_= []
        self.number = 1
        self.files_= []
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
        Luo().talk("I started searcing for you, sir ,file searched   "+file_name)
        for files in set_luo.fi.searchfile(file_name):
            Luo().luoprint(str(self.number)+"    "+files,"info","blue")
            self.number+=1
            self.files_.append(files)
        if self.files_!=[]:
            data = Luo().read(self.files_,talk = "the file search is over, sir")
            """talk de yazan metin söylendikten sonra isteğe bağlı files_ listesini okutuyorum istemez ise ne yapma istiyosa
            söylüyor bende söylenen veriyi alıp devam ediyorum"""
            num = re.search("^open ([0-9])$",data)
            if num != None:
                Open(self.files_,num.group(1))

    def folder(self,search_folder): # klasör arama işlemi
        search_selection = re.search("folder name (.*)",search_folder)
        if search_selection == None:
            Luo().talk("I started searcing for you sir ,searcing all folders")
            with open("all_folder.txt","a") as file_:
                for all_folder in fi.isdir():
                    file_.write(all_folder)
            Luo().talk("I saved all the files for you in a text file name all_folder")
        elif search_selection != None:
            folder_name = search_selection.group(1)
            Luo().talk("I started searcing for you sir ,folder searched "+folder_name)
            for folder in set_luo.fi.searchfolder(folder_name):
                Luo().luoprint(str(self.number)+"     "+folder,"info","blue")
                self.number+=1
                self.folders_.append(folder)
            if self.folders_!=[]:
                data = Luo().read(self.folders_,talk = "the folder search is over, sir")
                num = re.search("^open ([0-9].*)$",data)
                if num != None:
                    Open(self.folders_,num.group(1))
            else:
                Luo().talk("the folder search is over, sir match not found")

    def drivers(self): # sürücü arama işlemi
        drivers = [x for x in set_luo.fi.drivers()]
        Luo().talk(("drivers on your computer,").split()+drivers)

    def web(self,search_web): # web arama işlemi
        urls = []
        self.number = 0
        for url in search(search_web, lang='es', stop=24):
            self.number+=1
            urls.append(url)
            Luo().luoprint(str(self.number)+" - "+url,"search","magenta")
        data = Luo().read(urls,talk = "the web search is over, sir")
        num = re.search("^open ([0-9])$",data)
        if num != None:
            Open(urls,num.group(1))


class Open():
    "uygulama klasör vs açma işlemleri"
    def __init__(self,o_list,data):
        if set_luo.os_name == "posix":
            Luo().talk("This feature is only available for windows systems")
            return None
        elif set_luo.os_name == "nt": # açma çalıştırma olayları sadece windows da var
            self.data = data
            self.o_list = o_list
            driver = re.search("^open (.) (driver|drivers)$",self.data)
            application = re.search("^open (.*) (application|applications)$",self.data)
            "hafızasında kalan en son şeyi yani ekranda gördüğü listeyi açtırmak isterse"
            if driver != None:
                self.dopen(driver.group(1)+":"+set_luo.os_sep)
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
            luoprint(title)
            Luo().talk(title+" , is opened sir")
        except:
            Luo().talk("error opening file")

    def dopen(self,driver):
        " sürücülerden birini açmak isterse "
        drivers = [d for d in set_luo.fi.drivers()]
        if driver in drivers:
            os.startfile(driver)
            Luo().talk(driver+ ", driver , is opened sir")
        else:
            Luo().talk(driver+" driver is not in your computer ")

    def open_application(self,application):
        "istenilen uygulama masaüstünde varsa çalıştırır"
        for path in set_luo.desktop_path:
            for x in os.listdir(path):
                x=x.lower()
                if application in x:
                    os.startfile(path+"\\"+x)
                    Luo().talk(application+" is open , sir")


class Luo():

    def __init__(self,data = None):

        "Bildiği şeyler ve diğer organlarına yönlendirmeleri - beyin ve omurilik"
        self.data = data
        self.r = set_luo.r

        if self.data != None:
            if re.search("^(what time is it|what time|time)", self.data) != None:
                self.talk(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

            elif re.search("^search (driver|drivers|folder name .*|all folder|all folders|file name .*|on web .*)$",self.data) != None:
                Search(self.data)

            elif re.search("^open (. driver|drivers)|[0-9]|.* applications|.* application$",self.data) != None:
                Open(None,self.data)

            elif re.search("^(help|help me)",self.data) != None:
                self.read(explain())

            # Luo().call(self.data)
    def luoprint(self,text,type=None,color=""):
        if color=="random":
            color = random.choice(colors.keys())
        text = colors[color] + types[type] + text
        print text

    def talk(self,text):

        "bu yazıları okutmak için - konuşmak"
        Luo().luoprint("-"*30+"\n"+"preparing to read ;\n"+"-"*30,"info","random")

        if type(text) == list:
            m_text = ""

            for i in text:
                m_text += i+" "
            text = m_text
        elif type(text) == str:

            pass
        else:

            return
        Luo().luoprint(text,"info","random")
        set_luo.talk_engine.say(text)
        set_luo.talk_engine.runAndWait()

    def listen(self,explain="Say something!"):

        "dinleyip söylenini anlamak için - duymak"
        a = 0
        Luo().luoprint(explain,"info","random")
        self.talk(explain)
        with speech.Microphone() as source:
            if a == 0:
                if os.name == "posix":
                    os.system("clear")
                elif os.name =="nt":
                    os.system("cls")
                a = a + 1

            while True:

                data = ""
                audio = self.r.listen(source)
                try:

                    data = self.r.recognize_google(audio)
                    Luo().luoprint(data.lower())
                    break

                except speech.UnknownValueError:

                    Luo().luoprint("Google Speech Recognition could not understand audio","error","red")
                except speech.RequestError as e:

                    Luo().luoprint("Could not request results from Google Speech Recognition service; {0}".format(e),"info","red")

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

                Luo().talk(talk)
            else:

                pass
        if talk == False:

            Luo().luoprint(text,"info","random")
        while True:

            data = Luo().listen()
            if re.search("^(read this|read|yes read|yeah read|yes read this)",data) != None:

                Luo().talk("yes sir,"+text)
                return data
            elif data !="":

                return data # eğer lazım olursa söylenen cümleyi kullanırım ,olmaz ise kullanmam

    def call(self,data):
        # Bu fonksiyon kullanıcının isteklerini yerine getirmeyi amaçlar 12.09.2017 : Fexyler
        data = k_a.kelimelerine_ayir(data)
        wordlist = ['help','time','search','file','driver','web','read']
        if wordlist[0] in data:
            Luo().read(explain())
        elif wordlist[1] in data:
            Luo().luoprint(strftime("%Y-%m-%d %H:%M:%S", gmtime()),"info","random")
        elif wordlist[2] in data and wordlist[3] in data:
            # this

def explain():
    cds="""
         ```python
         from assis import Luo
         Luo(Luo().listen())
         ```
        - and you can speak

         example speak ;
         ------
         + help
           - help
           - help me

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

         + Luo can read the text on the screen
           - read this
           - read
           - yes read
           - yes read this
           - yeah read

       if os.name == "nt": # you can run this commands

         + you can open drivers of your computer
           - open d driver

         + you can run defined applications on your desktop
           - open google chrome application
           - open media player application

         + Luo can open or run on the screen
           - open 3
           - open 5


       # you can check with commands instead of talking

       example ;
        ------
       ```python

       from assis import Luo,Search
       import os
       while True:
           Luo(Luo().listen())
       # or

       Luo("open d drivers")
       Luo("search folder name python")
       Luo("search drivers")
       Luo("search file name django")
       Luo("search on web face")
       Luo("search on web python programming")
       Search("search driver")
       Search("search all folder")
       Luo().talk("hello everyone")
       data = Luo().listen("can i help yoo ?")
       data = Luo().listen()
       if os.name == "nt":
         Luo("open chrome applications")
       # to read text on the screen
       read = Luo().read("read this messages .")
       # before print(read this messages)
       # and
       # if it says yes read this
       # after
       # Luo talk = read this messages and return this data
       # does not say yes read this and return this data
       """
    return cds

