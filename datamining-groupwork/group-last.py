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
import importer
import arches




def hasGraduated(student):
	d = collections.defaultdict(int)
	for course in student.courses:
		if course.grade > 0:
			d[course.code] = max(d[course.code], course.credits)
	ret = 0
	for k in d.items():
		ret += k[1]
	return ret >= 180


datum = importer.readData('data.txt')
#CourseNames
courseNames = importer.courseNames(datum)

periods         = sorted(list(set(itertools.chain(*map(
					lambda student:
						map(
							lambda course: course.period
						,student.courses),
				datum)))))


datumSeq              = map(lambda student: importer.makeSeqs(student, periods), datum)
graduatingDatumSeq    = map(lambda student: importer.makeSeqs(student, periods), filter(hasGraduated, datum))
notGraduatingDatumSeq = map(lambda student: importer.makeSeqs(student, periods), filter(lambda x: not hasGraduated(x), datum))


apriori.verbose=True
apriori.partialFile="partialGraduated.txt"
#apriori.aprioriSeqs(graduatingDatumSeq, 4./75, 12)#Best is 9-.05

apriori.partialFile="partialNotGraduated.txt"
#apriori.aprioriSeqs(notGraduatingDatumSeq, .006, 12)#Best is 8-.01


apriori.partialFile="arches.py"
#apriori.aprioriSeqs(datumSeq, .01, 12)#Best is 8-.01


import partialGraduated
import partialNotGraduated

def maxSeq(seqs):
	m   = -1.
	ret = None
	for s in seqs:
		if seqs[1] > m:
			m = seqs[1]
			ret = s
	return ret



graduatingSeqs = map(maxSeq, partialGraduated.seqs) #itertools.chain(*partialGraduated.seqs)

notGraduatingSeqs = map(maxSeq, partialNotGraduated.seqs) #itertools.chain(*partialNotGraduated.seqs)



def getNames(seq, courseNames):
	return map(lambda s: map(lambda r: courseNames[r] ,s), seq)



#Take the one with the best support for each size
bestSeqs = map(maxSeq, arches.seqs)

#use support instead of supportcount
bestSeqs = map(lambda s: [getNames(s[0], courseNames), s[1]/len(datum)], bestSeqs)

#Include the course name for each

with open("popularArches.py", "a") as myfile:
	myfile.write("seqs = [")
	myfile.write(str(bestSeqs))
	myfile.write("] \n")


exit(1)
regs = float(len(datumSeq))
print "a"
tmp = map(lambda g: [g[0], g[1]/regs, apriori.support(apriori.supportList(g[0], datumSeq), regs)], graduatingSeqs)
print "b"
graduatingRules = map(lambda g: [getNames(g[0], courseNames), g[1], g[1]/g[2]], tmp)
print "c"
tmp = map(lambda g: [g[0], g[1]/regs, apriori.support(apriori.supportList(g[0], datumSeq), regs)], notGraduatingSeqs)
print "d"
notGraduatingRules = map(lambda g: [getNames(g[0], courseNames), g[1], g[1]/g[2]],tmp)
print "e"
with open("graduatingRules.py", "a") as myfile:
	myfile.write(str(graduatingRules) + "\n")

with open("notGraduatingRules.py", "a") as myfile:
	myfile.write(str(notGraduatingRules) + "\n")










