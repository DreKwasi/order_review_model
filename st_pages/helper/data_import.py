import vaex as vx
import os
import pandas as pd
import datetime as dt
import streamlit as st


# path = os.path.dirname(os.getcwd())

def date_parser(x):
    return dt.datetime.strptime(x, "%d/%m/%Y")

@st.experimental_memo
def parse_data():
    # Imports data
    parse_dates = ['Sale Date']

    try:
    # You can try both to check speed of import
        data = vx.from_csv("st_pages/cleaned_data.csv", parse_dates=['Sale_Date'], date_parser=pd.to_datetime)
    except FileNotFoundError:
        st.error("Upload Dispensation Data")
        st.stop()

    return data


@st.experimental_memo
def read_stock():
    try:
        data = pd.read_csv("st_pages/cleaned_stock_balance.csv")
        return data
    except FileNotFoundError:
        st.error("Upload Inventory Overview Data")
        st.stop()
