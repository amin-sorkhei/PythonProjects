class student:
    'This class contains information regarding each student'
    def __init__(self, registration_year, course_list):
        self.registration_year = registration_year
        self.course_list = course_list
        self.courses = self.taken_courses()
        self.enrol_2007 = self.enrol_2008 = self.enrol_2009 = self.enrol_2010 = self.enrol_2011 = self.enrol_2012 = self.enrol_2013 = False

        if int(self.registration_year) == 2007:
            self.enrol_2007 = True
        elif int(self.registration_year) == 2008:
            self.enrol_2008 = True
        elif int(self.registration_year) == 2009:
            self.enrol_2009 = True
        elif int(self.registration_year) == 2010:
            self.enrol_2010 = True
        elif int(self.registration_year) == 2011:
            self.enrol_2011 = True
        elif int(self.registration_year) == 2012:
            self.enrol_2012 = True
        elif int(self.registration_year) == 2008:
            self.enrol_2013 = True

    def add_course(self, course_object):
        self.course_list.append(course_object)

    def get_course(self):
        return self.course_list

    def taken_courses(self):
        temp_list = []
        for crs in self.course_list:
            if crs.course_name not in temp_list:
                temp_list.append(crs.course_name)
        return temp_list

    def has_taken_course(self, given_course_list):
        given_course_set = set(given_course_list)
        courses_set = set(self.courses)
        if given_course_set.issubset(courses_set):
            return True
        else:
            return False

    def display(self):
        return self.registration_year + '\n'.join(self.courses)


