#!/usr/bin/env python
# -*- coding: utf8 -*-
import csv
import collections
import scipy
import datetime
import apriori
import sys
import itertools
import math

srcFile = None

def readData(fileName):
    # Courses will be tuples with this names
    Course = collections.namedtuple('Course', 'period code name credits grade')
    # Students will be tuples with this names
    Student = collections.namedtuple('Student', 'registration courses id')
    sId = 1
    ret = list()
    with open(fileName, 'rb') as dataFile:
        # We consider it to be a csv using space as separator
        datum = list(csv.reader(dataFile, delimiter=' '))
        for d in datum:
            # We perform a sanity check to ensure each course has 5 fields
            assert((len(d)-1) % 5 == 0)
            courses = list()
            for i in range((len(d) -1) / 5):
                # Every 5 entries make a record
                # TODO build objects from the values (dates, integers and so on)
                #: courses.append(Course(*d[i*5+1:i*5+6]))
                courses.append(Course(datetime.datetime.strptime(d[i*5+1], '%Y-%m').date(), d[i*5+2], d[i*5+3], float(d[i*5+4]), float(d[i*5+5])))
            ret.append(Student(datetime.datetime.strptime(d[0], '%Y').date(), courses, sId))
            sId += 1
    return ret


def makeSeqs(student, periods):
	ret = list()
	for period in periods:
		s = sorted(list(set(map(lambda c :  c.code ,filter(lambda course: course.period == period, student.courses)))))
		ret.append(s)
	return ret

def courseNames(datum):
	return dict(                                    #Make a dictionary
		set(itertools.chain(*                              #Of the flatlist
		map(                                               #Of maping
			lambda student: set(map(                       #Each student to the set
				lambda course: (course.code, course.name), #Of pairs (code, name)
				student.courses)),                         #For each course
			datum                                          #For each student
	))))

