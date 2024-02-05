import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds4.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Dr_waitlist')

def get_patients_seen_data():
    """
    Get the number of patients seen input from the user for multiple doctors.
    Run a loop to collect valid data from the user via the terminal.
    The loop will repeatedly request data until it is valid.
    """
    headings = ["A", "B","C","D","E","F"]
    patients_seen_data = {}

    for heading in headings:
        while True:
            print(f"Please enter the number of patients seen this month for {heading}.")
            print("Data should be a whole number.")
            print("Example: 10\n")

            data_str = input(f"Enter the number of patients here for {heading}: ")

            try:
                value = int(data_str)
                if heading not in patients_seen_data:
                    patients_seen_data[heading] = []
                patients_seen_data[heading].append(value)
                print("Data is valid!")
                break
            except ValueError:
                print("Invalid input. Please enter a whole number.")

    return patients_seen_data

# Call the function and store the result in a variable
result = get_patients_seen_data()

print (result)


def update_patients_seen_worksheet(result):
    """ Docstring explain"""
print("updating patients seen worksheet ...\n")
patients_seen_worksheet = SHEET.worksheet("patients seen")
patients_seen_worksheet.append_row(result)
print ("patients seen worksheet updated.\n")


update_patients_seen_worksheet (waitlist_data)