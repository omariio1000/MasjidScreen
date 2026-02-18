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
from datetime import datetime, timedelta
from emails import send_email
import os

# Base directory and resource paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, '..', 'resources')
SERVICE_ACCOUNT_FILE = os.path.join(RESOURCES_DIR, 'service_account.json')
TRIVIA_DETAILS_FILE = os.path.join(RESOURCES_DIR, 'trivia_details.json')
TRIVIA_WINNERS_FILE = os.path.join(RESOURCES_DIR, 'trivia_winners.json')
TRIVIA_ALL_ANSWERS_FILE = os.path.join(RESOURCES_DIR, 'trivia_all_answers.json')
RAMADAN_FIRST_DAY_FILE = os.path.join(RESOURCES_DIR, 'ramadan_first_day.txt')
AMAZON_CODES_FILE = os.path.join(RESOURCES_DIR, 'amazon_codes.txt')
AMAZON_USED_FILE = os.path.join(RESOURCES_DIR, 'amazon_used.txt')

def _ensure_json_file(filepath, default_content="{}"):
    """Create a JSON file with default content if it doesn't exist"""
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(default_content)
        print(f"Created missing file: {filepath}")


class Trivia:
    """Trivia class for finding correct answers and selecting"""

    def __init__(self, form_id, day, test=False):
        """Initialize by getting day's form, logging answers, and selecting winners"""

        key_file = SERVICE_ACCOUNT_FILE

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

        save_all_responses(rows, day, test=test)

        # Convert the list of rows into a Pandas DataFrame
        self.data = pd.DataFrame(rows).drop_duplicates(subset=["First Name", "Last Name"], keep="last")
        self.correct_answers = []

    def find_correct(self, answers):
        """Find the people who answered correctly and filter them"""

        a1, a2, a3 = answers

        if not self.data.empty:
            filtered = self.data[   (self.data["Question 1"] == a1) &
                                    (self.data["Question 2"] == a2) &
                                    (self.data["Question 3"] == a3)]
        
            if not filtered.empty:
                self.correct_answers = filtered.apply(lambda row: [str(row["First Name"] + " " + row["Last Name"]), row["Email"]], axis=1).tolist()

    def select_winners(self):
        """Select three winners at most from filtered answers"""

        _ensure_json_file(TRIVIA_WINNERS_FILE)
        try:
            with open(TRIVIA_WINNERS_FILE, "r") as file:
                past_winners_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            past_winners_data = {}

        past_winners = set()
        for winners_list in past_winners_data.values():
            for winner in winners_list:
                past_winners.add(winner[1])
        
        new_winners = [entry for entry in self.correct_answers if entry[1] not in past_winners]

        if (len(new_winners) < 3):
            past_winners_pool = [entry for entry in self.correct_answers if entry[1] in past_winners]
            random.shuffle(past_winners_pool)
            remaining_needed = 3 - len(new_winners)
            new_winners.extend(past_winners_pool[:min(remaining_needed, len(past_winners_pool))])

        selected_names = random.sample(new_winners, min(len(new_winners), 3))
        return selected_names

def rmDoubleSpace(text: str) -> str:
    """Removes extra spaces between words and trims leading/trailing spaces."""
    return " ".join(text.split())

def cleanup(text: str) -> str:
    return rmDoubleSpace(text.strip().lower())

def save_all_responses(data, day, test=False):
    """Log all responses in form at time of winner selection"""

    for entry in data:
        if "First Name" in entry:
            entry["First Name"] = cleanup(entry["First Name"])
        if "Last Name" in entry:
            entry["Last Name"] = cleanup(entry["Last Name"])
        if "Email" in entry:
            entry["Email"] = cleanup(entry["Email"])

    if test:
        print(f"[TEST] Would save {len(data)} responses for day {day}")
        return

    _ensure_json_file(TRIVIA_ALL_ANSWERS_FILE)
    try:
        with open(TRIVIA_ALL_ANSWERS_FILE, "r") as file:
            all_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        all_data = {}

    all_data[str(day)] = data

    with open(TRIVIA_ALL_ANSWERS_FILE, "w") as file:
        json.dump(all_data, file, indent=4)

def get_form_link_answers(json, form_id):
    """Get the form link and correct answers from trivia_details.json"""

    # Search for the form with the given form_id
    for form in json["forms"]:
        if str(form["form_id"]) == str(form_id):
            form_link = form["form_link"]
            answers = [question["correct_option"] for question in form["questions"]]
            
            # Pad with None if less than 3 answers exist
            while len(answers) < 3:
                answers.append(None)
                
            return form_link, answers
    return None, None    

def get_form_questions_options(day):
    """Get questions and options from the form given day of trivia"""

    key_file = SERVICE_ACCOUNT_FILE

    SCOPES = ["https://www.googleapis.com/auth/forms.responses.readonly", "https://www.googleapis.com/auth/forms.body.readonly"]
    credentials = service_account.Credentials.from_service_account_file(key_file, scopes=SCOPES)

    service = build("forms", "v1", credentials=credentials)

    try:
        with open(TRIVIA_DETAILS_FILE, 'r') as file:
            trivia_json = json.load(file)
    except FileNotFoundError:
        print(f"Warning: {TRIVIA_DETAILS_FILE} not found")
        return [], [], [], [], []

    form_link, _ = get_form_link_answers(trivia_json, day)

    if not form_link:
        return [], [], [], [], []

    form = service.forms().get(formId=form_link).execute()

    questions = []
    option1, option2, option3, option4 = [], [], [], []

    all_items = form.get("items", [])
    
    # Get the last 3 items (trivia questions) - forms may have metadata items before questions
    items = all_items[-3:] if len(all_items) >= 3 else all_items

    for idx, item in enumerate(items):
        question_details = item.get("title", item.get("description", "No details available"))
        options = [
            opt.get("value") for opt in item.get("questionItem", {})
            .get("question", {})
            .get("choiceQuestion", {})
            .get("options", [])
        ]

        questions.append(question_details)

        option1.append(options[0] if len(options) > 0 else "")
        option2.append(options[1] if len(options) > 1 else "")
        option3.append(options[2] if len(options) > 2 else "")
        option4.append(options[3] if len(options) > 3 else "")
    
    print(f"Questions: {questions}\nOptions: {option1}, {option2}, {option3}, {option4}")

    return questions, option1, option2, option3, option4


def get_winners(day, test=False):
    """Get the winners of the day given the day of the month"""

    try:
        with open(TRIVIA_DETAILS_FILE, 'r') as file:
            trivia_json = json.load(file)
    except FileNotFoundError:
        print(f"Warning: {TRIVIA_DETAILS_FILE} not found")
        return []

    form_link, answers = get_form_link_answers(trivia_json, day)
    # print(form_link, answers)

    if not form_link:
        return []
    
    trivia = Trivia(form_link, day, test=test)
    if not trivia.data.empty:
        trivia.data['First Name'] = trivia.data['First Name'].apply(lambda x: cleanup(x))
        trivia.data['Last Name'] = trivia.data['Last Name'].apply(lambda x: cleanup(x))
        trivia.data['Email'] = trivia.data['Email'].apply(lambda x: cleanup(x))

    # Display the DataFrame
    # print(f"\n{trivia.data}")

    trivia.find_correct(answers)
    # print(f"\nAnswered correctly: {trivia.correct_answers}")

    winners = trivia.select_winners()

    # print(f"\nSelected winners: {winners}")
    cleanupFiles()
    return winners

def make_qr_with_link(public_link, filename):
    """Make a QR code for a google form given the code from the public link"""

    img = qrcode.make(public_link, border=1)
    img.save(f"{filename}")

def make_qr(day):
    """Make a QR code given the day of ramadan"""

    public_link = None
    try:
        with open(TRIVIA_DETAILS_FILE, 'r') as file:
            trivia_json = json.load(file)
            for form in trivia_json["forms"]:
                if str(form["form_id"]) == str(day):
                    public_link = form["public_link"]
                    break
    except FileNotFoundError:
        print(f"Warning: {TRIVIA_DETAILS_FILE} not found")

    if not public_link:
        print(f"Warning: No form found for day {day}, using fallback QR")
        make_qr_with_link("icc-hillsboro.org", "trivia.png")
        return

    make_qr_with_link(public_link, "trivia.png")
    print(f"\nGenerated qr code for day {day}: \"{public_link}\"")

def get_next_code():
    """Get next amazon code from text file"""

    try:
        # Read all lines from the file
        with open(AMAZON_CODES_FILE, 'r') as file:
            lines = file.readlines()
        
        # Check if the file is not empty
        if not lines:
            print("Error: No amazon codes remaining.")
            return None
        
        # Remove the first line
        first_line = lines[0].strip()
        lines = lines[1:]
        
        # Write the remaining lines back to the file
        with open(AMAZON_CODES_FILE, 'w') as file:
            file.writelines(lines)

        # Log the used code
        with open(AMAZON_USED_FILE, 'a') as used_file:
            used_file.write(f"{first_line} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        return first_line
    
    except FileNotFoundError:
        print(f"Error: Amazon codes file not found at {AMAZON_CODES_FILE}")
        # Create empty file so it doesn't crash again
        os.makedirs(os.path.dirname(AMAZON_CODES_FILE), exist_ok=True)
        with open(AMAZON_CODES_FILE, 'w') as f:
            pass
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_trivia_day(test=False):
    """Get what day of ramadan it is"""

    try:
        with open(RAMADAN_FIRST_DAY_FILE, 'r') as file:
            first_day = file.readline().strip()
    except FileNotFoundError:
        print(f"Warning: {RAMADAN_FIRST_DAY_FILE} not found, defaulting to day 0")
        return 0

    if not first_day:
        print("Warning: Ramadan first day file is empty, defaulting to day 0")
        return 0

    try:
        input_date = datetime.strptime(first_day, "%Y-%m-%d")
    except ValueError:
        print(f"Warning: Invalid date format in {RAMADAN_FIRST_DAY_FILE}: '{first_day}'")
        return 0

    today = datetime.now()
    delta = today - input_date
    day = delta.days + 1

    return day

def check_winners_updated(day) -> bool:
    """Check if winners have been updated already for this day"""

    try:
        with open(TRIVIA_WINNERS_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    
    if day in data:
        return True
    
    return False

def get_past_winners(day):
    """Get the past winners that have already been logged for this day"""

    try:
        with open(TRIVIA_WINNERS_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    winners_data = data.get(day, [])

    winners = [[winner[0], winner[1]] for winner in winners_data if len(winner) >= 2]

    return winners

def log_winners(day, winners : list, test):
    """Log winners for the day and send emails with gift card codes"""

    _ensure_json_file(TRIVIA_WINNERS_FILE)
    
    # Load existing data from the JSON file or create a new structure
    try:
        with open(TRIVIA_WINNERS_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    # Ensure the current date exists as a key
    if day not in data:
        data[day] = []
    
    # Send emails with gift card codes to winners
    date_str = datetime.now().strftime("%B %d, %Y")
    for winner in winners:
        if len(winner) >= 2:
            name, email = winner[0], winner[1]
            if not test:
                code = get_next_code()
                if code:
                    try:
                        send_email(name, email, code, date_str)
                    except Exception as e:
                        print(f"Failed to send email to {name}: {e}")
                else:
                    print(f"No amazon codes available for {name}")
            else:
                print(f"[TEST] Would send email to {name} ({email})")
    
    if test:
        print(f"[TEST] Would log {len(winners)} winners for day {day}")
        return
    
    data[day].extend(winners)
    
    # Save the updated data back to the JSON file
    with open(TRIVIA_WINNERS_FILE, "w") as file:
        json.dump(data, file, indent=4)
    
    if winners:
        print(f"\nLogged {len(winners)} winners for day {day}.")
    else:
        print(f"\nLogged 0 winners for day {day}.")

def cleanupFiles():
    """Cleans up winner and all answer files"""
    # Clean up winners file
    _ensure_json_file(TRIVIA_WINNERS_FILE)
    try:
        with open(TRIVIA_WINNERS_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    for day in data:
        for winner in data[day]:
            if len(winner) >= 2:
                winner[0] = cleanup(winner[0])
                winner[1] = cleanup(winner[1])

    with open(TRIVIA_WINNERS_FILE, 'w') as file:
        json.dump(data, file, indent=4)


    # Clean up all answers file
    _ensure_json_file(TRIVIA_ALL_ANSWERS_FILE)
    try:
        with open(TRIVIA_ALL_ANSWERS_FILE, "r") as file:
            all_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        all_data = {}

    for day in all_data:
        for entry in all_data[day]:
            if "First Name" in entry:
                entry["First Name"] = cleanup(entry["First Name"])
            if "Last Name" in entry:
                entry["Last Name"] = cleanup(entry["Last Name"])
            if "Email" in entry:
                entry["Email"] = cleanup(entry["Email"])

    with open(TRIVIA_ALL_ANSWERS_FILE, "w") as file:
        json.dump(all_data, file, indent=4)

def main():
    """Test trivia functionality"""

    # day = get_trivia_day(test=True)
    # print(day)
    # get_winners(0)
    # get_form_questions_options(0)

    cleanupFiles()

if __name__ == '__main__':
    main()