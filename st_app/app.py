import streamlit as st

import about
import order_review
import dispensation


# Page settings
st.set_page_config(page_title="Order Review Model", page_icon=":bar_chart", layout="wide")

# Sidebar settings

PAGES = {
    'About this App': about,
    'Visualize Dispensation Data': dispensation,
    'Review SC Monthly Order': order_review
}


# image = ''
# st.sidebar.image(image, use_column_width=True)


st.sidebar.title("Order Review Model Analysis")

page = st.sidebar.radio("Navigation", list(PAGES.keys()))

# Display the selected page in the main viewport
PAGES[page].show_page()

# Made by section - footer in the sidebar
st.sidebar.markdown('''
### Made with ❤️ by:
 - [Andrews Asamoah Boateng](https://www.linkedin.com/in/aaboateng/)
''')

# st.sidebar.image('./logos/logo-white.png', use_column_width=True)

# END OF SCRIPT
