from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
import settings

class Folders(settings.Base):
    __tablename__ = 'folders'
    id = Column(Integer, primary_key=True)
    path = Column(String)
    time = Column(DateTime, default=func.now())

class Files(settings.Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    path = Column(String)
    time = Column(DateTime, default=func.now())

settings.session()
