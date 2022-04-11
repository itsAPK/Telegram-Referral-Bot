from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session
from bot import DATABASE_URI



def start() -> scoped_session:
    
    engine=create_engine(DATABASE_URI)
    base.metadata.bind=engine
    base.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine,autoflush=False))
    
base=declarative_base()
session=start()