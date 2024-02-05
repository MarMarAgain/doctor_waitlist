import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds3.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Dr_waitlist')

def get_patients_seen_data():
    """
    Get the number of patients seen input from the user for multiple doctors.
    Run a loop to collect valid data from the user via the terminal.
    The loop will repeatedly request data until it is valid.
    """
    headings = ["DR. Hough", "DR. O'Flynn", "DR. Carey", "Dr. Poland", "Dr. Lehan", "Dr. Burke"]
    patients_seen_data = {}

    for heading in headings:
        while True:
            print(f"Please enter the number of patients seen this month for {heading}.")
            print("Data should be a whole number.")
            print("Example: 10\n")

            data_str = input(f"Enter ythe number of patients here for {heading}: ")

            try:
                value = int(data_str)
                if heading not in patients_seen_data:
                    patients_seen_data[heading] = []
                patients_seen_data[heading].append(value)
                print("That isn't a valid number!!")
                break
            except ValueError:
                print("Invalid input. Please enter a whole number.")

    return patients_seen_data

'Call the function and store the result'
patients_seen_data_result = get_patients_seen_data()

'Print the result'
print("\nPatients Seen Data:")
for doctor, values in patients_seen_data_result.items():
    print(f"{doctor}: {values}")

