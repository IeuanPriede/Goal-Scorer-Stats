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
def add_name_to_sheet():
    # Promt the user to enter a name
    name = input("Enter players name: ")
    # Appends the name to the sheet as a new row
    stats.append_row([name])
    print(f"Player '{name}' has been added to the sheet!")

# Call the function
add_name_to_sheet()    

data = stats.get_all_values()

print(data)