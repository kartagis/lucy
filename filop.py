" filop --> file operations --> dosya işlemleri"
import os

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
        except PermissionError:
            pass
        except FileNotFoundError:
            pass
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
                            if type(list(type_))==type(type_): # liste olarak belirli türleri isteyebilir
                                for pat in type_:
                                    if full_ex.endswith("."+pat):
                                        self.isfile.append(full_ex)
                            elif type(str(type_))==type(type_):
                                if full_ex.endswith("."+type_):
                                    self.isfile.append(full_ex)
                                pass
                        elif type_==None: # tür araması yapmıyorum
                            self.isfile.append(full_ex) # ve girilen driv deki sürücülerinde ki klasörleri kaydediyoruz
        except PermissionError:
            pass
        except FileNotFoundError:
            pass
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
    def __init__(self):
        pass

    def isdir(self): # pc deki tüm klasörleri bulan fonksiyon
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
        extensions="qwertyuıopğüişlkjhgfdsazxcvbnmöç/"
        for ex in extensions:
            try:
                os.listdir(str(ex)+":")
                yield str(ex)+":"+os.sep
            except:
                pass

    def searchfile(self,word,type_=None): # aranan kelime ile işlesen dosya isimlerini bulur liste olarak verir
        for isd in self.isdir() :
            for add in Search(word,Help(driv=isd).file(type_=type_)).match:
                yield add

    def searchfolder(self,word): # aranan kelime mile eşleşen dosyaları bulur ve liste olarak verir
        for isd in self.isdir():
            for add in Search(word,Help(driv=isd).folder()).match: # burda bir kod ve işlem fazlalığı varmış gibi geliyor ama
            # kodu düzeltince sonuç alınmıyor anlamadım
                yield add

    def open(self,path): # list or str girilen yoldaki dosya yı açar liste veya str olarak girilebilir
        liste=[]
        if type(liste)==type(path):
            for pat in path:
                os.startfile(pat)
        else:
            os.startfile(path)

    def size(self,path):
        if type(list(path))==type(path): # liste olarak girilmiş ise
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
        elif type(str(path))==type(path): # sadece bir tane str olarak girilmiş ise
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
            return "You should only use list or str" # buraya düzgün bir hata olayı yap
