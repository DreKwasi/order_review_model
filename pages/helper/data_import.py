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

    # You can try both to check speed of import
    data = vx.from_csv("pages/cleaned_data.csv", parse_dates=['Sale_Date'], date_parser=pd.to_datetime)

    return data


@st.experimental_memo
def read_stock():
    data = pd.read_csv("pages/cleaned_data.csv")
    return data