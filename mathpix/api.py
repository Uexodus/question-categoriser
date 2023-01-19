import re
from time import sleep
import requests
from PyPDF2 import PdfWriter, PdfReader

API_URL = "https://api.mathpix.com/v1"


class Mathpix:
    def __init__(self, email, password) -> None:
        #creates a requests session which stores login cookies and other session data.
        self.session = requests.Session() 
        
        #sends data to the server, attemping to login with the given email and password.
        res = self.session.post(f"{API_URL}/user/login", json={"email":email,"password":password})

        #raises an error if login information is incorrect.
        if res.status_code != 200:
            raise ValueError("Invalid username/password.")

    @staticmethod
    def get_filename(path: str):
        return re.findall("([^\\\/]+)\.\w+$", path)[0]

    def create_question_only_pdf(self, pdf_path):
        #regex that matches each question in the pdf
        questionregex = "\d{1,2}\. "

        #for pdf reading
        reader = PdfReader(pdf_path)

        #for pdf creation
        writer = PdfWriter()

        #goes through each page in the pdf
        for page in reader.pages:

            text = page.extract_text()

            #returns a list of matches for the questionregex
            results = list(re.finditer(questionregex, text))


            # if the page has any results, add it to the pdf creater
            if len(results) > 0:
                writer.add_page(page)

        #overwrites the inputed pdf with one that only contains pages with questions in it
        writer.write(open(pdf_path, "wb"))

    
    def pdf_already_converted(self, file_name):
        pdfs = self.session.get(f"{API_URL}/pdfs").json()["pdfs"]

        for pdf in pdfs:
    
            if file_name in pdf.get("input_file"):
                return pdf.get("id")
                
    
        
    def convert_pdf(self, pdf_path: str, output_path: str) -> str:
        #gets the file name, for example if the pdf_path was "question-data\pastpapers\N5_Mathematics_all_2015.pdf" "N5_Mathematics_all_2015" would be returned
        file_name = self.get_filename(pdf_path)

        #overwrites inputed pdf with a question only verison
        self.create_question_only_pdf(pdf_path)
        
        #checks if Mathpix as already converted a pdf to text with the same name
        pdf_id = self.pdf_already_converted(file_name)

        #if pdf hasn't been converted before, convert it
        if not pdf_id:

            #sends the the pdf to the convertion url. 
            res = self.session.post(f"{API_URL}/pdfs", files={"file" : open(pdf_path, "rb")})
            pdf_id = res.json()["pdf"]["id"]


        #waits until the pdf is finished processing
        while True:
            response = self.session.get(f"{API_URL}/pdfs/{pdf_id}")

            if response.json()["pdf"]["status"] == "completed":
                break

            sleep(1)

        #gets the converted pdf text from the server
        pdf_text = self.session.get(f"{API_URL}/pdfs/{pdf_id}/mmd").text    

        
        save_path = f"{output_path}/{file_name}.txt"

        #saves the text in the specifed output folder
        with open(save_path, "wb") as file:

            file.write(pdf_text.encode("utf"))

        #returns the file location of the converted data.
        return save_path

        


        
