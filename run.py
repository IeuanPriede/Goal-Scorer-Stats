import gspread
from google.oauth2.service_account import Credentials
import math
import sys

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
        display_player_stats(selected_name=name)
    else:
        # Ask for position, goals, matches, and minutes only if new player is added
        position = get_valid_position()
        goals = get_valid_integer("Enter the number of goals scored:\n ")
        matches = get_valid_integer("Enter the number of matches played:\n ")
        minutes = get_valid_integer("Enter the amount of minutes played:\n ")

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
        name = get_input_with_exit("Enter player's name, or press Enter to see the list of players (You can exit the program at anytime by typing 'exit'.):\n ").strip()
        if name =="":
            # Show the list of players if no name is entered
            print("\nPlayer List:")
            for player in player_names:
                print(player)
            
            # Proceed directly to allow the user to select a player from the list
            while True:
                selected_name = get_input_with_exit("\nEnter a player's name to view their stats:\n ").strip()
                if selected_name.lower() in [p.lower() for p in player_names]:
                    # Return the exact matching name from list
                    return next(p for p in player_names if p.lower() == selected_name.lower())
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
        position = get_input_with_exit("Enter player's position (Attacker/Midfielder/Defender/Goalkeeper):\n ").strip().capitalize()
        if position in allowed_positions:
            return position
        print(f"Invalid data: Position must be one of {allowed_positions}.")

def get_valid_integer(prompt):
    """
    Prompt user to enter a valid integer.
    """
    while True:
        user_input = get_input_with_exit(prompt)
        try:
            value = int(user_input)
            if value >= 0:
                return value
            print("Invalid data: Please enter a non-negative integer.")
        except ValueError:
            print("Invalid data: Please enter a valid integer.")

def display_player_stats(selected_name=None):
    """
    Display a list of players and allow the user to view, edit or remove their stats.
    If a specific player name is provided, jump directly to their stats.
    """    

    # Get all data from the sheet
    data = stats.get_all_values()

    # Extract the header and player names
    headers = data[0]
    player_data = data[1:]

    # Extract the player names
    player_names = [row[0] for row in player_data]

    if not player_names:
        print("\nNo players found in the stats sheet.")
        return

    if not selected_name:
        # Display the player list if no specific player is provided   
        print("\nPlayer List:")
        for name in player_names:
            print(name)

        # Prompt user to select a player's name
        while True:
            selected_name = get_input_with_exit("\nEnter a player's name to view their stats, type 'back' to go back, or type 'exit' to exit the program:\n ").strip()
            if selected_name.lower() == "back":
                return add_data_to_sheet()

            if selected_name.lower() in [p.lower() for p in player_names]:
                # Get the exact name
                selected_name = next(p for p in player_names if p.lower() == selected_name.lower())
                break
            else:
                print(f"Invalid selection: '{selected_name}' is not on the player list. Please try again")

    # Get the player's row
    index = [p.lower() for p in player_names].index(selected_name.lower())
    row_index = index + 2 # Account for header row (1-indexed in Google Sheets)
    player_row = player_data[index]

    print(f"\nStats for {selected_name}:")
    for key, value in zip(headers, player_row):
        print(f"{key}: {value}")
            
    # Offer options to edit or remove
    while True:
        print("\nOptions:")
        print("1. Edit stats")
        print("2. Remove player")
        print("3. Go back")

        choice = get_input_with_exit("\nEnter your choice:\n ").strip()

        if choice == "1":
            # Prompt for updated values
            position_input = input(f"Enter new position (current: {player_row[1]}):\n ").strip()
            position = position_input if position_input else player_row[1]

            goals_input = input(f"Enter new goals scored (current: {player_row[2]}):\n ").strip()
            goals = int(goals_input) if goals_input else int(player_row[2])

            matches_input = input(f"Enter new matches played (current: {player_row[3]}):\n ").strip()
            matches = int(matches_input) if matches_input else int(player_row[3])

            minutes_input = input(f"Enter new minutes played (current: {player_row[4]}):\n ").strip()
            minutes = int(minutes_input) if minutes_input else int(player_row[4])

            minutes_per_goal = calculate_minutes_per_goal(minutes, goals)

            # Update the row in the sheet
            stats.update(
                range_name=f'A{row_index}:F{row_index}', 
                values=[[selected_name, position, goals, matches, minutes, minutes_per_goal]],
            )
            print(f"\nStats for {selected_name} have been updated!")
            return add_data_to_sheet()

        elif choice == "2":
            # Remove the row from the sheet
            stats.delete_rows(row_index)
            print(f"\nStats for {selected_name} have been removed!")
            return add_data_to_sheet()

        elif choice == "3":
            return add_data_to_sheet()

        else:
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
        player_row = player_data[[p.lower() for p in player_names].index(name.lower())]
        player_stats = dict(zip(headers, player_row))
        print(f"\nStats for {name}:")
        for key, value in player_stats.items():
            print(f"{key}: {value}")
    else:
        print(f"Player '{name}' not found in the stats sheet.")

def get_input_with_exit(prompt):
    """
    Prompt the user for input, and exit the program if 'exit is entered.
    """
    user_input = input(prompt).strip()
    if user_input.lower() == "exit":
        print("\nExiting the program. Goodbye!")
        sys.exit()
    return user_input

# Call the functions to add a player and view stats
add_data_to_sheet()
display_player_stats()
