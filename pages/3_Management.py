import streamlit as st
import sys
import os
import pandas as pd
from Modules import VisualHandler
from Management import Manager
manager = Manager()
VisualHandler.initial()

class Management:
    st.cache_data

    @classmethod
    def more_class(cls):
        add_class_name = st.text_input("Add a new Class", placeholder = "Enter new class name")
        if st.button("Add Class"):
            manager.add_class(add_class_name)
            st.balloons()
    @classmethod
    def delete_class(cls):
        delete_class_name = st.selectbox("Select Class to delete", manager.get_all_classes())
        if st.button("Delete Class"):
            manager.delete_class(delete_class_name)
            st.balloons()
    @classmethod
    def update_class(cls):
        update_class_name = st.selectbox("Select Class to update", manager.get_all_classes())
        new_class_name = st.text_input("Enter new class name")
        cls_id_new = st.text_input("Enter new class ID")
        if st.button("Update Class"):
            manager.update_class(cls_id_new, new_class_name)
            st.balloons()
    @classmethod
    def get_class_students(cls, main_class_id, main_class_name,term, year):
        try:
            # column1 ,column2 = st.columns([0.5,0.5])
            # with column1:
            #     main_class_name = st.text_input("Enter Class Name", placeholder = "Enter class name")
            # with column2:
            #     main_class_id = st.text_input("Enter Class ID", placeholder = "Enter class ID")
            return(manager.get_class_students(main_class_id, main_class_name, term, year))
        except:
            return(manager.get_class_students(main_class_id, main_class_name, term, year))
    @classmethod
    def more_student(cls, main_class_name, term ,year):
        add_student_name = st.text_input("New Student Name", placeholder = "Enter new student name")
        add_student_address = st.text_input("New Student Address ")
        add_student_birthdate = st.date_input("Student Birthdate")
        add_student_email = st.text_input("Student Email")
        if st.button("Add Student in Class"):
            manager.add_student_with_class(add_student_name, add_student_address, add_student_birthdate, add_student_email, main_class_name, term, year)
            st.balloons()
    
    @classmethod
    def update_student(cls):
            st.success("About to fix the update")
        # if st.button("Update Name"):
        #     update_student_name = st.text_input("Enter update student name")
        # update_class_name = st.selectbox("Select Class ", manager.get_all_classes())
        # cls_id_new = st.text_input("Enter new class ID")
        # if st.button("Update Class"):
        #     manager.update_class(cls_id_new, new_class_name)
            #st.balloons()         
    @classmethod
    def delete_student(cls):
        delete_student_id = st.text_input("Enter Student ID to delete")
        try:
            if st.button("Delete Student"):
                manager.delete_student(delete_student_id)
                st.balloons()
        except:
            st.warning(manager.delete_student(delete_student_id))
    @classmethod
    def delete_teacher(cls):
        delete_teacher_id = st.text_input("Enter Teacher ID to delete")
        try:
            if st.button("Delete Teacher"):
                manager.delete_student(delete_teacher_id)
                st.balloons()
        except:
            st.warning(manager.delete_student(delete_teacher_id))
    @classmethod
    def add_teacher(cls):
        add_teacher_name = st.text_input("Add a new Teacher", placeholder = "Enter new teacher name")
        subject_teach = st.selectbox("Select Subject", manager.get_all_subjects(), key = "Add teacher subject")
        subject_teach = int(subject_teach.split(",")[0].strip())
        add_teacher_email = st.text_input("Add a new Teacher", placeholder = "Enter new teacher email")
        if st.button("Add Teacher"):
            manager.add_teacher(add_teacher_name, subject_teach, add_teacher_email)
            st.balloons()
    @classmethod
    def update_teacher(cls):
        update_teacher_id = st.text_input("Enter Teacher ID to update")
        update_teacher_name = st.text_input("Enter Teacher Name")
        long_sj_id = st.selectbox("Select Subject", manager.get_all_subjects(), key = "update teacher subject")
        update_teacher_subject_id = int(long_sj_id.split(",")[0].strip())
        update_teacher_email = st.text_input("Enter Teacher Email")
    
        try:
            if st.button("Update Teacher In4"):
                manager.update_teacher(update_teacher_id, update_teacher_name,  update_teacher_subject_id, update_teacher_email)
                st.success("Update successful")
        except:
            st.warning(manager.update_student( update_teacher_id, update_teacher_name, update_teacher_subject_id, update_teacher_email))
    @classmethod
    def get_class_bill(cls, term, year):
        try:
            st.dataframe(manager.get_fee_by_class_term_year( term, year))
            st.success("Got the fee load for Class")
        except:
            st.warning(manager.get_fee_by_class_term_year(term, year))
    @classmethod
    def get_student_fee_load(cls):
        student_fee_id = st.text_input("Enter Student ID to get fee load")
        if st.button("Take Student Fee Load"):
            try:
                st.dataframe(manager.get_fee_summary_by_student(student_fee_id))
                st.success("Got the fee load")
            except:
                st.warning(manager.get_fee_summary_by_student(student_fee_id))


    @classmethod
    def display_management(cls):
        if st.session_state.log  ==  True:
            tab1, tab2, tab3, tab4 = st.tabs(["Class", "Teachers", "Student", "Grade"])
            with tab1:
                st.header("CLASS MANAGEMENT")                
                col1, col2,col3 = st.columns([1,1,1], border = True)
                with col1:
                    cls.more_class()
                with col2:
                    cls.delete_class()
                with col3:
                    cls.update_class()
############### Class Tab ################
                st.subheader("Class List")
                if st.button("Show all classes"):
                    st.dataframe(manager.get_all_classes())
                st.divider()
                cl1, cl2 = st.columns([0.5,0.5])
                with cl1:
                    term = st.selectbox("Term", manager.get_all_term(), key = "Class term")
                with cl2:
                    year = st.selectbox("Year", manager.get_all_year(), key = "Class year")
                st.divider()
############### Class Tab ################
                column1 ,column2 = st.columns([0.5,0.5])
                with column1:
                    main_class_id = st.text_input("Enter Class ID", placeholder = "Enter class ID")
                with column2:
                    main_class_name = st.text_input("Enter Class Name", placeholder = "Enter class name")
                
                if main_class_id.isdigit():
                    main_class_id = int(main_class_id)
                    st.dataframe(manager.find_class(main_class_id, main_class_name, term, year))
                    st.balloons()
                else:
                    st.warning("Please enter a valid numeric Class ID.")
                    main_class_id = None  # or return early
                
                if st.button("Show all students in class"):
                    try:
                        st.dataframe(cls.get_class_students( main_class_id, main_class_name,term, year))
                    except:
                        st.warning(cls.get_class_students( main_class_id,main_class_name,term, year))
                st.divider()
############### Class Tab ################
                st.subheader("Class Schedule")
                st.dataframe(manager.get_class_schedule(main_class_id, main_class_name, term, year))
############### Class Tab ################
                st.subheader("Manage Student Information")
                clm1, clm2, clm3 = st.columns([1,1,1])
                with clm1:
                    cls.more_student(main_class_name, term, year)
                with clm2:
                    cls.delete_student()
                with clm3:
                    cls.update_student()
                st.divider()
############### Class Tab ################
                st.subheader("Class Fee Load")
                cls.get_class_bill(term, year)
                st.divider()
            with tab2:
                st.header("TEACHER MANAGEMENT")
                st.divider()
############### Class Tab ################
                if st.button("Show all teachers"):
                    st.subheader("All Teachers")
                    st.dataframe(manager.get_all_teachers())
                st.divider()
############### Class Tab ################
                ############### Class Tab ################
                teachcl1, teachcl2 = st.columns([0.5,0.5])
                with teachcl1:
                    teacher_term = st.selectbox("Term", manager.get_all_term(), key = "teacher term")
                with teachcl2:
                    teacher_year = st.selectbox("Year", manager.get_all_year(), key = "teacher year")
                ############### Class Tab ################
                st.subheader("Find Teacher")
                find_teacher_id = st.text_input("Enter Teacher ID", placeholder = "Enter teacher ID")
                find_teacher_name = st.text_input("Enter Teacher Name", placeholder = "Enter teacher name")
                if st.button("Find Teacher", key = "find teacher button"):
                    st.dataframe(manager.find_teacher(find_teacher_id, find_teacher_name))
                st.divider()

                st.subheader("Teacher Schedule")
                st.dataframe(manager.get_teacher_schedule(find_teacher_id, teacher_term, teacher_year))
                st.divider()
############### Class Tab ################
                col1, col2,col3 = st.columns([1,1,1], border = True)
                with col1:
                    cls.add_teacher()
                with col2:
                    cls.delete_teacher()
                with col3:
                    cls.update_teacher()
                ############### Class Tab ################
                st.divider()
            
                
               
                    



if st.session_state.log == True:
    Management.display_management()
else:
    st.warning("Please log in to continue")