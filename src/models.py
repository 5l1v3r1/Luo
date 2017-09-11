from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
import settings

class SetLuo(settings.Base): # birden fazla kayıt yaptırabilir ler bu sayede kişilere özel davranır
    __tablename__ = 'setluo'
    id = Column(Integer, primary_key=True)
    name = Column(String) # name of luo , birden fazla ismi olabilir,her kullanıcı bir isim verir
    pwgn = Column(String) # person who give name,bu kişiyi tanıyıp onun verilerini açıp ona göre davranır onu tanır
    time = Column(DateTime, default=func.now()) # time you start using

class Questions(settings.Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question = Column(String) # question
    pwgn = Column(String) # person who use now
    time = Column(DateTime, default=func.now()) # time ask question



"""
bu modellerden sonra makine öğrenmesi için diğer modeller eklenecek
mesela pwgn bunun modelinde luo gördüğü duydugu bildiği herşeyi
kişilere göre saklayacak ve edindiği bilgiler dogrultusunda işlemler yapacak
"""

"dil seçme eklenecek vs"


settings.session()
