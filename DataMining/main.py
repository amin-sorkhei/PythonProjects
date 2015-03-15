from student import student
from course import student_course
import re
def main():
    input_file = open('dataMining.txt', 'r')
    lines = input_file.readlines()
    students_list = []
    course_info_dictionary = {}
    print 'this is the number of students ' + str(len(lines))
    for line in lines:
        registration_year = line.split()[0]  # the first element is always the registration year
        data = ' '.join(line.split()[1:])  # Join the rest of the sentence but the first string which is the year
        all_matches = re.findall(r'(\d+\-\d+)\s(\d+)\s\"([\w|\W|\s]+?)\"\s(\d+\W\d+)\s(\w+\W*)', data)
        tmp_course_list = []
        if not all_matches:
            print 'Not found'
            print line
        for match in all_matches:
            course_year_month = match[0]
            course_code = int(match[1])
            course_name = match[2].decode('utf8')
            course_credit = float(match[3])
            final_grade = match[4]
            tmp_student_course = student_course(course_year_month, course_code, course_name, course_credit, final_grade)
            tmp_course_list.append(tmp_student_course)

            if course_code not in course_info_dictionary.keys():
                course_info_dictionary[course_code] = [course_name, course_credit]

        students_list.append(student(registration_year, tmp_course_list))
    st = students_list[0]
    list = st.course_list
    print 'I found ' + str(len(students_list))
    # print list[0].display()
    print course_info_dictionary[57598]


if __name__ == '__main__':
    main()