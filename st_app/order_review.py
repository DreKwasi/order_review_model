from dispensation import human_format
import datetime as dt
import folium as fl
import pyarrow as pa
from datetime import datetime
from data_import import load_data, load_stock_balance
import plotly_express as px
import vaex as vx
import numpy as np
import pandas as pd
import streamlit as st


if not vx.cache.is_on():
    vx.cache.on()

vx_df = load_data()
vx_df = vx_df._future()

stk_df = load_stock_balance()


def merge_order(df, vx_df, facility, location, date_range):

    df_max = vx_df['Sale_Date'].values.max()

    differences = {"All Time": np.timedelta64(730, "D"),
                   "Past 12 months": np.timedelta64(365, "D"),
                   "Past 6 months": np.timedelta64(180, "D"),
                   "Past 3 months": np.timedelta64(90, "D"),
                   "Past Month": np.timedelta64(30, "D")
                   }

    df_min = df_max - differences[date_range]
    vx_df = vx_df[vx_df.Sale_Date >= df_min]

    facility_df = vx_df[vx_df['Sale_Facility'] == facility]
    location_df = vx_df[vx_df['LOCATION'] == location]
    stock_df = stk_df[stk_df['facility_name'] == facility]

    facility_gp = facility_df.groupby(
        by=['Product_Description'], agg={"Packs_Sold": "sum"})
    facility_gp = facility_gp.to_pandas_df()

    regional_gp = location_df.groupby(
        by=['Product_Description'], agg={"Packs_Sold": "sum"})
    regional_gp = regional_gp.to_pandas_df()

    df['Packs Dispensed (Facility Level)'] = 0
    df['Packs Dispensed (Regional Level)'] = 0
    df['Stock Balance (Facility Level)'] = 0
    

    for index, row in df.iterrows():
        facility_match = facility_gp[facility_gp['Product_Description']
                                     == row['DRUG ']]
        df.loc[index, 'Packs Dispensed (Facility Level)'] = facility_match['Packs_Sold'].values[0] if len(
            facility_match['Packs_Sold'].values) > 0 else 0

        region_match = regional_gp[regional_gp['Product_Description']
                                   == row['DRUG ']]
        df.loc[index, 'Packs Dispensed (Regional Level)'] = region_match['Packs_Sold'].values[0] if len(
            region_match['Packs_Sold'].values) > 0 else 0

        stock_match = stock_df[stock_df['product_name'] == row['DRUG ']]
        df.loc[index, 'Stock Balance (Facility Level)'] = stock_match['Stock Balance'].values[0] if len(
            stock_match['Stock Balance'].values) > 0 else 0


def compute_final(df):
    df['Final Requested Quantity'] = 0
    df['Excess Variance'] = 0

    for index, row in df.iterrows():
        if row['Packs Dispensed (Facility Level)'] < row['QUANTITY ']:
            dispensation_factor = (
                row['Packs Dispensed (Facility Level)'] / row['QUANTITY ']) * 0.5
        else:
            dispensation_factor = 0.5

        if row['Packs Dispensed (Regional Level)'] < row['QUANTITY ']:
            location_factor = (
                row['Packs Dispensed (Regional Level)']) / row['QUANTITY '] * 0.25
        else:
            location_factor = 0.25

        perm_stk = row['QUANTITY '] * 0.25
        if row['Stock Balance (Facility Level)'] > perm_stk:
            balance = row['Stock Balance (Facility Level)'] - perm_stk
            if balance > row['QUANTITY ']:
                stock_factor = 0
            else:
                stock_factor = (1 - (balance / row['QUANTITY '])) * 0.25
        else:
            stock_factor = 0.25
        total_factor = dispensation_factor + location_factor + stock_factor
        final_qty = np.round(total_factor * row['QUANTITY '], decimals=0)
        df.loc[index, 'Final Requested Quantity'] = 1 if final_qty < 1 else final_qty

    df['Total After Review'] = df['Final Requested Quantity'] * df['PRICE']
    df['Excess Variance'] = np.round(df['QUANTITY '] - df['Final Requested Quantity'], decimals=2)


def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


def show_page():
    st.sidebar.header("User Inputs")
    file = st.sidebar.file_uploader(
        "Upload a csv file", type="csv"
    )
    facility = st.sidebar.multiselect(
        "Select Facility:", vx_df['Sale_Facility'].unique(), default=None)


    if facility == []:
        location = st.sidebar.multiselect(
            "Select Location:", options=vx_df['LOCATION'].unique())
        if location == []:
            st.warning("Select Facility or Location")
            st.stop()
    else:
        location = vx_df[vx_df['Sale_Facility'].isin(
            facility)]['LOCATION'].unique()
        st.sidebar.multiselect(
            "Select Location:", options=vx_df['LOCATION'].unique(), default=location)

    date_range = st.sidebar.select_slider(
        label='Date Range',
        options=["Past Month", "Past 3 months",
                "Past 6 months", "Past 12 months", "All Time", ],
        value=("All Time"),
        help='Select a date range.',
    )

    if file and facility:
        new_df = pd.read_csv(file)
        merge_order(df=new_df, vx_df=vx_df,
                    facility=facility[0], location=location[0], date_range=date_range)
        new_df = new_df.round(decimals=2)
        st.header(facility[0])
        st.subheader("Stats")

        metrics = st.columns(4)
        metrics[0].metric(label='Total Order Value',
                          value=f"GHS {human_format(sum(new_df['TOTAL']))}")
        metrics[1].metric(label='Total Packs Requested',
                          value=f"{human_format(sum(new_df['QUANTITY ']))}")
        st.subheader("Order Data")
        with st.expander("View Raw Data"):
            st.dataframe(new_df)
        df = new_df.copy()
        review = st.checkbox("Review Order", on_change=compute_final(df))

        order_chart_options = st.multiselect("Compare Order Quantity With:", options=[
            "Stock Balance", "Regional Sales", "Dispensed Sales"], default="Dispensed Sales")

        order_cols = {
            "Stock Balance": "Stock Balance (Facility Level)",
            "Regional Sales": "Packs Dispensed (Regional Level)",
            "Dispensed Sales": "Packs Dispensed (Facility Level)",
            
        }
        chart_y = ["QUANTITY ", ]

        for option in order_chart_options:
            chart_y.append(order_cols[option])

        fig_1 = px.bar(df, x="DRUG ", y=chart_y, barmode='group')
        with fig_1.batch_update():
            fig_1.update_layout(coloraxis_showscale=False)
            fig_1.update_layout(width=1000, height=700, title="Comparing Order Against Various Metrics")

        st.plotly_chart(fig_1)

        

        if review:
            message = st.success(
                "Bingo!!! Requested Quantities Have Been Reviewed")
            
            st.subheader("Review Order Data")

            csv = convert_df(df)
            st.download_button("Press to Download", csv, "file.csv", "text/csv", key='download-csv')

            with st.expander("Expand Data"):
                metrics[2].metric(label='Total Order Value After Review',
                                  value=f"GHS {human_format(sum(df['Total After Review']))}")
                metrics[3].metric(label='Total Packs After Review',
                                  value=f"{human_format(sum(df['Final Requested Quantity']))}")

                st.dataframe(df)

            compare_option = st.multiselect("Compare Order Quantity With:", options=[
                "Stock Balance", "Regional Sales", "Dispensed Sales", "Reviewed Quantity","Excess Variance"], default="Reviewed Quantity")

            compare = {
                "Stock Balance": "Stock Balance (Facility Level)",
                "Regional Sales": "Packs Dispensed (Regional Level)",
                "Dispensed Sales": "Packs Dispensed (Facility Level)",
                "Reviewed Quantity": "Final Requested Quantity",
                "Excess Variance" : "Excess Variance"
            }
            bar_y = ["QUANTITY ", ]

            for option in compare_option:
                bar_y.append(compare[option])

            fig = px.bar(df, x="DRUG ", y=bar_y, barmode='group')
            with fig.batch_update():
                fig.update_layout(coloraxis_showscale=False)
                fig.update_layout(width=1000, height=700, title="Comparing Order Against Various Metrics")
                

            st.plotly_chart(fig)

    else:
        st.stop()