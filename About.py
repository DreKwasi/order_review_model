import streamlit as st
import os


# Page settings
st.set_page_config(page_title="Order Review Model",
                   page_icon=":bar_chart", layout="wide")


# Sidebar settings
st.sidebar.title("Order Review Model Analysis")
files = os.listdir("tempDir")

if len(files) != 0:
    for file in files:
        os.remove(f"tempDir/{file}")

dispensation = st.sidebar.file_uploader(
    "Upload Dispensation Data", type="csv"
)

stock = st.sidebar.file_uploader(
    "Upload a Stock Balance file", type="csv"
)
# image = ''
# st.sidebar.image(image, use_column_width=True)


if dispensation is not None:
    if dispensation.name != "cleaned_data.csv":
        st.error("Upload the Right Dispensation Data")
    else:   
        with open(os.path.join("tempDir",dispensation.name),"wb") as f: 
            f.write(dispensation.getbuffer())         
            st.success("Saved Dispensation")

if stock is not None:
    if stock.name != "cleaned_stock_balance.csv":
        st.error("Upload the Right Stock Balance Data")
    else:   
        with open(os.path.join("tempDir",stock.name),"wb") as f: 
            f.write(stock.getbuffer())         
            st.success("Saved Stock Balance")



# About the GDELT Project
with st.expander("About this App"):
    st.markdown("""
    The Order Review Project monitors the month on month orders from Retail facilities.

    Given the fulfillment strain on the Supply Chain Unit, the Order Review Model provides a unique
    perspective on how orders should be processed.

    The Order Review Model employs the Stock Balance, Product Category, Facility & Regional Dispensation of Products
    and in future models the Withdrawal Pattern
    """)

# About the data we are using
with st.expander("The Dataset"):
    st.markdown("""
    This app uses Metabase Data from the flagship POS Software.

    Learn more about this dataset [here](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/).
    """)

# How to use the app
with st.expander("How to use the app"):
    st.markdown("""
    With this app you can explore the various effects of:
        - 
        
    Optionally you can also constrain the time period for which you are interested in.
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
