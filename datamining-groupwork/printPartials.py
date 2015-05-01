#!/usr/bin/env python
# -*- coding: utf8 -*-
import importer
import partialGraduated
import partialNotGraduated
import arches

#We will need the original data
datum = importer.readData('data.txt')

#We might want to replace course names (courseNames[code] = name)
courseNames = importer.courseNames(datum)

#Given a list of seqs, finds the one with the highest support
def maxSeq(seqs):
	m   = -1.
	ret = None
	for s in seqs:
		if seqs[1] > m:
			m = seqs[1]
			ret = s
	return ret


#Print into a file, do whatever you want with it
for sizeGroup in arches.seqs:
	for s in sizeGroup:
		for group in s[0]: #Each group of courses taken together
			for course in group: #Each course in the group
				print course
		print s[1] #Support


