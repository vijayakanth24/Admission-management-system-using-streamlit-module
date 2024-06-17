import streamlit as st
import sqlite3
import pandas as pd

# Function to create or connect to the SQLite database
def create_database():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS STUD_REGISTRATION ("
                   "STU_NAME TEXT,"
                   "STU_CONTACT TEXT,"
                   "STU_EMAIL TEXT,"
                   "STU_ROLLNO TEXT,"
                   "STU_BRANCH TEXT)"
                   )
    conn.commit()
    conn.close()

def generate_email(first_name,domain=".23aim@kongu.edu"):

    first_initial = first_name.lower()
    email = f"{first_initial}{domain}"
    return email

def get_students():
    conn = sqlite3.connect('student.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM STUD_REGISTRATION')
    rows = cur.fetchall()
    conn.close()
    return rows

# Function to insert a new student record
def insert_record(name, contact, email, rollno, branch):
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO STUD_REGISTRATION (STU_NAME, STU_CONTACT, STU_EMAIL, STU_ROLLNO, STU_BRANCH) "
                   "VALUES (?, ?, ?, ?, ?)",
                   (name, contact, email, rollno, branch)
                   )
    conn.commit()
    conn.close()
    st.success("Student record added successfully!")

# Function to delete a student record by name and roll number
def delete_record(name, rollno):
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM STUD_REGISTRATION WHERE STU_NAME = ? AND STU_ROLLNO = ?",
                   (name, rollno)
                   )
    conn.commit()
    conn.close()
    st.success("Record deleted successfully!")

# Function to display all student records
def display_table():
    st.subheader('View Students')
    students = get_students()
    df = pd.DataFrame(students, columns=['Student Name', 'Contact', 'Email', 'Roll Number', 'Branch'])
    df.insert(0, 'S.No', range(1, len(df) + 1))

    st.dataframe(df)
        
# Main function to create the Streamlit web interface
def main():
    st.title("Admission Management System")

    menu = ["Home", "Insert Record", "Delete Record", "Display Records"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write("Welcome to Admission Management System!")

    elif choice == "Insert Record":
        st.subheader("Insert Record")
        name = st.text_input("Enter Student Name")
        contact = st.text_input("Enter Contact Number")
        #email = st.text_input("Enter Email Address")
        rollno = st.text_input("Enter Roll Number")
        branch = st.text_input("Enter Branch")
        email = generate_email(name)

        if st.button("Insert Record"):
            insert_record(name, contact,email, rollno, branch)

    elif choice == "Delete Record":
        st.subheader("Delete Record")
        name = st.text_input("Enter Student Name")
        rollno = st.text_input("Enter Roll Number")

        if st.button("Delete Record"):
            delete_record(name, rollno)

    elif choice == "Display Records":
        
        display_table()

if __name__ == '__main__':
    create_database()
    main()
