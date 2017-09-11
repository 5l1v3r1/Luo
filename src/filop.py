#-*-coding:utf-8-*-
" filop --> file operations --> dosya işlemleri"
import os
from time import gmtime, strftime
import time
try:
    import settings
    from models import *
except Exception as error:
    print("I guess you started this module as Filop(True) ---",error)
    time.sleep(1)

os_name = os.name

class Help():
    """Bu yardım sınıfı SEARCH sınıfına yardım etmesi için yazıldı ve
     amacı girilen uzantılardaki tüm dosları ve klasörleri bulmaktır"""

    def __init__(self,driv):
        self.isdir=[] # bu bulunan klasör leri geçeci depoluyor
        self.isfile=[] # bu bulunan dosyaların geçesi depo listesidir
        self.driv=driv # girilen driver yani sürücü işte

    def folder(self):# girilen uzantının altındaki klasör lerin bbulur vemliste olarak verir
        try:
            for sea in os.listdir(self.driv):
                full_ex=os.path.join(self.driv,sea)
                if "windows" in full_ex.lower(): # burda amaç pc deki windows klasöründe arama yapmamasını sağlamak
                    pass
                else:
                    if os.path.isdir(full_ex) and full_ex not in self.isdir:
                        self.isdir.append(full_ex)
        except Exception as error:
            print(error)
        return self.isdir

    def file(self,type_=None):
        """
        girilen uzantının altındaki dosya ları bulup liste olarak verir
        type_=None ise tür araması yapmak istemiyordur
        """
        try:
            for sea in os.listdir(self.driv):
                full_ex=os.path.join(self.driv,sea)
                if "windows" in full_ex.lower(): # burda amaç pc deki windows klasöründe arama yapmamasını sağlamak
                    pass
                else:
                    if os.path.isfile(full_ex) and full_ex not in self.isfile:
                        # burada bulunan dosyanın eğer türü hakkında bir seçim yapılmış ise gereken işlemler burda yapılıyor
                        if type_!=None: # None değil ise dosya türü istiyordur
                            if list==type(type_): # liste olarak belirli türleri isteyebilir
                                for pat in type_:
                                    if full_ex.endswith("."+pat):
                                        self.isfile.append(full_ex)
                            elif str==type(type_):
                                if full_ex.endswith("."+type_):
                                    self.isfile.append(full_ex)
                                pass
                        elif type_==None: # tür araması yapmıyorum
                            self.isfile.append(full_ex) # ve girilen driv deki sürücülerinde ki klasörleri kaydediyoruz
        except Exception as error:
            print(error)
        return self.isfile

    def size(self,totaly=False):
        """
        normal çıktı verir liste veya dict değildir
        totaly false şu demek eğer bir klasörün içindeki dosyaların boyutlarını bayt çinsinden hesaplamış
        ve bunun kaç mb/gb oldugunu öğrenmek istiyorsan totaly=bulunan bayt miktarı girilmesi gerek yapmalısın
        """
        size_int=os.stat(self.driv).st_size # her dosyanın boyutunu alıyoruz
        size_str=str(size_int) # bir int bir de str kopya cıkartıyoruz
        if totaly!=False:
            size_int=totaly
            size_str=str(size_int)
        try:
            point=size_str[:size_str.index(".")] # burda nokta varmı diye bakıyoruz varsa konumunu aldık
        except:
            point=len(size_str) # yoksa toplam uzunlugunu aldık
        if size_int<1024:
            size=size_str[:point]+"/Bayt"
        elif size_int>1024 and size_int<1048576:
            size=str(size_int/1024)[:point]+"/KB"
        elif size_int>1048576 and size_int<1073741824:
            size=str(size_int/1048576)[:point]+"/MB"
        elif size_int<1073741824 and size_int<1099511627776:
            size=str(size_int/1073741824)[:point]+"/GB"
        elif size_int>1099511627776:
            size=str(size_int/1099511627776)[:point]+"/TB"
        return size,self.driv


class Search():
    " This class is PYTHON SEARCH ALGORİTHMA "
    def __init__(self,word,word_list):
        self.word=word.lower()
        self.match=[] # bu aranan kelime ile eşleşen sonuçları depolar
        self.word_list=word_list
        for word_l in self.word_list:
            word_l=word_l.lower()
            temp = os.path.split(word_l)[1]
            if self.word == temp and word_l not in self.match: # bu tam eşleşme olanları alıyor önce
                self.match.append(word_l)

            elif self.word in temp and word_l not in self.match:
                self.match.append(word_l)

            # bura da tam eşitlik olmasada girilen kelime nın harf sayısından yarısından fazla ile eşlesirse
            number=0
            while True:
                try:
                    if temp[number]==self.word[number] and word_l not in self.match:
                        number+=1
                    else:
                        if number>int(len(self.word)/2) and word_l not in self.match:
                            self.match.append(word_l)
                        break
                except IndexError:
                    break


class Filop():
    """ python dosya işlemleri, ana sınıf bu """
    def __init__(self,scan = False,year = 0,month = 0,day = 5):
        """scan false demek program baştan sona tüm pc yi taramak yerine daha önceden depolamış olduğu veritabanından
        bilgiyi alıp öyle arama yapacak,eğer daha önce kayıt etmemişse tarayıp kayıt edecek ve filop sınıfına girilmiş olanlar
        parametrelerdeki tarhi geçmiş ise son kayıt tarihi tekrar tarayıp depolayacak,
        eğer veri tabanı ile hiç uğraşmamak için veya yeni bir dosya arıyolar ise scan True yapılmalı"""
        self.scan = scan
        self.year = year
        self.month = month
        self.day = day
        try:
            self.s =  settings.session() # veri tabanına bağlanıyorum
        except Exception as error:
            if self.scan == False:
                print(("due to this error -- {} -- I have set as Filop(True)"),format(error))
                self.scan = True
                time.sleep(3)
        if self.scan == False: # eğer True olursa işlemler veritabanına bağlanmadan canlı olarak yapılır
            try:
                last_save = str(self.s.query(Folders).order_by(Folders.id)[0].time).split()[0].split("-")
                now = str(strftime("%Y-%m-%d", gmtime())).split("-")
                int(now[0])-int(last_save[0]) > self.year and int(now[1])-int(last_save[1])> self.month and int(now[2])-int(last_save[2]) > self.day
                scan_is = False
            except IndexError:
                scan_is = True
            if scan_is:
                print("""güncel veriler kayıt ediliyor bu yüzden biraz zaman alabilir,işlem bittikden sonra arama işlemleriniz daha hızlı olacaktır
                --
                The current data is saved so it can take some time and it will process faster after the process is finished""")
                try:
                    os.remove(settings.db_name) # eski db yi siliyorum
                except:
                    pass
                self.scan = True # bunu böyle yapıyorum ki anlık tarayıp verileri kayıt etsin
                for i in self.isdir(): # bütün klasörleri ekliyorum
                     data = Folders(path=i)
                     self.s.add(data)
                for i in self.searchfile(""): # bütün dosyaları ekliyorum
                    data = Files(path=i)
                    self.s.add(data)
                self.s.commit() # ve kayıt ettim
                self.scan = False # ve tekrar eski haline gelir

    def isdir(self): # pc deki tüm klasörleri bulan fonksiyon
        if self.scan == False:
            for isd in self.s.query(Folders).order_by(Folders.id):
                yield isd
        else:
            isdir=[] # bu pc de ki tüm klasör lerin listesidir
            for driving in self.drivers(): # burda sınıf çağırıldıgında bulunan sürücüleri alıyoruz
                for i in Help(driving).folder(): # ve her bulunan sürücüdeki klasörleri yardım sayesinde buraya alıyoruz
                    if i not in isdir:
                         isdir.append(i) # bulunan tüm klasör leri alıyorum
                         yield i
            for isd in isdir:# daha sonra sürekli genişleyecek olan isdir listesindeki klasörleri tekrar yardıma yollayıp pc deki
                for fo in Help(isd).folder(): # tüm klasörleri buluyoruz:
                    if fo not in isdir:
                        isdir.append(fo) # bulunan her klasörü genişlemesi için isdire ekliyoruz
                        yield fo

    def drivers(self): # ve pc de kullanılan sürücü yollarını buluyoruz
        extensions="qwertyuıopğüişlkjhgfdsazxcvbnmöç"+os.sep
        for ex in extensions:
            if os_name == "posix":
                try:
                    os.listdir(str(ex))
                    yield str(ex)
                except:
                    pass
            elif os_name == "nt":
                try:
                    os.listdir(str(ex)+":")
                    yield str(ex)+":"+os.sep
                except:
                    pass
        if os_name == "posix":
            for home in os.listdir(os.sep+"home"):  # linux home dizini
                yield os.sep+"home"+os.sep+home


    def searchfile(self,word,type_=None): # aranan kelime ile işlesen dosya isimlerini bulur
        if self.scan == False:
            for isd in self.s.query(Files).order_by(Files.id):
                # type_ olayı yok burda eklenmesi gerek
                isd_list = []# search de çalışabilmesi için liste yaptım
                isd = isd.path
                if type_!=None: # None değil ise dosya türü istiyordur
                    if list==type(type_): # liste olarak belirli türleri isteyebilir
                        for pat in type_:
                            if isd.endswith("."+pat):
                                isd_list.append(full_ex)
                    elif str==type(type_):
                        if isd.endswith("."+type_):
                            isd_list.append(isd)
                else:
                    isd_list.append(isd)
                for add in Search(word,isd_list).match:
                    yield add
        else:
            for isd in self.isdir() :
                for add in Search(word,Help(driv=isd).file(type_=type_)).match:
                    yield add

    def searchfolder(self,word): # aranan kelime mile eşleşen dosyaları bulur
        if self.scan == False:
            for isd in self.s.query(Folders).order_by(Folders.id):
                isd_list = []
                isd_list.append(isd.path)
                # type_ olayı yok burda eklenmesi gerek
                for add in Search(word,isd_list).match:
                    yield add
        else:
            for isd in self.isdir():
                for add in Search(word,Help(driv=isd).folder()).match: # burda bir kod ve işlem fazlalığı varmış gibi geliyor ama
                # kodu düzeltince sonuç alınmıyor anlamadım
                    yield add

    def open(self,path): # list or str girilen yoldaki dosya yı açar liste veya str olarak girilebilir
        if list==type(path):
            for pat in path:
                os.startfile(pat)
        else:
            os.startfile(path)

    def size(self,path):
        if list==type(path): # liste olarak girilmiş ise
            show=[]
            for pat in path:
                if os.path.isdir(pat): # klasör ise
                    total_size=0
                    for f in Help(driv=pat).file():
                        total_size+=os.stat(f).st_size
                    for fo in Help(driv=pat).folder(): # altındaki tüm klasörleri buluyoruz
                        for f in Help(driv=fo).file():
                            total_size+=os.stat(f).st_size
                    show.append(Help(driv=pat).size(totaly=total_size))
                else: # dosya ise
                    for pat in path:
                        try:
                            show.append(Help(driv=pat).size())
                        except:
                            pass
            return show
        elif str==type(path): # sadece bir tane str olarak girilmiş ise
            if os.path.isfile(path): # dosya ise
                return Help(driv=path).size()
            else: # klasör ise
                total_size=0
                show=[]
                for f in Help(driv=path).file():
                    total_size+=os.stat(f).st_size
                for fo in Help(driv=pat).folder(): # altındaki tüm klasörleri buluyoruz
                    for f in Help(driv=fo).file():
                        total_size+=os.stat(f).st_size
                show.append(Help(driv=pat).size(totaly=total_size))
                return show
        else:
            raise Exception("You should only use list or str")
