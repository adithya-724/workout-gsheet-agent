import gspread
from google.oauth2.service_account import Credentials
import os

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPE)

client = gspread.authorize(creds)

sheet = client.open_by_key("1-19g2yEjeGBToSOw5lTnmKPnREehoSf6rNNq3zC4wUk")


worksheet = sheet.worksheet("Tracker")
values_to_add = [
    "value1",
    "value2",
    "value3",
    "value4",
]  # Replace with your actual values


# Add the values from C120 onwards, for as many columns as there are values in the list


ROW_TRACK_FILE = "row_tracker.txt"


def get_next_row(start=120):
    if os.path.exists(ROW_TRACK_FILE):
        with open(ROW_TRACK_FILE, "r") as f:
            last_row = int(f.read().strip())
            next_row = last_row + 1
    else:
        next_row = start
    with open(ROW_TRACK_FILE, "w") as f:
        f.write(str(next_row))
    return next_row


start_row = get_next_row()
print(start_row)
start_col = 3  # Column C

# Calculate the ending column letter based on the number of values
end_col_letter = chr(ord("A") + start_col + len(values_to_add) - 1)
cell_range = f"C{start_row}:{end_col_letter}{start_row}"

worksheet.update(range_name=cell_range, values=[values_to_add])
