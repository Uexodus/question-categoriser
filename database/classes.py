import re
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    questions = relationship("Question", back_populates="category")

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Category(name='{self.name})>"

class Subject(Base):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    questions = relationship("Question", back_populates="subject")

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Subject(name='{self.name})>"

class Paper(Base):
    __tablename__ = "paper"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    questions = relationship("Question", back_populates="paper")

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Paper(name='{self.name})>"


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    number = Column(Integer) 
    content = Column(String)
    raw = Column(String)
    paper_number = Column(Integer)    

    paper = relationship("Paper", back_populates="questions")
    category = relationship("Category", back_populates="questions")
    subject = relationship("Subject", back_populates="questions")

    paper_id = Column(Integer, ForeignKey('paper.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    
    

    def __init__(self, raw, number, paper_number, paper= None, category=None, subject=None) -> None:
        self.number = number
        self.raw = raw
        self.content = self.filter(self.raw)
        self.paper_number = paper_number
        self.paper = paper
        self.category = category
        self.subject = subject

    #filters out subquestions eg "(a) or (iv)" and images in the text eg (![](url_here))
    def filter(self, text):
        subquestion = "\([a-z]+\)\s"
        image = "!\[\]\(.*\)\s*"
        text = re.sub(subquestion, "", text)
        return re.sub(image, "", text)


    def __repr__(self) -> str:
        return f"<Question(id='{self.id}, number='{self.number}')>"


    