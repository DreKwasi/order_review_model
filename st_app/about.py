import streamlit as st


def show_page():

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