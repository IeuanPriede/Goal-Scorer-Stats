import gspread
from google.oauth2.service_account import Credentials

# Define the scope and authenticate
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Goal-Scorer-Stats')

# Access the "stats" worksheet
stats = SHEET.worksheet('stats')

# Function to input data
def add_data_to_sheet():
    # Promt the user to enter data
    name = input("Enter players name: ")
    position = input("Enter players position(Attacker/Midfielder/Defender/Goalkeeper):")
    goals = int(input("Enter the number of goals scored: "))
    matches = int(input("Enter the number of matches played: "))
    minutes = int(input("Enter the amount of minutes played: "))
    # Appends the data to the sheet as a new row
    stats.append_row([name, position, goals, matches, minutes])
    print(f"Player '{name}' that plays as a '{position}' with {goals} goals in {matches} matches and {minutes} minutes has been added to the sheet!")

# Call the function
add_data_to_sheet()    

data = stats.get_all_values()

print(data)