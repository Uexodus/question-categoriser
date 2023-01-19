from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .classes import *

class QuestionDatabase:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self.engine  = create_engine(database_url)

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

        Base.metadata.create_all(self.engine)


    #checks if record with certain values exists in a table
    def exists(self, table, **kwargs):

        return self.session.query(table).filter_by(**kwargs).first()


    #adds a new record to a table if its isn't already added
    def get(self, new_obj, **kwargs):
        table = new_obj.__class__

        obj = self.exists(table, **kwargs)
        if not obj:
            self.session.add(new_obj)
            return new_obj

        return obj

    

        

    

