import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('panem_survey')

""" use to print worksheet data in terminal 
results = SHEET.worksheet('results')

data = results.get_all_values()

print(data)
"""


def get_program_choice():
    while True:
        choice = input("To submit data press 'a', to view the statistics press 'b':\n")

        if choice == 'a':
            print("Starting survey...")
            # get_survey_data()
            break
        elif choice == 'b':
            print("Fetching statistics...")
            # get_statistics()
            break
        else:
            print("Invalid choice. Please try again.")


print("Welcome to the Panem national population survey.")
get_program_choice()


# get_survey_data()

# get_statistics()
