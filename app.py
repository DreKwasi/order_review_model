import streamlit as st
from streamlit_option_menu import option_menu
from st_pages.dispensation import show_disp
from st_pages.order_review import show_review
from st_pages.about import show_about


# Page settings
st.set_page_config(page_title="Order Review Model",
                   page_icon=":bar_chart", layout="wide")

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
