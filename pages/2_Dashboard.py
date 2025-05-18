import streamlit as st
from Modules import VisualHandler
import pandas as pd
from Report import SchoolAnalytics
def take_data(file):
    df = pd.read_excel(file)
    return df
VisualHandler.initial()
school = SchoolAnalytics()
def display_dasboard():
    if st.session_state.log == True:
        col1, col2, col3 = st.columns(3)
        col1.metric("Student", "1250", "1.2%", border = True)
        col2.metric("Teachers", "50", "-8%", border = True)
        col3.metric("Earning", "$240000", "5%", border = True)
         ############### Class Tab ################

        cl1, cl2 = st.columns([0.5,0.5])
        with cl1:
            term = st.selectbox("Term", school.take_term())
        with cl2:
            year = st.selectbox("Year", school.take_year())


        st.divider()
        #st.map(school.get_student_locations_df(term, year))
        st.divider()

        ############### Class Tab ################


        tab1, tab2 = st.tabs(["Overall","Class"])
        with tab1:
            st.subheader("Top students")
            st.dataframe(school.top_students_overall(term, year, top_n = 2))
            st.divider()
            ############### Class Tab ################
            cols1, cols2 = st.columns([0.5,0.5])
            with cols1:
                st.subheader("Subject Wise Top Students")
            with cols2:
                subject_name = st.selectbox("Subject",school.take_subject())
            st.dataframe(school.top_students_per_subject(term, year,top_n = 3, subject_name = subject_name))
            st.subheader("Students Scorecard")
            student_id = st.text_input("Student ID", placeholder = "Enter Student ID")
            try:
                sc_class_name, sc_student_name, sc_df, sc_overall_score = school.generate_scorecard(student_id, term, year)
                with st.container():
                    st.write(f"Score card for {sc_student_name}") 
                    st.write(f"Class name: {sc_class_name}")
                    st.dataframe(sc_df)
                    st.write(f"Overall score: {sc_overall_score}")
            except:
                st.warning(school.generate_scorecard(student_id, term, year))   
            
            st.divider()
            st.subheader("Teacher load")
            st.dataframe(school.generate_teacher_load(term, year))
            ############### Class Tab ################
            
        with tab2:
            ############### Class Tab ################
        
            column1, column2= st.columns([0.5,0.5])
            with column1:
                st.subheader("Class Average Score")
            with column2:
                class_name = st.selectbox("Class", school.take_class_name())
            st.dataframe(school.generate_class_average_score(class_name,term,year))
            st.divider()
            col1, col2 = st.columns([0.5, 0.5])
            with col1:
                st.subheader("Top Students")
            st.dataframe(school.top_students_per_class(class_name, term, year, top_n = 2))




display_dasboard()