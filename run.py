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
            calculate_statistics()
            break
        else:
            print("Invalid choice. Please try again.")


"""
Prints instructions for the survery to user 
Prints questions to the user and passes their response to the validator
Puts user data into a list to send to worksheet
"""


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
            return

        name = validate_data("What is your name?\n", 'string')
        age = validate_data("What is your age?\n", 'age')
        district = validate_data("Which district are your from?\n", 'district')
        occupation = validate_data("What is your occupation?\n", 'string')
        illness = validate_data("Do you have any illnesses? (y/n)\n", 'yes_no')
        married = validate_data("Are you married? (y/n)\n", 'yes_no')
        children = validate_data("Do you have any children? (y/n)\n", 'yes_no')
        special_skills = validate_data("List any special skills:\n", 'string')
        survival_skills = validate_data(
            "How would you rate your survival skills (1-10)\n", 'rating')
        education = validate_data(
            "What is the highest level of education you have completed?\n", 'string')
        physically_active = validate_data(
            "Are you physically active on a regular basis? (y/n)\n", 'yes_no')

        user_data = [name, age, district, occupation, illness, married, children,
                     special_skills, survival_skills, education, physically_active]
        update_survey(user_data)
        print("Thank you for submitting your answers")
        break


"""
Validates each data input by user depending on the question asked 
Prints a ValueError if invalid information submitted
"""


def validate_data(question, validation_type):
    while True:
        user_input = input(question)

        try:
            if validation_type == 'string':
                if isinstance(user_input, str) and not user_input.isdigit():
                    pass
                else:
                    raise ValueError
            elif validation_type == 'age':
                age = int(user_input)
                if age <= 0:
                    raise ValueError
            elif validation_type == 'district':
                district = int(user_input)
                if district <= 0 or district > 13:
                    raise ValueError
            elif validation_type == 'yes_no':
                if user_input.lower() not in ['y', 'n']:
                    raise ValueError
            elif validation_type == 'rating':
                rating = int(user_input)
                if rating < 1 or rating > 10:
                    raise ValueError

            return user_input

        except ValueError:
            print("Invalid input. Please try again.")
# add code to print answers back to the user?


"""
Accesses the google worksheet and adds the user inputted data to the bottom row 
Returns the user to the main menu
"""


def update_survey(user_data):
    print("Updating survey...\n")
    survey_worksheet = SHEET.worksheet("results")
    survey_worksheet.append_row(user_data)
    print("Survey submission successful.\n")
    print("You will now be returned to the main menu.\n")

    get_program_choice()


def calculate_statistics():
    print("Calculating statistics...\n")
    survey_worksheet = SHEET.worksheet("results")

    name_values = survey_worksheet.col_values(1)[1:]
    total_entries = sum(1 for value in name_values if value)
    print(total_entries)

    age_values = survey_worksheet.col_values(2)[1:]
    age_values = [int(age) for age in age_values if age]
    average_age = sum(age_values) / len(age_values)
    print(average_age)

    youngest = min(age_values)
    print(youngest)

    oldest = max(age_values)
    print(oldest)


    # married%
    # children%
    # illness%
    # active%


print("Welcome to the Panem national population survey.")
get_program_choice()


# get_statistics():
