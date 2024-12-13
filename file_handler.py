import csv # Imports the ability to create csv data files
from datetime import datetime  # Import datetime for date handling
from student import Student  # Import Student class from student.py

def save_students_to_csv(filename, students): # Saves data to a storage file that will hold all the information about the students.
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file) # Write header
            writer.writerow(['Student ID', 'First Name', 'Middle Name', 'Surname', 'DOB']) # Write student data
            for student_id, student in students.items():
                writer.writerow([
                    student_id,
                    student.first_name,
                    student.middle_name,
                    student.surname,
                    student.dob.strftime('%d-%m-%y')  # Save in DD-MM-YY format
                ])
        print(f"Students saved successfully to {filename}.")
    except Exception as e:
        print(f"Error saving students to {filename}: {e}")


def save_attendance_to_csv(filename, attendance_records): # Saves data to a storage file that will hold all the information about the students' attendance
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file) # Write header
            writer.writerow(['Date', 'Student ID', 'Status']) # Write attendance records
            for date, records in attendance_records.items(): # Makes sure that the attendance is assigned to the right students
                for student_id, status in records.items():
                    writer.writerow([date, student_id, status])
        print(f"Attendance records saved successfully to {filename}.")
    except Exception as e:
        print(f"Error saving attendance to {filename}: {e}")


def load_students_from_csv(filename): # Used to retrieve the student data that is stored in the dictionary
    students = {}
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader: # Extract data from the row
                student_id = row['Student ID']
                first_name = row['First Name']
                middle_name = row['Middle Name']
                surname = row['Surname']
                dob = datetime.strptime(row['DOB'], '%d-%m-%y')  # In DD-MM-YY format
                students[student_id] = Student(first_name, middle_name, surname, dob) # Reconstruct the student object
        print(f"Students loaded successfully from {filename}.")
    except FileNotFoundError:
        print(f"File {filename} not found. Returning an empty student dictionary.")
    except Exception as e:
        print(f"Error loading students from {filename}: {e}")
    return students
