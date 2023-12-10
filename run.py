import colorama
import time
import os
import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init(autoreset=True)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('panem_survey')


def get_program_choice():
    """
    Obtain which program to open based on the users input
    Validates their input and triggers desired program function
    """
    while True:
        choice = input(f"\n- To submit data"
                       f" press '{Fore.YELLOW}{Style.BRIGHT}"
                       f"a{Style.RESET_ALL}'\n- To view statistics"
                       f" press '{Fore.YELLOW}{Style.BRIGHT}"
                       f"b{Style.RESET_ALL}'\n\n")

        if choice == 'a':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Starting survey...\n\n")
            time.sleep(2)
            get_survey_data()
            break
        elif choice == 'b':
            calculate_statistics()
            break
        else:
            print("Invalid choice. Please try again.")


def get_survey_data():
    """
    Prints instructions for the survery to user
    Prints questions to the user and passes their response to the validator
    Puts user data into a list to send to worksheet
    """
    print(Fore.BLACK + Back.WHITE + Style.BRIGHT + " S U R V E Y ")
    print("\n1. Please answer all the questions truthfully.")
    time.sleep(1)
    print("2. Type your answers in lowercase.")
    time.sleep(1)
    print("3. For answers requiring multiple items please separate with"
          " commas.")
    print("   example: 1,2,3,4\n\n")
    time.sleep(1)
    print("By completing the survey, you can lower the possibility of being"
          " chosen\nas a Tribute in the next annual Hunger Games.\n\n")
    time.sleep(1)
    print(Style.BRIGHT +
          "M A Y   T H E   O D D S   B E   E V E R   I N   Y O U R"
          "   F A V O R.\n\n")
    time.sleep(1)

    while True:
        continue_prompt = input(f"Press '{Fore.YELLOW}{Style.BRIGHT}"
                                f"y{Style.RESET_ALL}' to continue or"
                                f" '{Fore.YELLOW}{Style.BRIGHT}"
                                f"n{Style.RESET_ALL}' to exit:\n")
        if continue_prompt == 'n':
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
            break
        elif continue_prompt == 'y':
            break
        else:
            print("Invalid choice. Please try again.")

    name = validate_data("What is your name?\n", 'string')
    age = validate_data("What is your age?\n", 'age')
    district = validate_data("Which district are your from? (1-13)\n",
                             'district')
    occupation = validate_data("What is your occupation?\n", 'string')
    illness = validate_data("Do you have any illnesses? (y/n)\n", 'yes_no')
    married = validate_data("Are you married? (y/n)\n", 'yes_no')
    children = validate_data("Do you have any children? (y/n)\n", 'yes_no')
    special_skills = validate_data("List any special skills:\n", 'string')
    survival_skills = validate_data(
        "How would you rate your survival skills (1-10)\n", 'rating')
    education = validate_data(
        "What is the highest level of education you have completed?\n",
        'string')
    physically_active = validate_data(
        "Are you physically active on a regular basis? (y/n)\n", 'yes_no')

    user_data = [name, age, district, occupation, illness, married,
                 children, special_skills, survival_skills, education,
                 physically_active]
    update_survey(user_data)
    print("Thank you for submitting your answers")


def validate_data(question, validation_type):
    """
    Validates each data input by user depending on the question asked
    Prints a ValueError if invalid information submitted
    """
    while True:
        user_input = input(question)

        try:
            if validation_type == 'string':
                if isinstance(user_input, str) and not user_input.isdigit() \
                        and user_input != '':
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


def update_survey(user_data):
    """
    Accesses the google worksheet and adds the user inputted data to
    the bottom row
    Returns the user to the main menu
    """
    print("Updating survey...\n")
    survey_worksheet = SHEET.worksheet("results")
    survey_worksheet.append_row(user_data)
    print("Survey submission successful.\n")
    print("You will now be returned to the main menu.\n")
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')
    main()


def calculate_statistics():
    """
    Fetches values from the worksheet, performs calculations based
    on the statistic
    Prints the result to the user
    Returns the user to the main menu
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Calculating statistics...\n\n")
    time.sleep(1)
    print(Fore.BLACK + Back.WHITE + Style.BRIGHT +
          " C U R R E N T   S T A T I S T I C S ")
    survey_worksheet = SHEET.worksheet("results")
    
    # Total entries 
    name_values = survey_worksheet.col_values(1)[1:]
    total_entries = sum(1 for value in name_values if value)
    print(f"\n- {Style.BRIGHT}{total_entries}{Style.RESET_ALL} individuals"
          " have participated in the survey.")
    # Average age
    age_values = survey_worksheet.col_values(2)[1:]
    age_values = [int(age) for age in age_values if age]
    average_age = sum(age_values) / len(age_values)
    print(
        f"- The average age of survey participants is "
        f"{Style.BRIGHT}{round(average_age)}{Style.RESET_ALL} years old.")
    # Youngest age
    youngest = min(age_values)
    print(
        f"- The youngest participant"
        f" is {Style.BRIGHT}{youngest}{Style.RESET_ALL} years old.")
    # Oldest age
    oldest = max(age_values)
    print(
        f"- The oldest participant"
        f" is {Style.BRIGHT}{oldest}{Style.RESET_ALL} years old.")
    # Percentage of illness
    illness_values = survey_worksheet.col_values(5)[1:]
    illness_percentage = illness_values.count('y') / len(illness_values)*100
    print(f"- {Style.BRIGHT}{round(illness_percentage)}%{Style.RESET_ALL} of"
          " respondents reported having an illness.")
    # Percentage married
    marital_status_values = survey_worksheet.col_values(6)[1:]
    married_percentage = marital_status_values.count(
        'y') / len(marital_status_values)*100
    print(f"- {Style.BRIGHT}{round(married_percentage)}%{Style.RESET_ALL} of"
          " participants are married.")
    # Percentage with children
    children_values = survey_worksheet.col_values(7)[1:]
    children_percentage = children_values.count('y') / len(children_values)*100
    print(f"- {Style.BRIGHT}{round(children_percentage)}%{Style.RESET_ALL} of"
          " respondents have children.")
    # Percentage who are active
    activity_values = survey_worksheet.col_values(11)[1:]
    active_percentage = activity_values.count('y') / len(activity_values)*100
    print(f"- {Style.BRIGHT}{round(active_percentage)}%{Style.RESET_ALL} of"
          " individuals are physically active.\n\n")

    while True:
        menu_prompt = input(f"Press '{Fore.YELLOW}{Style.BRIGHT}"
                            f"y{Style.RESET_ALL}' to return to the"
                            f" main menu\n")
        if menu_prompt == 'y':
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
            break
        else:
            print(f"Error: Invalid input. Please enter"
                  f" '{Fore.YELLOW}{Style.BRIGHT}y{Style.RESET_ALL}'.")


def main():
    """
    Runs the start program print message and choice function
    """
    print(Fore.BLACK + Back.WHITE + Style.BRIGHT +
          " T H E   P A N E M   N A T I O N A L   P O P U L A T I O N"
          "   S U R V E Y ")
    get_program_choice()


main()
