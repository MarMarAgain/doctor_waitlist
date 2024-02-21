import gspread
from google.oauth2.service_account import Credentials
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
    print("Please enter the current Month for validation")

    while True:
        data_str = input("Enter the Month here: ")
        print(f"The Month you provided is {data_str}\n")
        print(f"Converting data now...\n")

        try:
            validate_data(data_str)
            # Return the validated month
            selected_month = data_str
            return selected_month
        except ValueError as e:
            print(f"Invalid data {e}. Please try again\n")


current_month = datetime.now().month


def validate_data(data_str):
    # Raise an error if the user does not enter a Month

    months = ["january", "february", "march", "april", "may", "june",
              "july", "august", "september", "october", "november", "december"]
    if data_str.lower() not in months or data_str.lower() != months[current_month - 1]:
        raise ValueError("Invalid Month entered. Please enter the current Month only")


def get_sheet1_data(selected_month):
    # Open the source worksheet and get values from sheet 1
    source_worksheet = SHEET.worksheet("Sheet1")
    data = source_worksheet.get_all_values()

    # Process the data
    processed_data = []
    regular_hours = 0
    extra_hours = 0
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

        # Check if it's Sunday
        if day.lower() == "sunday":
            extra_hours += float(row[4])  # Assuming duration is in hours
        else:
            regular_hours += float(row[4])  # Assuming duration is in hours

        processed_data.append(
            ["Dance Cork Firkin Crane", area, duration, f"{date} {selected_month.capitalize()} 2024", time])

    return processed_data, regular_hours, extra_hours


def main():
    # Get the month from the user
    selected_month = get_month()

    # Get data from Sheet1
    processed_data, regular_hours, extra_hours = get_sheet1_data(selected_month)

    # Open target worksheet (Sheet2)
    target_worksheet = SHEET.worksheet("Sheet2")

    # Clear previous values in Sheet2
    target_worksheet.clear()

    # Define the titles and corresponding cells
    titles = ["Place", "Area", "Duration", "Date", "Start Time", "Billable Hours (regular)", "Billable Hours (extra)"]

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

    print("Calculating billable hours")

    # Insert regular and extra hours in Sheet2
    target_worksheet.update_cell(2, len(titles) - 1, regular_hours)  # Regular hours
    target_worksheet.update_cell(2, len(titles), extra_hours)  # Extra hours

    print("Changes successful")


main()