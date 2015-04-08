from student import student
from course import student_course
import re
import itertools
import time


def read():
    input_file = open('data.txt', 'r')
    lines = input_file.readlines()
    students_list = []
    course_info_dictionary = {}
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
            course_code = match[1]
            course_name = match[2].decode('utf8')
            course_credit = match[3]
            final_grade = match[4]
            tmp_student_course = student_course(course_year_month, course_code, course_name, course_credit, final_grade)
            tmp_course_list.append(tmp_student_course)

            if course_code not in course_info_dictionary.keys():
                course_info_dictionary[course_code] = [course_name, course_credit]

        students_list.append(student(registration_year, tmp_course_list))
    return students_list, course_info_dictionary


def support_count(list_of_items, transactions, threshold):
    result = []
    for item in list_of_items:
        _item = item
        count = 0
        for transaction in transactions:
            if type(item) != list:
                _item = [item]
            if set(_item) <= set(transaction):
                    count += 1
        support = float(count) / len(transactions)
        # print str(item) + ' ' + str(support)
        if support >= threshold:
            result.append(item)
    result.sort()
    return result


def merge(list_of_items):
    result = []
    for i in xrange(len(list_of_items) - 1):
        j = i + 1
        while j < len(list_of_items) and list_of_items[i][:-1] == list_of_items[j][:-1]:
                result.append(list_of_items[i][:-1] + list_of_items[i][-1].split() + list_of_items[j][-1].split())
                j += 1
    return result


def main():
    students_list, course_info_dictionary = read()
    transactions = []
    for std in students_list:
        transactions.append([course.course_code for course in std.course_list])
    items = course_info_dictionary.keys()

    threshold = 0.08
    start = time.clock()
    initial = support_count(items, transactions, threshold)
    two_candidates = map(list, list(itertools.combinations(initial, 2)))
    print 'length of two-candidates: ' + str(len(two_candidates))
    final_items = two_candidates
    new_candidates = support_count(two_candidates, transactions, threshold)
    while new_candidates:
        final_items = new_candidates
        print 'length of best answers so far: ' + str(len(final_items)) + ' and the length of the rule is ' + str(len(final_items[0]))
        new_candidates = merge(new_candidates)
        if not new_candidates:
            new_candidates = support_count(new_candidates, transactions, threshold)
    end = time.clock()
    print 'the best answers: ' + str(final_items)
    print 'This is the elapsed time ' + str(end - start)


if __name__ == '__main__':
    main()