from student import student
from course import student_course
import re
import itertools
import time
import pickle
import math


support_count_dic = {}
closed_frequent_itemsets = []


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
        if frozenset(_item) not in support_count_dic.keys():
            support_count_dic[frozenset(_item)] = support
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


def closed_set_finder(list_of_parents, list_of_new_children):
    print 'These are parents ' + str(list_of_parents)
    print 'These are children ' + str(list_of_new_children)
    for parent in list_of_parents:
        children = filter(lambda x: set(parent) <= set(x), list_of_new_children)
        print str(parent) + ' => ' + str(children)
        matched_children = filter(
            lambda child: support_count_dic[frozenset(parent)] == support_count_dic[frozenset(child)], children)
        if not matched_children and children:
            print 'closed frequent item set found ' + str(parent)
            closed_frequent_itemsets.append(parent)


def item_gen(items, transactions, threshold):
    initial = support_count(items, transactions, threshold)
    two_candidates = map(list, list(itertools.combinations(initial, 2)))
    print 'length of two-candidates: ' + str(len(two_candidates))
    final_items = two_candidates
    # since initial contains elements which are not list, we need to turn them to lists
    initial = map(lambda x: x.split(), initial)
    new_candidates = support_count(two_candidates, transactions, threshold)
    closed_set_finder(initial, new_candidates)
    while new_candidates:
        final_items = new_candidates
        print 'length of best answers so far: ' + str(len(final_items)) + ' and the length of the itemset is ' + str(
            len(final_items[0]))
        new_candidates = merge(new_candidates)
        print 'size of new candidates ' + str(len(new_candidates))
        if new_candidates:
            new_candidates = support_count(new_candidates, transactions, threshold)
            closed_set_finder(final_items, new_candidates)
    return final_items


def rule_generator(all_freqent_itemsets, conf):
    for frequent_itemset in all_freqent_itemsets:
        one_level_rule_gen(frequent_itemset, conf)


def one_level_rule_gen(itemset, conf):
    consequent = itemset
    for item in itemset:
        head = item.split()
        precedent = [item for item in itemset if item not in head]
        rule_conf = support_count_dic[frozenset(head + precedent)] / support_count_dic[frozenset(precedent)]
        rule_lift = rule_conf / support_count_dic[frozenset(head)]
        rule_IS = support_count_dic[frozenset(head + precedent)] / (math.sqrt(support_count_dic[frozenset(precedent)] * support_count_dic[frozenset(head)]))
        if rule_conf < conf:
            consequent = list(set(consequent) - set(head))

        print str(precedent) + ' => ' + str(head) + '  ' + ' conf: ' + str(rule_conf) + ' lift: ' + str(rule_lift) + ' IS: ' + str(rule_IS)
    consequent = map(list, list(itertools.combinations(consequent, 2)))
    print 'First set of consequents ' + str(consequent)
    while consequent:
        temp_consequent = consequent
        for head in temp_consequent:
            precedent = [item for item in itemset if item not in head]
            if not precedent:
                break
            rule_conf = support_count_dic[frozenset(head + precedent)] / support_count_dic[frozenset(precedent)]
            rule_lift = rule_conf / support_count_dic[frozenset(head)]
            rule_IS = support_count_dic[frozenset(head + precedent)] / (math.sqrt(support_count_dic[frozenset(precedent)] * support_count_dic[frozenset(head)]))
            if rule_conf < conf:
                consequent = [x for x in consequent if x != head]
            print str(precedent) + ' => ' + str(head) + '  ' + ' conf: ' + str(rule_conf) + ' lift: ' + str(rule_lift) + ' IS: ' + str(rule_IS)
        consequent = merge(consequent)
        print 'This is the list of new consequents ' + str(consequent)


def print_dic():
    f_str = ''
    keys = map(list, support_count_dic.keys())
    keys.sort(lambda x, y: cmp(len(x), len(y)))
    print len(keys)
    for k in keys:
        f_str += str(k) + ' ' + str(support_count_dic[frozenset(k)]) + '\n'
    return f_str


def main():
    students_list, course_info_dictionary = read()
    transactions = []
    for std in students_list:
        transactions.append([course.course_code for course in std.course_list])
    items = course_info_dictionary.keys()
    start = time.clock()
    final_items = item_gen(items, transactions, threshold=0.16)
    end = time.clock()
    print 'the best answers: ' + str(final_items)
    print 'This is the elapsed time ' + str(end - start)
    for itemset in final_items:
        print 'This is the support for ' + str(itemset) + ' ' + str((support_count_dic[frozenset(itemset)]))
    final_frequent_closed_itemsets = closed_frequent_itemsets + final_items

    pickle.dump(support_count_dic, open('dic.pic', 'w'))
    open('dic.txt', 'w').write(print_dic())
    print(final_frequent_closed_itemsets)

    print '-----------------------------------'
    f_itemset = [
        ['57043', '581325'],
        ['581324', '581325'],
        ['581325', '581328'],
        ['581325', '582102'],
        ['581325', '582103'],
        ['581325', '582104'],
        ['581325', '582514'],
        ['581324', '581325', '582102'],
        ['581324', '581325', '582103'],
        ['581324', '581325', '582104'],
        ['581325', '582102', '582103'],
        ['581325', '582103', '582104']]

    rule_generator(f_itemset, conf=0.1)


if __name__ == '__main__':
    main()