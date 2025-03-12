import requests
import pandas as pd
from openpyxl import load_workbook
import tkinter as tk
from tkcalendar import Calendar
from tkinter import filedialog


# Function to prompt the user for the date range using a calendar widget
def select_dates():
    root = tk.Tk()
    root.title("Select Dates")
    root.geometry("400x500")

    # Create a calendar widget for the start date
    start_label = tk.Label(root, text="Select Start Date:")
    start_label.pack(padx=10, pady=5)
    start_calendar = Calendar(root, date_pattern='yyyy-mm-dd', selectmode='day', showweeknumbers=False, firstweekday='monday')
    start_calendar.pack(padx=10, pady=5)

    # Create a calendar widget for the end date
    end_label = tk.Label(root, text="Select End Date:")
    end_label.pack(padx=10, pady=5)
    end_calendar = Calendar(root, date_pattern='yyyy-mm-dd', selectmode='day', showweeknumbers=False, firstweekday='monday')
    end_calendar.pack(padx=10, pady=5)

    # Variables to store the selected dates
    start_date = None
    end_date = None
    
    # Button to confirm the dates
    def confirm_dates():
        nonlocal start_date, end_date
        start_date = start_calendar.get_date()
        end_date = end_calendar.get_date()
        root.quit()

    confirm_button = tk.Button(root, text="Confirm Dates", command=confirm_dates)
    confirm_button.pack(padx=10, pady=20)

    # Show the window and wait for confirmation
    root.deiconify()
    root.mainloop()

    return start_date, end_date

# Get the date range from the user
start_date, end_date = select_dates()

# Exit if no date range is provided
if not start_date or not end_date:
    print("No date range provided. Exiting...")
    exit()

# Define the API endpoint and parameters
url = 'https://statsapi.mlb.com/api/v1/transactions'
params = {
    'startDate': start_date,  # User-provided start date
    'endDate': end_date       # User-provided end date
}

mlb_teams = [
    "Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox", 
    "Chicago Cubs", "Chicago White Sox", "Cincinnati Reds", "Cleveland Indians", 
    "Colorado Rockies", "Detroit Tigers", "Houston Astros", "Kansas City Royals", 
    "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins", "Milwaukee Brewers", 
    "Minnesota Twins", "New York Mets", "New York Yankees", "Oakland Athletics", 
    "Philadelphia Phillies", "Pittsburgh Pirates", "San Diego Padres", "San Francisco Giants", 
    "Seattle Mariners", "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers", 
    "Toronto Blue Jays", "Washington Nationals"
]

# Send a GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
else:
    print(f'Failed to retrieve data: {response.status_code}')
    data = None

# Process and organize the retrieved data
if data and 'transactions' in data:
    transactions = []
    
    for transaction in data['transactions']:
        date = transaction.get('date')
        player = transaction.get('person', {}).get('fullName')

        # Use fromTeam if available, otherwise use toTeam
        team = transaction.get('fromTeam', {}).get('name') or transaction.get('toTeam', {}).get('name')
        
        transaction_type = transaction.get('typeDesc')

        description = transaction.get('description')
        
        if team in mlb_teams:
            transactions.append([date, team, transaction_type, player, description])

    # Create a DataFrame
    df = pd.DataFrame(transactions, columns=['Date', 'Team', 'Transaction Type', 'Player', 'Description'])

    # Sort by Team name first, then by Transaction Type
    df = df.sort_values(by=['Team', 'Transaction Type'])

    # Display the sorted DataFrame
    pd.set_option('display.max_rows', None)  # Show all rows
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        df.to_excel(file_path, index=False)


    # Load workbook and worksheet
    wb = load_workbook(file_path)
    ws = wb.active

    # Autofit column width
    for col in ws.columns:
        max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2  # Add padding

    # Save adjusted Excel file
    wb.save(file_path)
    print(f"Saved {file_path} with autofit columns.")
else:
    print('No transaction data available.')