from sqlalchemy import Column, Integer, String,Date,Text,DateTime,BigInteger,Float,Boolean,func
import datetime 
import hashlib
from bot import LOGGER
import threading
from sqlalchemy.orm.exc import NoResultFound

from bot.modules.sql import session,base



class User(base): 
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    first_name= Column(String)
    last_name=Column(String)
    username = Column(String)
    score=Column(Integer,default=0)
    refferal=Column(Integer,default=0)
    invalid_ref=Column(Integer,default=0)
    refferal_id=Column(Integer)
    joined=Column(Date,default=datetime.date.today())
    wallet=Column(String)
    
    def __init__(self,chat_id,first_name,last_name,username,refferal=0,invalid_ref=0,refferal_id=None,score=0,wallet=None):
        self.score=score
        self.chat_id=chat_id
        self.first_name=first_name
        self.last_name=last_name
        self.username=username
        self.refferal=refferal
        self.invalid_ref=invalid_ref
        self.refferal_id=refferal_id
        self.wallet=wallet
        
    def __repr__(self):
        return self.chat_id
        
User.__table__.create(checkfirst=True)

LOCK=threading.RLock()

def add_user(message):
        
        user=session.query(User).filter(User.chat_id == message.chat.id).all()
        first_name = message.chat.first_name
        last_name = message.chat.last_name
        username = message.chat.username
        chat_id = message.chat.id
        
        if first_name == None:
            first_name = 'None'
        if last_name == None:
            last_name = 'None'
        if username == None:
            username = 'None'
        if chat_id == None:
            chat_id = 'None'
        with LOCK:
            if not len(user):
                if message.text[7:] == '':
                    session.add(User(chat_id=chat_id,username=username,first_name=first_name,last_name=last_name))
                    session.commit()
                else:
                    session.add(User(chat_id=chat_id,username=username,first_name=first_name,last_name=last_name,refferal_id=message.text[7:]))
                    session.commit()
                LOGGER.info('New User : chat_id {} username {}'.format(chat_id,username))
            if len(user):
                session.query(User).filter(User.chat_id == message.chat.id).update({ 
                    User.first_name:first_name,
                    User.last_name:last_name,
                    User.username:username ,
                    })
                session.commit()

def get_users_id():
    return [user.chat_id for user in session.query(User).all()]

def add_referral(chat_id):
    LOGGER.info(f"Updating Score of {chat_id}")
    with LOCK:
        
        session.query(User).filter(User.chat_id==chat_id).update({User.refferal : User.refferal+1,User.score : User.score+1})
        session.commit()
        
def get_user_data(chat_id):
    try:
        LOGGER.info(f"Getting data of {chat_id}")
        return session.query(User).filter(User.chat_id==chat_id).first()
    finally:
        session.close()
        
        
def add_invalid_ref(chat_id):
    with LOCK:
        session.query(User).filter(User.chat_id==chat_id).update({User.invalid_ref: User.invalid_ref + 1,User.score : User.score -1})
        session.commit()
        
        
def get_rank(chat_id):
    subquery=session.query(User,func.rank().over(order_by=User.score.desc()).label('rank')).subquery()
    query=session.query(subquery).filter(User.chat_id==chat_id)
    return query.filter_by(chat_id=chat_id).first().rank

def get_top_usrs():
    users=session.query(User).order_by(User.score.desc()).limit(100).all()
    i=1
    data=''
    for user in users:
        if user.username =='None':
            data+=f"{i}. <a href='tg://user?id={user.chat_id}'>{user.first_name}</a> ({user.score})\n"
        else:
            data+=f"{i}. @{user.username} ({user.score})\n"
        i=i+1
    return data
    
def  get_total_user_count():
    return session.query(User).count()

def get_referral_users_count():
    return session.query(User).filter(User.refferal_id != None).count()

def get_new_user_count():
    return session.query(User).filter(User.joined == datetime.date.today()).count()

def get_new_referral_user():
    return session.query(User).filter(User.refferal_id != None,User.joined == datetime.date.today()).count()

def get_all():
    return session.query(User).all()

def reset_score():
    session.query(User).update({User.score:0})
    session.commit()
    
def set_user_wallet(chat_id,address):
    with LOCK:
        session.query(User).filter(User.chat_id==chat_id).update({User.wallet:address})
        session.commit()