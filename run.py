import gspread
from google.oauth2.service_account import Credentials
import math

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
    # Get player names from the sheet
    player_names = get_player_names_from_sheet()

    # Promt the user to enter data with validation
    name = get_valid_name(player_names)

    # If the name is selected from the list(i,e., user pressed Enter and selected a player)
    if name in player_names:
        # Skip the inputs for position, goals, matches, and minutes
        print(f"\nShowing stats for player '{name}'.")
        display_player_stats_for_name(name)
    else:
        # Ask for position, goals, matches, and minutes only if new player is added
        position = get_valid_position()
        goals = get_valid_integer("Enter the number of goals scored: ")
        matches = get_valid_integer("Enter the number of matches played: ")
        minutes = get_valid_integer("Enter the amount of minutes played: ")

        # Calculate minutes per goal
        minutes_per_goal = calculate_minutes_per_goal(minutes, goals)

        # Appends the data to the sheet as a new row
        stats.append_row([name, position, goals, matches, minutes, minutes_per_goal])

        print(f"\nPlayer '{name}' that plays as '{position}' with {goals} goals in {matches} matches and {minutes} minutes" f"(Minutes per Goal: {minutes_per_goal}) has been added to the stats sheet!")

def calculate_minutes_per_goal(minutes, goals):
    """
    Calculate minutes per goal.
    If the player scored 0 goals, return 'N/A' to aviod division by zero.
    """ 
    return math.ceil(minutes / goals) if goals > 0 else "N/A"  

def get_valid_name(player_names):
    """
    Prompt user to enter a valid name, or press Enter to see the list of players.
    """
    while True:
        name = input("Enter player's name (or press Enter to see the list of players): ").strip()
        if name =="":
            # Show the list of players if no name is entered
            print("\nPlayer List:")
            for player in player_names:
                print(player)
            
            # Proceed directly to allow the user to select a player from the list
            while True:
                selected_name = input("\nEnter a player's name to view their stats: ").strip()
                if selected_name in player_names:
                    return selected_name # Return valid player name
                else:
                    print(f"Invalid selection: '{selected_name}' is not in the player list. Please try again.")
        elif name:    
            return name # Valid name entered
        else:
            print("Invalid data: Please input a valid name.")

def get_valid_position():
    """
    Prompt user to enter a valid position
    """
    allowed_positions = ["Attacker", "Midfielder", "Defender", "Goalkeeper"]
    while True:
        position = input("Enter player's position (Attacker/Midfielder/Defender/Goalkeeper)")
        if position in allowed_positions:
            return position
        print(f"Invalid data: Position must be one of {allowed_positions}.")

def get_valid_integer(prompt):
    """
    Prompt user to enter a valid integer.
    """
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            print("Invalid data: Please enter a non-negative integer.")
        except ValueError:
            print("Invalid data: Please enter a valid integer.")

def display_player_stats():
    """
    Prompt the user to input a player's name and display their stats.
    """    

    # Get all data from the sheet
    data = stats.get_all_values()

    # Extract the header and player names
    headers = data[0]
    player_data = data[1:]

    # Extract the player names
    player_names = [row[0] for row in player_data]

    print("\nPlayer List:")
    for name in player_names:
        print(name)

    # Prompt user to select a player's name
    while True:
        selected_name = input("\nEnter a player's name to view their stats: ").strip()
        if selected_name in player_names:
            # Find and display the stats of the selected player
            player_row = player_data[player_names.index(selected_name)]
            player_stats = dict(zip(headers, player_row))
            print(f"\nStats for {selected_name}:")
            for key, value in player_stats.items():
                print(f"{key}: {value}")
            break
        print(f"Invalid selection: '{selected_name}' is not in the player list. Please try again.")
    
def get_player_names_from_sheet():
    """
    Retrieve the list of player names from the spreadsheet.
    """

    data = stats.get_all_values()

    player_data = data[1:]
    player_names = [row[0] for row in player_data]

    return player_names

def display_player_stats_for_name(name):
    """
    Display the stats for a specific player by name.
    """
    # Get all data from the sheet
    data = stats.get_all_values()

    # Extract the header and player names
    headers = data[0]
    player_data = data[1:]

    # Extract the player names
    player_names = [row[0] for row in player_data]

    if name in player_names:
        # Find and display the stats of the selected player
        player_row = player_data[player_names.index(name)]
        player_stats = dict(zip(headers, player_row))
        print(f"\nStats for {name}:")
        for key, value in player_stats.items():
            print(f"{key}: {value}")
    else:
        print(f"Player '{name}' not found in the stats sheet.")


# Call the functions to add a player and view stats
add_data_to_sheet()
display_player_stats()
