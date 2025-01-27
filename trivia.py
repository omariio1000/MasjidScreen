"""
Created on Mon Jan 20 21:52 2025

@author: Omar Nassar
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import random
import json
import qrcode

class Trivia:
    def __init__(self, form_id):
        key_file = "icch-ramadan-trivia-0be68aa75675.json"

        SCOPES = ["https://www.googleapis.com/auth/forms.responses.readonly", "https://www.googleapis.com/auth/forms.body.readonly"]
        credentials = service_account.Credentials.from_service_account_file(key_file, scopes=SCOPES)

        service = build("forms", "v1", credentials=credentials)

        # Fetch the form metadata to get question titles
        form_metadata = service.forms().get(formId=form_id).execute()
        items = form_metadata.get("items", {})

        # Create a mapping of question IDs to their titles
        question_mapping = {}
        for item in items:
            question_id = item.get("questionItem", {}).get("question", {}).get("questionId")
            question_text = item.get("title", "")
            if question_id:
                question_mapping[question_id] = question_text

        # Fetch form responses
        responses = service.forms().responses().list(formId=form_id).execute()
        all_responses = responses.get("responses", [])

        # Initialize a list for DataFrame rows
        rows = []

        # Process each response
        for response in all_responses:
            answers = response.get("answers", {})
            row = {question_mapping.get(key, key): value.get("textAnswers", {}).get("answers", [{}])[0].get("value", "") 
                for key, value in answers.items()}
            rows.append(row)

        # Convert the list of rows into a Pandas DataFrame
        self.data = pd.DataFrame(rows).drop_duplicates(subset="Name", keep="last")
        self.correct_answers = []

    def find_correct(self, answers):
        a1, a2, a3 = answers

        filtered = self.data[   (self.data["Question 1"] == a1) &
                                (self.data["Question 2"] == a2) &
                                (self.data["Question 3"] == a3)]
        
        self.correct_answers = filtered["Name"].tolist()

    def select_winners(self):
        selected_names = random.sample(self.correct_answers, min(len(self.correct_answers), 3))
        return selected_names
    
def get_form_link_answers(json, form_id):
    # Search for the form with the given form_id
    for form in json["forms"]:
        if form["form_id"] == form_id:  # Convert form_id to string for comparison
            form_link = form["form_link"]
            answers = [question["correct_option"] for question in form["questions"]]
            
            # Pad with None if less than 3 answers exist
            while len(answers) < 3:
                answers.append(None)
                
            return form_link, answers
    return None, None    

def get_form_question_options(json, form_id):
    for form in json["forms"]:
        if form["form_id"] == form_id:  # Convert form_id to string for comparison
            questions = [question["question_details"] for question in form["questions"]]
            option1 = [question["option_1"] for question in form["questions"]]
            option2 = [question["option_2"] for question in form["questions"]]
            option3 = [question["option_3"] for question in form["questions"]]
            
            return questions, option1, option2, option3
    return None, None, None, None

def get_winners(day) -> list[str]:
    """Get the winner of the day given the day of the month"""
    with open('triviaDetails.json', 'r') as file:
        trivia_json = json.load(file)

    form_link, answers = get_form_link_answers(trivia_json, day)
    print(form_link, answers)

    # # Your Google Form ID (from the URL: https://forms.google.com/d/formID/viewform)
    # trivia = Trivia("1C2nSAbcClybroHWtE6IMw6yFPocOQHs0dTyGiLig5Lg")
    trivia = Trivia(form_link)

    # Display the DataFrame
    print(trivia.data)

    trivia.find_correct(answers)
    print(trivia.correct_answers)

    winners = trivia.select_winners()

    print(winners)

    return winners

def get_questions_and_answers(day):
    """Get the winner of the day given the day of the month"""
    with open('triviaDetails.json', 'r') as file:
        trivia_json = json.load(file)

    questions, option1, option2, option3 = get_form_question_options(trivia_json, day)
    print(questions, option1, option2, option3)

    return questions, option1, option2, option3

def make_qr_with_link(public_link):
    """Make a QR code for a google form given the code from the public link"""
    img = qrcode.make(f"https://docs.google.com/forms/d/e/{public_link}/viewform")
    img.save(f"trivia.png")

def make_qr(day):
    with open('triviaDetails.json', 'r') as file:
        trivia_json = json.load(file)
        for form in trivia_json["forms"]:
            if form["form_id"] == day:  # Convert form_id to string for comparison
                public_link = form["public_link"]

    make_qr_with_link(public_link)
    print(f"Generated qr code for day {day}: \"https://docs.google.com/forms/d/e/{public_link}/viewform\"")

def main():
    # with open('triviaDetails.json', 'r') as file:
    #     data = json.load(file)

    # form_link, answers = get_form(data, 1)
    # print(form_link, answers)

    # # # Your Google Form ID (from the URL: https://forms.google.com/d/formID/viewform)
    # # trivia = Trivia("1C2nSAbcClybroHWtE6IMw6yFPocOQHs0dTyGiLig5Lg")
    # trivia = Trivia(form_link)

    # # Display the DataFrame
    # print(trivia.data)

    # trivia.find_correct(answers)
    # print(trivia.correct_answers)
    # print(trivia.select_winners())

    # make_qr("1FAIpQLSeuOSzoL511RD_56Bo6FXJbh2OhmCXXwcLveIn7WUW0A7QLkQ")

    get_winners(1)
    get_questions_and_answers(1)    


if __name__ == '__main__':
    main()