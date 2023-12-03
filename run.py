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

"""
Obtain which program to open based on the users input
Validates their input and triggers desired program function
"""


def get_program_choice():
    while True:
        choice = input(
            "To submit data press 'a', to view the statistics press 'b':\n")

        if choice == 'a':
            print("Starting survey...")
            get_survey_data()
            break
        elif choice == 'b':
            print("Fetching statistics...")
            # get_statistics()
            break
        else:
            print("Invalid choice. Please try again.")


def get_survey_data():
    print("Please answer all the questions truthfully.")
    print("Type your answers in lowercase. For answers requiring multiple items please separate with commas without spaces.")
    print("Example: 1,2,3,4")
    print("Completion of the survey will reduce your chance of being selected as Tribute in the next annual Hunger Games…")
    print("May the odds be ever in your favor.")
    
    while True:
        continue_prompt = input("Press 'y' to continue or 'n' to exit:\n")
        if continue_prompt == 'n':
            get_program_choice()
            break
    
        name = input("What is your name?\n")
        age = input("What is your age?\n")
        district = input("Which district are your from?\n")
        occupation = input("What is your occupation?\n")
        illness = input("Do you have any illnesses? (y/n)\n")
        married = input("Are you married? (y/n)\n")
        children = input("Do you have any children? (y/n)\n")
        special_skills = input("List any special skills:\n")
        survival_skills = input("How would you rate your survival skills (1-10)\n")
        education = input("What is the highest level of education you have completed?\n")
        physically_active = input("Are you physically active on a regular basis? (y/n)\n")


print("Welcome to the Panem national population survey.")
get_program_choice()

# get_statistics()
