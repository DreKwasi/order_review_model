import streamlit as st
import os
import pandas as pd


# Page settings
st.set_page_config(page_title="Order Review Model",
                   page_icon=":bar_chart", layout="wide")


# Sidebar settings
st.sidebar.title("Order Review Model Analysis")
files = os.listdir("pages")

for file in files:
    if ".csv" in file:
        os.remove(f"pages/{file}")

dispensation = st.sidebar.file_uploader(
    "Upload Dispensation Data", type="csv"
)
dispensation_template = pd.read_csv(
    "pages/templates/dispensation_template.csv")
st.sidebar.download_button("Download Dispensation Template", dispensation_template.to_csv(index=False),
                           "dispensation_template.csv", "text/csv", key='download-disp')

stock = st.sidebar.file_uploader(
    "Upload Inventory Overview Data", type="csv"
)
stock_balance_template = pd.read_csv(
    "pages/templates/stock_balance_template.csv")
st.sidebar.download_button("Download Stock Balance Template", stock_balance_template.to_csv(index=False),
                           "stock_balance_template.csv", "text/csv", key='download-stk')
# image = ''
# st.sidebar.image(image, use_column_width=True)


if dispensation is not None:
    if dispensation.name != "cleaned_data.csv":
        st.error("Upload the Right Dispensation Data")
    else:
        with open(os.path.join("pages", dispensation.name), "wb") as f:
            f.write(dispensation.getbuffer())
            st.success("Saved Dispensation")

if stock is not None:
    if stock.name != "cleaned_stock_balance.csv":
        st.error("Upload the Right Stock Balance Data")
    else:
        with open(os.path.join("pages", stock.name), "wb") as f:
            f.write(stock.getbuffer())
            st.success("Saved Stock Balance")


# About the GDELT Project
with st.expander("About this App"):
    st.markdown("""
    The Order Review Project monitors compares the month-on-month dispensation of Retail Facilities with 
    their respective monthly demand.

    Given the difficulty in attaining appreciable fulfillment levels within a give timeframe,
    the Order Review Model provides a unique approach fulfilling 'rational' demand across the various facilities.

    The Order Review Model ascertain a facilities demand as a function of their Stock Balance, Product Category,
    Facility & Regional Dispensation of Product and finally Withdrawal Patterns (Facility/Warehouse Initiated)
    
    In future models, a forecast model will be trained using the factors mentioned above to ascertain consistent
    and progressive demand thus reducing the JIT model of procurement to a more sustainable approach.
    """)

# About the data we are using
with st.expander("The Dataset"):
    st.markdown("""
    This app uses Data from Metabase which is curated from the flagship POS Software of the Facilities.
    
    This includes;
     - [Dispensation Data](https://metabase.mpharma.datacoral.io/question/2662-dispensation-data-for-order-review-model)
     - [Facility Stock Balance Data](https://metabase.mpharma.datacoral.io/question/2667-stock-balance-data-for-order-review)

    Email all Raw Downloaded Data to [Andrews Asamoah Boateng](andrews.boateng@mpharma.com) for Data Cleanup and Prepping
    """)

# How to use the app
with st.expander("How to use the app"):
    st.markdown("""
    About Page
     - Upload all preliminary data i.e. Dispensation and Stock Balance Data before proceeding in app
     - Proceed to the Next Page Only After Getting a Prompt that the Upload for Both Files are completed

    Dispensation Page
     - You can expore the demand for all Facilities Here
     - Toggle the Date Range, Facility, Product, Category and Location to Get An Overview of the Demand

    Order Review
     - This is where all the fun is; Upload an Order (csv format only) you wish to review
     - Ensure the Column Structure of the File is same as the Template File Provided
     - After Upload, Choose the Facility you wish to Review which will be followed a 
        brief stats overview of the Order and the Facility's Dispensation
     - Toggle the Review Checkbox to Review the Quantities of the Line Items. 
        (This is followed by a summary below as well)
     -Optionally you can also constrain the time period for which you are interested in.
    """)

# About Vaex
with st.expander("About Vaex"):
    st.markdown("""
    Vaex is high performance DataFrame library in Python that allows for fast processing on very large
    datasets on a single node. With its efficient algorithms, Vaex can go over *a billion* samples per second.
    Using memory mapping techniques, Vaex can work with datasets that are much larger then RAM.

    This makes Vaex a perfect backend choice for a variety of dashboards and data applications.

    Vaex is open source and available on [Github](https://github.com/vaexio/vaex/).
    A variety of relevant resources can be found [here](https://vaex.io/).
    """)


# Made by section - footer in the sidebar
st.sidebar.markdown('''
### Made with ❤️ by:
 - [Andrews Asamoah Boateng](https://www.linkedin.com/in/aaboateng/)
''')
