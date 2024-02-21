import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from datetime import datetime

SCOPE = [
   "https://www.googleapis.com/auth/spreadsheets",
   "https://www.googleapis.com/auth/drive.file",
   "https://www.googleapis.com/auth/drive"
]

# Load Credentials and Access spreadsheet
CREDS = Credentials.from_service_account_file('dcfccreds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('DCFC cleaning')

def get_month():
    """Get month desired from user"""
    print("Please enter the month you wish to translate")
    print("Write the Month with a capital letter at the beginning - ex: 'March'")

    while True:
        data_str = input("Enter the Month here: ")
        #Changed to .format method as codeanywhere has python version 3.5. Tried to upgrade and encountered further error messages.
        print("The Month you provided is {}".format(data_str))
        print("Converting data now...\n")

        try:
            validate_data(data_str)
            # Return the validated month
            selected_month = data_str
            return selected_month
        except ValueError as e:
            print(f"Invalid data {e}. Please try again\n")


def validate_data(data_str):
    # Raise an error if the user does not enter a Month

    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    if data_str not in months:
        raise ValueError("Invalid month format. Please enter the month with a capital letter at the beginning, e.g., 'March'.")


def get_sheet1_data(selected_month):
    # Open the source worksheet and get values from sheet 1
    source_worksheet = SHEET.worksheet("Sheet1")
    data = source_worksheet.get_all_values()

    # Process the data
    processed_data = []
    previous_date = None
    for row in data:
        date = row[0]

        # Check if the date cell is empty
        if not date:
            """If the date cell is empty and there's no previous date, skip the row 
            ( so that there isnt an error at the beginning of a loop). This will effectively skip two empty cells together"""
            if previous_date is None:
                continue
            else:
                # Use the previous complete date( if there is only one empty cell, use the previous date)
                date = previous_date

        # Update the previous date
        previous_date = date

        # Extract other information from the row
        day = row[1]
        area = row[2]

        # Changing any "JLH" to "Jack Lynch House"
        if area == 'JLH':
            area = 'Jack Lynch House'
        time = row[3]
        # Changing DCFC format hours to Angel Cleaning format hours. I chose 7 and 1 respectively as identifiers
        if '7' in time:
            time = '7am'
        elif '1pm' in time:
            time = '10am'
        # Formatting duration
        duration = f"{row[4]} hrs" 
        if duration == " hrs":
            continue 
        processed_data.append(["Dance Cork Firkin Crane", area, duration, f"{date} {selected_month} 2024", time])

    return processed_data


def main():
    # Get the month from the user
    selected_month = get_month() 

    # Get data from Sheet1
    processed_data = get_sheet1_data(selected_month)

    # Open target worksheet (Sheet2)
    target_worksheet = SHEET.worksheet("Sheet2")

    # Clear previous values in Sheet2
    target_worksheet.clear()
    
    # Define the titles and corresponding cells 
    titles = ["Place", "Area", "Duration", "Date", "Start Time"]

    # Apply bold formatting to the titles row
    bold_format = {
        "textFormat": {"bold": True}
    }
    for i, title in enumerate(titles, start=1):
        target_worksheet.update_cell(1, i, title)
        target_worksheet.format(f"{chr(64 + i)}1", bold_format)

    # Write processed data to the target worksheet. Start from the second row/column
    for i, row in enumerate(processed_data, start=2): 
        target_worksheet.insert_row(row, i)

    print("Changes Successful")

main()