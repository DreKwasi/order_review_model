import vaex as vx
import os
import pandas as pd
import datetime as dt


path = os.path.dirname(os.getcwd())

def date_parser(x):
    return dt.datetime.strptime(x, "%d/%m/%Y")

def load_data():

    # Imports data
    parse_dates = ['Sale Date']

    # You can try both to check speed of import

    try:
        # data = vx.open('%s//data//cleaned_data.csv.hdf5' % path)
        raise(FileNotFoundError)
    except (FileNotFoundError):
        data = vx.from_csv('%s//data//cleaned_data.csv' % path, parse_dates=['Sale_Date'], date_parser=pd.to_datetime)

    return data

def load_stock_balance():
    data = pd.read_csv('%s//data//cleaned_stock_balance.csv' % path)
    return data