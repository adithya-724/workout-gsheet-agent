import gspread
from gspread.utils import rowcol_to_a1
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime
from time import time

# from dotenv import load_dotenv
import json

# load_dotenv()


SHEET_ID = st.secrets["WORKSHEET_ID"]
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
ACCOUNT = json.loads(st.secrets["service_account"])

creds = Credentials.from_service_account_info(ACCOUNT, scopes=SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID)


def is_valid_date(s):
    try:
        datetime.strptime(s.strip(), "%m/%d/%Y")
        return True
    except ValueError:
        return False


def get_next_row():
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
    worksheet = sheet.worksheet("Tracker")

    values_to_add = list(sample_values.values())
    try:
        values_to_add[0] = values_to_add[0].strip().replace("'", "")
    except Exception:
        pass
    values_to_add = [values_to_add[0], values_to_add[1], "", "", *values_to_add[2:]]

    start_row = get_next_row()
    st.warning(f"Writing to row  {start_row}")

    start_col = 2
    end_col = start_col + len(values_to_add) - 1

    range_start = rowcol_to_a1(start_row, start_col)  # e.g. B12
    range_end = rowcol_to_a1(start_row, end_col)  # e.g. D12

    cell_range = f"{range_start}:{range_end}"
    st.write(values_to_add)
    try:
        worksheet.update(cell_range, [values_to_add])
        st.success("👍")
        time.sleep(5)
        st.rerun()
    except Exception as e:
        st.error("👎")
        print(e)
