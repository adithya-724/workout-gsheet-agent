import gspread
from gspread.utils import rowcol_to_a1
from google.oauth2.service_account import Credentials
import os
import streamlit as st

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
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


def add_values_to_sheet(sample_values):
    creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1-19g2yEjeGBToSOw5lTnmKPnREehoSf6rNNq3zC4wUk")
    worksheet = sheet.worksheet("Tracker")

    values_to_add = list(sample_values.values())
    values_to_add = [values_to_add[0], values_to_add[1], "", "", *values_to_add[2:]]

    start_row = get_next_row()
    st.write(f"Writing on row  {start_row}")

    # start_col = 2  # Column B

    # # Calculate the ending column letter based on the number of values
    # end_col_letter = chr(ord("A") + start_col + len(values_to_add) - 1)
    # cell_range = f"B{start_row}:{end_col_letter}{start_row}"

    start_col = 2
    end_col = start_col + len(values_to_add) - 1

    range_start = rowcol_to_a1(start_row, start_col)  # e.g. B12
    range_end = rowcol_to_a1(start_row, end_col)  # e.g. D12

    cell_range = f"{range_start}:{range_end}"
    worksheet.update(cell_range, [values_to_add])

    # worksheet.update(range_name=cell_range, values=[values_to_add])
