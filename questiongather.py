
from io import TextIOWrapper
import json
import re
from database import Question



def parse_questions(file: TextIOWrapper) -> list[Question]:
    questionregex = "\s*\d{1,2}\.\s"
    questionno_regex = "\d{1,2}"
    


    text = ""

    for line in file.readlines():
        continued = re.findall("\(continued\)", line)
        


        if not continued and not re.findall(r"\\section\{.*\}", line) :
            text += line

    



    #gets all occurances of question numbers in the text file eg ("1.", "2.", "3.", etc)
    results = list(re.finditer(questionregex, text))
    




    #Stop occurances of sentences ending with a number followed by a fullstop eg (..the 1 + 6.) being picked up as questions
    for i, result in enumerate(results):
        #gets the current question number eg (3)
        question_number = int(re.findall(questionno_regex, result.group())[0])

        #gets the previous question number eg (2)
        last_question_number = int(re.findall(questionno_regex, results[i - 1].group())[0])

    
    

        #if the current question number is less than the last question number and doesn't equal 1, delete the current number from the list
        #or if the absolute difference between the two numbers is greater than 2, delete the current number from the list
        if i != 0 and question_number != 1 and (question_number < last_question_number or abs(question_number - last_question_number) > 1):

            print(question_number, "deleted")
            del results[i]


    questions = []


    #math tests include two papers, paper 1 (non calculator) and paper 2 (calculator)
    paper_number = 1

    for i, result in enumerate(results):
        
        #transforms the question match into an integer eg (1. -> 1)
        question_number = int(re.findall(questionno_regex, result.group())[0])




        
        #gets the end of the match, which is also where the content of the question starts
        start = result.end()

        #if the current item isn't the last item in the list
        if i != len(results) - 1:

            #set the question to the end of the current match to the start of the next match eg ("1."...question..."2.")
            question = text[start:results[i+1].start()]

        else:

            #if its the last question in the list, set the question to the end of the current match to the end of the file
            question = text[start::]

        
        
        #if the current question number is less then the last question number, it means that the question is part of paper 2.
        if questions and question_number < questions[-1].number:

            paper_number += 1

        #deletes any random whitespace characters around the question
        question = question.strip()
        
        
        #creates a "Question" class using the gathered data and adds it to list.
        questions.append(Question(question, question_number,  paper_number))

    return questions


    