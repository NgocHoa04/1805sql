import streamlit as st
import sys
import os
import pandas as pd
from Modules import VisualHandler
VisualHandler.initial()
def take_data():
    df = pd.read_excel("Student_table.xlsx")
    return df
def display_management():
    if st.session_state.log  ==  True:
        tab1, tab2, tab3, tab4 = st.tabs(["Class", "Teachers", "Income", "Grade"])
        with tab1:
            st.header("CLASS MANAGEMENT")
            st.dataframe(take_data())

    else:
            st.warning("Please log in to continue")
display_management()