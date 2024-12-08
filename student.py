# Student class
class Student:
    def __init__(self, first_name, middle_name, surname, dob):
        # This part of the code sets the self parameter. This assigns the names to each of the parts within the class.
        self.first_name = first_name
        self.middle_name = middle_name
        self.surname = surname
        self.dob = dob
        self.student_id = self.generate_student_id()

    def generate_student_id(self):
        # Takes the inputted student data and produces a student ID for the student using the class that was created with all the details. It's in the format Initials + DD-MM-YY.
        initials = f"{self.first_name[0]}{self.middle_name[0]}{self.surname[0]}".upper()
        dob_formatted = self.dob.strftime("%d-%m-%y")
        return f"{initials}{dob_formatted}"