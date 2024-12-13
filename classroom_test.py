import pytest
from datetime import datetime
from student import Student  # Make sure this class exists in student.py
from classroom import Classroom, Attendance, validate_date, validate_attendance_status  # Ensure validate_attendance_status is imported


@pytest.fixture
def classroom(): # Used so pytest is assigned to the classroom.py file
    return Classroom()


@pytest.fixture
def student_data(): # Student data demo data 
    return {
        "first_name": "John",
        "middle_name": "D",
        "surname": "Doe",
        "dob": datetime(2000, 1, 1)
    }


def test_add_student(classroom, student_data): # Adds the demo students to the classroom, students.csv
    student_id = classroom.add_student(
        student_data["first_name"],
        student_data["middle_name"],
        student_data["surname"],
        student_data["dob"]
    )
    assert student_id is not None
    assert student_id in classroom.students
    assert classroom.students[student_id].first_name == student_data["first_name"]
    assert classroom.students[student_id].middle_name == student_data["middle_name"]
    assert classroom.students[student_id].surname == student_data["surname"]
    assert classroom.students[student_id].dob == student_data["dob"]


def test_mark_attendance(classroom, student_data): # Adds attendance to student
    student_id = classroom.add_student(
        student_data["first_name"],
        student_data["middle_name"],
        student_data["surname"],
        student_data["dob"]
    )
    date = "15-01-00" # Checks attendance is applied correctly
    classroom.attendance.mark_attendance(date, student_id, "Present")
    
    attendance = classroom.attendance.get_attendance_by_date(date)
    assert student_id in attendance
    assert attendance[student_id] == "Present"


def test_get_attendance_by_date(classroom, student_data): # Retrieves the attendance by date
    student_id = classroom.add_student(
        student_data["first_name"],
        student_data["middle_name"],
        student_data["surname"],
        student_data["dob"]
    )

    # Mark attendance for different dates
    classroom.attendance.mark_attendance("15-01-00", student_id, "Present")
    classroom.attendance.mark_attendance("16-01-00", student_id, "Absent")

    attendance = classroom.attendance.get_attendance_by_date("15-01-00")
    assert student_id in attendance
    assert attendance[student_id] == "Present"

    attendance = classroom.attendance.get_attendance_by_date("16-01-00")
    assert student_id in attendance
    assert attendance[student_id] == "Absent"


def test_get_attendance_by_student(classroom, student_data): # Retrieves the attendance by student
    student_id = classroom.add_student(
        student_data["first_name"],
        student_data["middle_name"],
        student_data["surname"],
        student_data["dob"]
    )

    # Mark attendance for the student on different dates
    classroom.attendance.mark_attendance("15-01-00", student_id, "Present")
    classroom.attendance.mark_attendance("16-01-00", student_id, "Absent")

    attendance = classroom.attendance.get_attendance_by_student(student_id)
    assert "15-01-00" in attendance
    assert attendance["15-01-00"] == "Present"
    assert "16-01-00" in attendance
    assert attendance["16-01-00"] == "Absent"


# Testing errors
def test_invalid_date_format():
    """Test that the date validation function works correctly."""
    assert validate_date("15-01-00") is True
    assert validate_date("15-01-2000") is False
    assert validate_date("01/15/00") is False


def test_invalid_attendance_status():
    """Test that the attendance status validation function works correctly."""
    assert validate_attendance_status("Present") is True
    assert validate_attendance_status("Absent") is True
    assert validate_attendance_status("Late") is False
    assert validate_attendance_status("Excused") is False
