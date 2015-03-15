
class student:
    'This class contains information regarding each student'
    def __init__(self, registration_year,course_list):
        self.registration_year = registration_year
        self.course_list = course_list

    def add_course(self, course_object):
        self.course_list.append(course_object)



