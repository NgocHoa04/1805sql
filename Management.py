import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
import tempfile
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

class Manager:
    @staticmethod
    def connect_db():
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=os.getenv("DB_NAME")
            )
            if connection.is_connected():
                print("Connected to MySQL database")
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    @staticmethod
    def fetch_data(query):
        connection = Manager.connect_db()
        if connection:
            try:
                # Sử dụng pandas để đọc dữ liệu từ truy vấn SQL
                df = pd.read_sql(query, connection)
                return df
            except Error as e:
                print(f"Error executing query: {e}")
                return None
            finally:
                connection.close()
                print("MySQL connection closed")
        return None
    @staticmethod
    def get_all_term():
        query = "SELECT DISTINCT Term FROM Academic_period"
        df = Manager.fetch_data(query)
        try:
            result = tuple(row['Term'] for _,row in df.iterrows())
            return result
        except Exception as e:
            return(f"Error: {e}")
        
    @staticmethod
    @staticmethod
    def get_all_year():
        query = "SELECT DISTINCT Year FROM Academic_period"
        df = Manager.fetch_data(query)
        try:
            result = tuple(row['Year'] for _,row in df.iterrows())
            return result
        except Exception as e:
            return(f"Error: {e}")
        

    @staticmethod
    def get_all_classes():
        query = "SELECT ClassID, ClassName FROM Classes"
        df = Manager.fetch_data(query)
        if df is not None and not df.empty:
            result = tuple(f"{row['ClassID']}, {row['ClassName']}" for _, row in df.iterrows())
            return result
        return ()

    @staticmethod
    def add_class(class_name):
        try:
            conn = Manager.connect_db()
            cursor = conn.cursor()
            cursor.callproc('AddClass', [class_name])
            for result in cursor.stored_results():
                new_id = result.fetchone()[0]
            conn.commit()
            return new_id
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    # Update a class
    @staticmethod
    def update_class(class_id, class_name):
        try:
            conn = Manager.connect_db()
            cursor = conn.cursor()
            cursor.callproc('UpdateClass', [class_id, class_name])
            for result in cursor.stored_results():
                affected_rows = result.fetchone()[0]
            conn.commit()
            return affected_rows
        except Error as e:
            return(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    # Delete a class
    @staticmethod
    def delete_class(class_id):
        try:
            conn = Manager.connect_db()
            cursor = conn.cursor()
            cursor.callproc('DeleteClass', [class_id])
            for result in cursor.stored_results():
                affected_rows = result.fetchone()[0]
            conn.commit()
            return affected_rows
        except Error as e:
            print(f"Error: {e}")
            return 0
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_class_list(search_name=None, limit=10):
        """
        Retrieve a list of classes with homeroom teacher, academic period, student count, and notes.
        
        Args:
            search_name (str, optional): Filter classes by name (partial match).
            limit (int): Number of records to return.
        
        Returns:
            pandas.DataFrame: DataFrame containing class details.
        """
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('GetClassList', [search_name, limit])
            classes = []
            for result in cursor.stored_results():
                classes = result.fetchall()
            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(classes)
            return df
        except Error as e:
            print(f"Error executing GetClassList: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def find_class(class_id=None, class_name=None, Term=None, Year=None):
        """
        Find classes by ClassID or ClassName.
        
        Args:
            class_id (int, optional): Exact ClassID to search for.
            class_name (str, optional): Partial ClassName to search for.
        
        Returns:
            pandas.DataFrame: DataFrame containing matching class details (ClassID, ClassName, Notes, 
                            HomeroomTeacher, Term, Year, StudentCount).
        """
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        
        try:
            cursor = conn.cursor(dictionary=True)
            # Ensure class_id is None if not provided or invalid
            class_id = class_id if class_id is not None else None
            cursor.callproc('FindClass', [class_id, class_name, Term, Year])
            classes = []
            for result in cursor.stored_results():
                classes = result.fetchall()
            df = pd.DataFrame(classes)
            return float(df["StudentCount"].iloc[0]), float(df["HomeroomTeacher"].iloc[0])
        except Error as e:
            print(f"Error executing FindClass: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def get_class_students(class_id=None, class_name=None, Term=None, Year=None):
        """
        Retrieve a list of students for a specific class.
        
        Args:
            class_id (int): The ClassID of the class to fetch students for.
        
        Returns:
            pandas.DataFrame: DataFrame containing student details (StudentID, StudentName, Address, BirthDate, Email).
        """
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('GetClassStudents', [class_id, class_name, Term, Year])
            students = []
            for result in cursor.stored_results():
                students = result.fetchall()
            df = pd.DataFrame(students)
            return df
        except Error as e:
            return(f"Error executing GetClassStudents: {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_class_schedule(class_id, class_name, Term, Year):
        """
        Lấy lịch học của một lớp dựa trên ClassID và PerId bằng stored procedure GetClassSchedule.
        
        Parameters:
        - class_id: ID của lớp.
        - per_id (int): ID của kỳ học.
        
        Returns:
        - pandas.DataFrame: DataFrame chứa lịch học với các cột ClassName, TeacherName, SubjectName, 
                            DayOfWeek, StartTime, EndTime, WeekNumber.
        """
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('GetClassSchedule', [class_id, class_name, Term, Year])
            schedules = []
            for result in cursor.stored_results():
                schedules = result.fetchall()
            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(schedules)
            return df
        except Error as e:
            print(f"Error executing GetClassSchedule: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def export_to_excel(df, filename="manager_export.xlsx"):
        """
        Export a DataFrame to an Excel file.
        
        Args:
            df (pandas.DataFrame): DataFrame to export.
            filename (str): Name of the output Excel file (default: 'manager_export.xlsx').
        
        Returns:
            str: Path to the generated Excel file, or None if failed.
        """
        try:
            # Create a temporary file path if filename is not absolute
            if not os.path.isabs(filename):
                temp_dir = tempfile.gettempdir()
                file_path = os.path.join(temp_dir, filename)
            else:
                file_path = filename
            
            # Export DataFrame to Excel
            df.to_excel(file_path, index=False, engine='openpyxl')
            return file_path
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return None
        
#Student         
    @staticmethod
    def add_student_with_class(name, address, birthdate, email,  class_name, Term, Year):
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('AddStudentWithClass', [name, address, birthdate, email, class_name, Term, Year])
            for result in cursor.stored_results():
                data = result.fetchall()
            conn.commit()
            return pd.DataFrame(data)
        except Error as e:
            print(f"Error executing AddStudentWithClass: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_student(student_id):
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('DeleteStudent', [student_id])
            for result in cursor.stored_results():
                data = result.fetchall()
            conn.commit()
            return pd.DataFrame(data)
        except Error as e:
            return(f"Error executing DeleteStudent: {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_student(student_id, name, address, birthdate, email, note = None):
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('UpdateStudent', [student_id, name, address, birthdate, email, note])
            for result in cursor.stored_results():
                data = result.fetchall()
            conn.commit()
            return pd.DataFrame(data)
        except Error as e:
            print(f"Error executing UpdateStudent: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def find_student_detail(student_id=None, student_name=None):
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('FindStudentDetail', [student_id, student_name])
            for result in cursor.stored_results():
                data = result.fetchall()
            return pd.DataFrame(data)
        except Error as e:
            print(f"Error executing FindStudentDetail: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()

#Teacher
    @staticmethod
    def get_all_subjects():
        query = "SELECT SubjectID, SubjectName FROM Subjects"
        df = Manager.fetch_data(query)
        try:
            result = tuple(f"{row['SubjectID']}, {row['SubjectName']}" for _, row in df.iterrows())
            return result
        except Exception as e:
            return(f"Error: {e}")

    @staticmethod
    def add_teacher(name, subject_id, email):
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('AddTeacher', [name, subject_id, email])
            for result in cursor.stored_results():
                data = result.fetchall()
            conn.commit()
            return pd.DataFrame(data)
        except Error as e:
            print(f"Error executing AddTeacher: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_teacher(teacher_id, name, subject_id, email):
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('UpdateTeacher', [teacher_id, name, subject_id, email])
            for result in cursor.stored_results():
                data = result.fetchall()
            conn.commit()
            return pd.DataFrame(data)
        except Error as e:
            print(f"Error executing UpdateTeacher: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def delete_teacher(teacher_id):
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('DeleteTeacher', [teacher_id])
            for result in cursor.stored_results():
                data = result.fetchall()
            conn.commit()
            return pd.DataFrame(data)
        except Error as e:
            return(f"Error executing DeleteTeacher: {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def find_teacher(teacher_id=None, teacher_name=None):
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('FindTeacher', [teacher_id, teacher_name])
            for result in cursor.stored_results():
                data = result.fetchall()
            return pd.DataFrame(data)
        except Error as e:
            print(f"Error executing FindTeacher: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def get_all_teachers():
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('GetAllTeachers')
            teacher = []
            for result in cursor.stored_results():
                teacher = result.fetchall()
            df = pd.DataFrame(teacher)
            return df
        except Error as e:
            print(f"Error executing GetAllTeachers: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def get_teacher_schedule(teacher_id, term, year):
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('GetTeacherSchedule', [teacher_id, term, year])
            teachersch = []
            for result in cursor.stored_results():
                teachersch = result.fetchall()
            df = pd.DataFrame(teachersch)
            return df
        except Error as e:
            print(f"Error executing GetTeacherSchedule: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()

#Class
    @staticmethod
    def get_fee_summary_by_period() -> pd.DataFrame:
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('sp_fee_summary_by_period')
            for result in cursor.stored_results():
                data = result.fetchall()
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error in get_fee_summary_by_period: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_fee_summary_by_student() -> pd.DataFrame:
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('sp_fee_summary_by_student')
            for result in cursor.stored_results():
                data = result.fetchall()
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error in get_fee_summary_by_student: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_fee_detail_by_student(student_id: int) -> pd.DataFrame:
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('sp_fee_detail_by_student', [student_id])
            for result in cursor.stored_results():
                data = result.fetchall()
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error in get_fee_detail_by_student: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_fee_by_class_term_year(term: int, year: int) -> pd.DataFrame:
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('sp_fee_by_class_term_year', [term, year])
            for result in cursor.stored_results():
                data = result.fetchall()
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error in get_fee_by_class_term_year: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_fee_total_by_class(term: int, year: int) -> pd.DataFrame:
        conn = Manager.connect_db()
        if not conn:
            return pd.DataFrame()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('sp_fee_total_by_class', [term, year])
            for result in cursor.stored_results():
                data = result.fetchall()
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error in get_fee_total_by_class: {e}")
            return pd.DataFrame()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def export_by_class_to_excel(df: pd.DataFrame, filename="money_by_class.xlsx"):
        try:
            if not os.path.isabs(filename):
                temp_dir = tempfile.gettempdir()
                file_path = os.path.join(temp_dir, filename)
            else:
                file_path = filename

            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                for class_name, group_df in df.groupby("ClassName"):
                    safe_name = class_name[:31].replace('/', '-')
                    group_df.to_excel(writer, sheet_name=safe_name, index=False)

            return file_path
        except Exception as e:
            print(f"Error exporting by class to Excel: {e}")
            return None
