import os

import datetime

import sqlalchemy 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


from dotenv import load_dotenv

load_dotenv()
POSTGRES_USER = os.getenv('POSTGRES_USER',"postgres")
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD',"0596")
POSTGRES_DB = os.getenv('POSTGRES_DB',"postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST","5432")

DSN = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_HOST}/{POSTGRES_DB}"
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)

metadata = sqlalchemy.MetaData()
Base = declarative_base(metadata=metadata)

class Advertisement(Base):
    __tablename__ = "advertisement"

    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String,nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text,nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Float,nullable=False)
    author = sqlalchemy.Column(sqlalchemy.String,nullable=False)
    date_of_creation = sqlalchemy.Column(sqlalchemy.DateTime,nullable=False, default=datetime.datetime.utcnow)


    def dict(self):
        return{
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "price":self.price,
            "author":self.author,
            "date_of_creation":self.date_of_creation
            }

def connect_session(new,add=None):
    try:
        with Session() as sess:
            if add:
                sess.add(new)
            sess.commit()
            return "the transaction for the session has been completed"
    except Exception as error:
        sess.rollback()
        return error



def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Creating database")