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
        self.data = pd.DataFrame(rows).drop_duplicates(subset="Name", keep="first")
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
    

    

def main():
    with open('triviaDetails.json', 'r') as file:
        data = json.load(file)

    # Extract the forms and questions
    forms_data = []
    for form in data["forms"]:
        form_id = form["form_id"]
        form_link = form["form_link"]
        
        # Extract answers for each question (ensure exactly 3 answers are present)
        answers = [question["correct_option"] for question in form["questions"]]
        
        # Pad with None if less than 3 answers exist (to handle cases with fewer questions)
        while len(answers) < 3:
            answers.append(None)

        # Combine form data with the answers
        forms_data.append([form_id, form_link] + answers)

    # Create DataFrame with specified column headers
    df = pd.DataFrame(forms_data, columns=["form_id", "form_link", "answer 1", "answer 2", "answer 3"])

    # Display the DataFrame
    print(df)

    form_data = df[df["form_id"] == 1]
    form_link = form_data["form_link"].values[0]
    answers = form_data[["answer 1", "answer 2", "answer 3"]].values[0]

    print(form_data, form_link, answers)

    # # Your Google Form ID (from the URL: https://forms.google.com/d/formID/viewform)
    # trivia = Trivia("1C2nSAbcClybroHWtE6IMw6yFPocOQHs0dTyGiLig5Lg")
    trivia = Trivia(form_link)

    # Display the DataFrame
    print(trivia.data)

    trivia.find_correct(answers)
    print(trivia.correct_answers)
    print(trivia.select_winners())
    


if __name__ == '__main__':
    main()