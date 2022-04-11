from sqlalchemy import Column,String,Integer,Boolean
import threading
from sqlalchemy.orm.exc import NoResultFound

from bot import LOGGER
from bot.modules.sql import base,session

class Settings(base):
    __tablename__ = 'setting'
    id = Column(Integer, primary_key=True)
    contest=Column(Boolean,default=True,server_default='t')
    
    
    def __init__(self,contest=True):
        self.contest=contest
        
    def __repr__(self):
        return f'{self.id}'
        
Settings.__table__.create(checkfirst=True)
INSERTION_LOCK=threading.RLock()

def update_contest(mode)  :
    
    contest=session.query(Settings).first()
    if not contest:
        with INSERTION_LOCK:
            session.add(Settings(contest=mode))
            session.commit()            
    else:
        
        with INSERTION_LOCK:
            session.query(Settings).filter(Settings.id==1).update({Settings.contest:mode})
            session.commit()
            
def get_contest():
    try:
        contest=session.query(Settings).first()
        return contest.contest
    finally:
        session.close()