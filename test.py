import gspread
from gspread.utils import rowcol_to_a1
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
ROW_TRACK_FILE = "row_tracker.txt"


def is_valid_date(s):
    try:
        datetime.strptime(s.strip(), "%m/%d/%Y")
        return True
    except ValueError:
        return False


def get_next_row():
    creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1-19g2yEjeGBToSOw5lTnmKPnREehoSf6rNNq3zC4wUk")
    worksheet = sheet.worksheet("Tracker")
    date_col = worksheet.col_values(2)  # Column A
    last_valid_row = 1

    for i, val in enumerate(date_col, start=1):
        if val.strip().lower() == "date":
            continue
        if is_valid_date(val):
            last_valid_row = i

    return last_valid_row + 1


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
