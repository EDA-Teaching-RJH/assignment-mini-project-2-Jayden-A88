import re
from datetime import datetime
from file_handler import save_students_to_csv, save_attendance_to_csv, load_students_from_csv
from student import Student  # Import Student class from student.py

# Attendance class
class Attendance:
    def __init__(self):
        self.records = {}  # Format: {date: {student_id: "Present"/"Absent"}}

    def mark_attendance(self, date, student_id, status): # Marks the attendance by accessing and assessing the records class.
        if date not in self.records:
            self.records[date] = {}
        self.records[date][student_id] = status

    def get_attendance_by_date(self, date): # It retrieves the attendance records for a certain date.
        return self.records.get(date, {})

    def get_attendance_by_student(self, student_id): # Retrieves the records for a specific student.
        result = {}
        for date, attendance in self.records.items():
            if student_id in attendance:
                result[date] = attendance[student_id]
        return result


# Classroom class
class Classroom:
    def __init__(self):
        self.students = {}
        self.attendance = Attendance()

    def add_student(self, first_name, middle_name, surname, dob): # Adds a student details to the classroom class to be stored and accessed
        student = Student(first_name, middle_name, surname, dob)
        self.students[student.student_id] = student
        return student.student_id


# Validation functions
def validate_date(date): # Validates the dob that is put in by the user
     return bool(re.fullmatch(r"\d{2}-\d{2}-\d{2}", date))

def validate_attendance_status(status): # validates whether the student is present or not.
    return status in ["Present", "Absent"]


def main():
    classroom = Classroom()
    
    # Load students from a CSV file
    filename = "students.csv"
    classroom.students = load_students_from_csv(filename)


    while True:
        print("Classroom Attendance Tracker")
        print("1. Add Student")
        print("2. Mark Attendance")
        print("3. View Attendance by Date")
        print("4. View Attendance by Student")
        print("5. Save Data")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            first_name = input("Enter first name: ").strip()
            middle_name = input("Enter middle name: ").strip()
            surname = input("Enter surname: ").strip()
            dob_str = input("Enter date of birth (DD-MM-YY): ").strip()

            if validate_date(dob_str):
                dob = datetime.strptime(dob_str, "%d-%m-%y")
                student_id = classroom.add_student(first_name, middle_name, surname, dob)
                print(f"Student added successfully! Student ID: {student_id}")
            else:
                print("Invalid date format. Please use DD-MM-YY.")

        elif choice == "2":
            date = input("Enter date (DD-MM-YY): ").strip()
            if not validate_date(date):
                print("Invalid date format. Please use DD-MM-YY.")
                continue

            student_id = input("Enter student ID: ").strip()
            if student_id not in classroom.students:
                print("Student ID not found.")
                continue

            status = input("Enter attendance status (Present/Absent): ").strip().capitalize()
            if validate_attendance_status(status):
                classroom.attendance.mark_attendance(date, student_id, status)
                print(f"Attendance marked for {student_id} on {date} as {status}.")
            else:
                print("Invalid attendance status. Please enter 'Present' or 'Absent'.")

        elif choice == "3":
            date = input("Enter date (DD-MM-YY): ").strip()
            if not validate_date(date):
                print("Invalid date format. Please use DD-MM-YY.")
                continue

            attendance = classroom.attendance.get_attendance_by_date(date)
            if attendance:
                print(f"Attendance on {date}:")
                for student_id, status in attendance.items():
                    print(f"  {student_id}: {status}")
            else:
                print(f"No attendance records found for {date}.")

        elif choice == "4":
            student_id = input("Enter student ID: ").strip()
            if student_id not in classroom.students:
                print("Student ID not found.")
                continue

            attendance = classroom.attendance.get_attendance_by_student(student_id)
            if attendance:
                print(f"Attendance for {student_id}:")
                for date, status in attendance.items():
                    print(f"  {date}: {status}")
            else:
                print(f"No attendance records found for {student_id}.")

        elif choice == "5":
            save_students_to_csv("students.csv", classroom.students)
            save_attendance_to_csv("attendance.csv", classroom.attendance.records)
            print("Data saved successfully!")

        elif choice == "6":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
