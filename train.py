#ai training 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer

#my own packages
from mathpix import Mathpix
from questiongather import parse_questions
from database import QuestionDatabase, Category, Question, Paper, Subject

#input pdf
question_paper = r"question-data\pastpapers\N5MathematicsSpecimenALL.pdf"

#output text folder
output_folder = "question-data/text"


api = Mathpix("jamie.4dice@gmail.com" , "8*C.7.HkK77gyFe")

#converts pdf to text
out_file = api.convert_pdf(question_paper, output_folder)

#gathers questions from outputted text document
with open(out_file) as file:
    questions = parse_questions(file)


subject_name = "mathematics"
paper_name = Mathpix.get_filename(question_paper)

#loads up the database
db = QuestionDatabase("sqlite:///questions.sqlite")


#creates Subject and Paper records for the specified names if they don't exist already.
subject = db.get(Subject(subject_name), name=subject_name)
paper = db.get(Paper(paper_name), name=paper_name)

#creates knn model
model = KNeighborsClassifier(n_neighbors=1)

#creates a vectorizer which turns words into plot points so the nearest result can be found
vectorizer = CountVectorizer()

for question in questions:
    
    question_exists = db.exists(Question, number=question.number, paper=paper, paper_number=question.paper_number)

    if question_exists:
        continue
        
    
    
    #gets all the questions and trains the ai with them
    data = []
    labels = []
    for question_data in db.session.query(Question).all():
        data.append(question_data.content)

        labels.append(question_data.category.name)


    X = vectorizer.fit_transform(data)
    model.fit(X, labels)
    
    
    print(question.number, question.content)
    print(model.predict(vectorizer.transform([question.content])))


    
    category_name = input("Enter question type: \n").lower()
    print("\n")



    category_name = category_name.strip()

    category = db.get(Category(category_name), name=category_name)
 
    db.session.add(question)
    question.subject = subject
    question.paper = paper
    question.category = category


    
    db.session.commit()

