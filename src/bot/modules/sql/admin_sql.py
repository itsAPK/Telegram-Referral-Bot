from sqlalchemy import Column, Integer, String,Date,Text,DateTime,BigInteger,Float,Boolean,func
import datetime 
import hashlib
from bot import LOGGER
import threading
from sqlalchemy.orm.exc import NoResultFound

from bot.modules.sql import session,base

class Admin(base):
    __tablename__='admin'
    id=Column(Integer,primary_key=True)
    chat_id=Column(BigInteger)
    
    def __init__(self,chat_id):
        self.chat_id=chat_id
    
    def __str__(self):
        return f"{self.chat_id}"

Admin.__table__.create(checkfirst=True)
LOCK=threading.RLock()
    
def add_admin(chat_id):
    with LOCK:
        session.add(Admin(chat_id=chat_id))
        session.commit()
        
def get_admins():
    try:
        return [admin.chat_id for admin in session.query(Admin).all() ]
    finally:
        session.close()
        
        
        