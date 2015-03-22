from student import student
from course import student_course
import re
import itertools
import time


def rule_generator(all_courses, size_of_the_set, students_list):
    set_count_dic = {}
    n_subset = itertools.combinations(all_courses, size_of_the_set)
    for elem in n_subset:
        support = support_counter(list(elem), students_list)
        if support > 0:
            set_count_dic[','.join(list(elem))] = support

    return set_count_dic


def support_counter(list_of_courses, student_list):
    cnt = 0
    for std in student_list:
        if set(list_of_courses).issubset(set(std.courses)):
            cnt += 1
    return cnt / float(len(student_list))


def read():
    input_file = open('data.txt', 'r')
    lines = input_file.readlines()
    students_list = []
    course_info_dictionary = {}
    print 'this is the number of students ' + str(len(lines))
    for line in lines:
        registration_year = line.split()[0]  # the first element is always the registration year
        data = ' '.join(line.split()[1:])  # Join the rest of the sentence but the first string which is the year
        all_matches = re.findall(r'(\d+\-\d+)\s(\d+)\s\"([\w|\W|\s]+?)\"\s(\d+\W\d+)\s(\d+)', data)
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
    return students_list, course_info_dictionary


def main():
    students_list, course_info_dictionary = read()
    print len(students_list)
    courses = [crs[0] for crs in course_info_dictionary.values()]
    start = time.clock()
    rule_generator(courses, 3, students_list)
    end = time.clock()
    print end - start
if __name__ == '__main__':
    main()