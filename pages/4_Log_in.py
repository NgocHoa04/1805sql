import streamlit as st
from Modules import VisualHandler
VisualHandler.initial() 
import streamlit as st

# Dummy user credentials
users = {
    "student01": "password123",
    "student02": "mypassword",
    "admin": "admin123"
}

def display_login():
    if st.session_state.log == False:
        st.title("🔐 Login")

        st.subheader("Please enter your credentials:")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.log = True
                st.success(f"Welcome, {username}!")
                st.switch_page("pages/2_Dashboard.py")
            else:
                st.error("Invalid username or password.")
    else:
        st.switch_page("pages/2_Dashboard.py")
display_login()
