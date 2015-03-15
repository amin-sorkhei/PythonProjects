class student_course:
    'This class contains information regarding each course'

    def __init__(self, course_year_month, course_code, course_name, credit, final_grade ):
        self.course_year_month = course_year_month
        self.course_code = course_code
        self.course_name = course_name
        self.credits = credit
        self.final_grade = final_grade

    def display(self):
        return self.course_year_month + ' ' + str(self.course_code) + ' ' + self.course_name + ' ' + str(self.credits) + ' ' + self.final_grade




