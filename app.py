import streamlit as st
from streamlit_option_menu import option_menu
from st_pages.dispensation import show_disp
from st_pages.order_review import show_review
from st_pages.about import show_about
import streamlit_authenticator as stauth


# Page settings
st.set_page_config(page_title="Order Review Model",
                   page_icon=":bar_chart", layout="wide")


# User Authentication
login_cred = dict(st.secrets(["login_cred"]))
cookie = dict(st.secrets(["cookie"]))

authenticator = stauth.Authenticate(
    login_cred,
    cookie['name'],
    cookie['key'],
    cookie['expiry_days'])

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter a username and password")

if authentication_status:
    selected = option_menu(menu_title=None, options=[
                        "Home", "Dispensation", "Order Review"],
                        icons=["house", "graph-up-arrow", "arrow-repeat"],
                        default_index=0, orientation="horizontal")


    if selected == "Home":
        show_about()
    if selected == 'Dispensation':
        show_disp()
    if selected == "Order Review":
        show_review()

    authenticator.logout("Logout", "sidebar")