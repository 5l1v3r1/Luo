#-*-coding:utf-8-*- 
import requests
import re
import socket
from bs4 import BeautifulSoup

# not text ve string işlemleri tam çalışmıyor galiba
class General(): # girilen adres ile igili genel bilgi verir
    def __init__(self,url):
        try:
            self.ip=socket.gethostbyname(url_socket)
        except:
            self.ip="Error - please  enter the wep address like this www.facebook.com"
        get_=requests.get(url) # burada girilen url de ki html kısmını alıyoruz
        self.soup=BeautifulSoup(get_.content,"html.parser") # ve burda diğer tüm işlemleri yapmak için html yi bu sınıfa veriyoruz
    def head(self):
        return self.soup.head # head kısmını verir

    def body(self):
        return self.soup.body # body kısmını verir
        #self.keywords=re.search("<meta content=.*keywords",str(self.head.find("meta"))).group()
        #self.description=re.search("<meta content=.*description",str(self.head.find("meta"))).group()
    def title(self):
        return self.soup.title.string # başlık bilgisi

    def prettify(self):
        return self.soup.prettify() # tüm html'i güzelleştirerek verir

    def wholetext(self,tag=None):
        if tag==None:
            return self.soup.get_text() # html'de bulunan tüm metni verir
        else:
            return self.soup.get_text(tag)

    def urls(self,tag1="a",tag2="href"):
        for f in self.soup.find_all(tag1): # ana sayfadaki tüm url adreslerini bulur
            text=f.get_text()
            f=f.get(tag2) # f bulunan web adresidir
            try:
                if f[0:1]=="/":
                    if f[0:2]=="//":
                        if url[0:5]=="https":
                            yield "https"+f,text
                        elif url[0:4]=="http":
                            yield "http"+f,text
                        else:
                            yield f,text
                    else:
                        yield url+f,text
                elif f[0:4]=="http":
                    yield f,text
            except:
                pass

    def img(self,tag1="img",tag2="src"): # girilen url adresinde bulunan  img adresleri ni verir
        for i in self.urls(self,tag1="a",tag2="href"):
            yield i

    def alltag(self): # tüm tagları verir
        for tag in self.soup.find_all(True):
            yield tag.name

    def table(self):
        self.table=self.soup.table

class Youtube():
    def __init__(self,url,type_=None):
        import pafy
        video=pafy.new(url)
        self.title=video.title
        self.rating=video.rating
        self.viewcount=video.viewcount
        self.author=video.author
        self.length=video.length
        self.duration=video.duration
        self.likes=video.likes
        self.dislikes=video.dislikes
        self.description=video.description
        if type_==None:
            self.besturl=video.getbest(preftype="mp4").url
        else:
            self.besturl=video.getbest(preftype=type_).url
