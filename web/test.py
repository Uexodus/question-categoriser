import json
from database import QuestionDatabase, Category, Question, Paper, Subject

db = QuestionDatabase("sqlite:///questions.sqlite")

subject_name = "mathematics"
data_out = "question-data/data1.json" 


qu = db.session.query(Paper).filter_by(id=9).all()
    
print(list(qu))
db.session.commit()