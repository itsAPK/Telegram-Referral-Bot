from sqlalchemy import Column,String,Integer
import threading
from sqlalchemy.orm.exc import NoResultFound

from bot import LOGGER
from bot.modules.sql import base,session



class Shill(base): 
    __tablename__ = 'shill'
    id = Column(Integer, primary_key=True)
    shill1=Column(String)
    shill2=Column(String)
    shill3=Column(String)

    def __init__(self,shill1=None,shill2=None,shill3=None):
        self.shill1=shill1
        self.shill2=shill2
        self.shill3=shill3
        
class Welcome(base):
    __tablename__ = 'welcome'
    id = Column(Integer, primary_key=True)
    text=Column(String)
    image=Column(String)
        
    def __init__(self,text=None,image=None):
        self.text=text
        self.image=image
        

Shill.__table__.create(checkfirst=True)
Welcome.__table__.create(checkfirst=True)

WELCOME_LOCK=threading.RLock()
LOCK=threading.RLock()    

def add_welcome_text(text):
    if not session.query(Welcome).first():
        with WELCOME_LOCK :
            session.add(Welcome(text=text))
            session.commit()
    else:
        with WELCOME_LOCK:
            session.query(Welcome).filter(Welcome.id==1).update({Welcome.text : text})
            session.commit() 

def add_welcome_image(link):
    if not session.query(Welcome).first():
        with WELCOME_LOCK :
            session.add(Welcome(image=link))
            session.commit()
    else:
        with WELCOME_LOCK :
            session.query(Welcome).filter(Welcome.id==1).update({Welcome.image : link})
            session.commit() 
    
def get_welcome():
    return session.query(Welcome).filter(Welcome.id==1).first()
        
def add_shill1(text):
    if not session.query(Shill).first():
        with LOCK :
            session.add(Shill(shill1=text))
            session.commit()
    else:
        with LOCK :
            session.query(Shill).filter(Shill.id==1).update({Shill.shill1 : text})
            session.commit()

def add_shill2(text):
    if not session.query(Shill).first():
        with LOCK :
            session.add(Shill(shill2=text))
            session.commit()
    else:
        with LOCK :
            session.query(Shill).filter(Shill.id==1).update({Shill.shill2 : text})
            session.commit()
            
def add_shill3(text):
    if not session.query(Shill).first():
        with LOCK :
            session.add(Shill(shill3=text))
            session.commit()
    else:
        with LOCK :
            session.query(Shill).filter(Shill.id==1).update({Shill.shill3 : text})
            session.commit()
            
def get_shill():
    try :
        return session.query(Shill).first()
    finally:
        session.close()