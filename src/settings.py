from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_name = "db/filop.db"
Base = declarative_base()
def session(db_name = db_name):
    engine = create_engine('sqlite:///{}'.format(db_name))
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
    return session()
