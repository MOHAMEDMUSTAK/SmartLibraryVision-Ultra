from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
engine = create_engine("sqlite:///library.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    shelf = Column(String)
    image_path = Column(String)

Base.metadata.create_all(engine)
