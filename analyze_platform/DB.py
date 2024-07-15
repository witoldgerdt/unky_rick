from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from decouple import config

DATABASE_URL = config('DATABASE_URL')

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, Sequence('id_seq'), primary_key=True)

class Record(BaseModel):
    __tablename__ = 'records'
    column1 = Column(String(50))
    column2 = Column(String(50))

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()