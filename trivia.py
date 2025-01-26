"""
Created on Mon Jan 20 21:52 2025

@author: Omar Nassar
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import random
import json

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

        filtered = self.data[   (self.data["Answer 1"] == a1) &
                                (self.data["Answer 2"] == a2) &
                                (self.data["Answer 3"] == a3)]
        
        self.correct_answers = filtered["Name"].tolist()

    def select_winners(self):
        selected_names = random.sample(self.correct_answers, min(len(self.correct_answers), 3))
        return selected_names
    
def get_form(data, form_id):
    # Search for the form with the given form_id
    for form in data["forms"]:
        if form["form_id"] == form_id:  # Convert form_id to string for comparison
            form_link = form["form_link"]
            answers = [question["correct_option"] for question in form["questions"]]
            
            # Pad with None if less than 3 answers exist
            while len(answers) < 3:
                answers.append(None)
                
            return form_link, answers
    return None, None    

def get_winners(day):
    with open('triviaDetails.json', 'r') as file:
        data = json.load(file)

    form_link, answers = get_form(data, day)
    print(form_link, answers)

    # # Your Google Form ID (from the URL: https://forms.google.com/d/formID/viewform)
    # trivia = Trivia("1C2nSAbcClybroHWtE6IMw6yFPocOQHs0dTyGiLig5Lg")
    trivia = Trivia(form_link)

    # Display the DataFrame
    print(trivia.data)

    trivia.find_correct(answers)
    print(trivia.correct_answers)
    print(trivia.select_winners())

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

    get_winners(1)
    


if __name__ == '__main__':
    main()