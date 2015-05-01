#!/usr/bin/env python
# -*- coding: utf8 -*-
import itertools
import copy

#We need some verbosity value
verbose = False

#Print partial results
partialFile = None

#
def isSubList(sub, sup):
	i = 0
	j = 0
	while i < len(sub) and j < len(sup):
		if (len(sub[i]) == 0):
			i += 1
			continue
		if set(sub[i]).issubset(set(sup[j])):
			i += 1
		j += 1
	return i == len(sub)

#We will define support a litle differently so that we can 
#compute things faster. Support now will stand for
#"records that would be counted when computing the suppport"
def supportList(s, data):
	return filter(lambda e: isSubList(s, e), data)


def removeLast(seq):
	v = copy.deepcopy(seq)
	if len(v[-1]) == 1:
		return seq[:-1]
	else:
		v[-1] = v[-1][:-1]
		return v

def seqsCanMate(seq1, seq2):
	return removeLast(seq1) == removeLast(seq2)


def seqsOffspring(seq1, seq2):
	e1 = seq2[0][-1][-1]
	e2 = seq2[0][-1][-1]
	cc = copy.deepcopy(seq1[0])
	c1 = copy.deepcopy(seq1[0])
	c2 = copy.deepcopy(seq2[0])
	cc[-1].append(e2)
	c1.append([e2])
	c2.append([e1])
	return [
		[c1, supportList(c1, seq1[1])],
		[c2, supportList(c2, seq1[1])]
	]
	

#Make the next generation, given a sorted list of parents
def aprioriSeqGen(parents):
	candidates = list()
	i = 0
	while i < len(parents):
		j = i+1
		while j < len(parents) and seqsCanMate(parents[i][0], parents[j][0]):
			for s in seqsOffspring(parents[i], parents[j]):
				candidates.append(s)
			j += 1
		i += 1
	return sorted(candidates, key=lambda c: removeLast(c[0]))


#Get the support from a list and a count
def support(l, count):
	return len(l)/float(count)


#Apriori algorithm for sequences
#data must be in the form of [{}, {}, {}]
#The return shall be in the form of
#[
#[[seq], support],
#[[seq], support],
#[[seq], support],
#[[seq], support],
#]
def aprioriSeqs(data, minSup, maxSize=False):
	global verbose
	size = 1
	#Here we will store our answer
	ret = list()
	#We will need to know the size of the original set
	count      = len(data)
	#First we make a set for each unique item, it must be sorted to bootstrap the sorted genereration of nextGen
	#candidates = sorted(map(list, list(set(itertools.chain(*data)))))
	candidates = map(lambda e: [e], sorted(list(set(list(itertools.chain(*list(itertools.chain(*data))))))))
	candidates = map(lambda e: [e], candidates)
	#We get the support for each of the candidates
	supports   = map(lambda c: supportList(c, data), candidates)
	#We zip the candidates with their supports
	candidateSupports = zip(candidates, supports)
	#While we still have candidates to work on
	while len(candidateSupports) > 0:
		if verbose:
			print "Filtering candidates\t\tset size(" + str(size) + ")\tpop size(" + str(len(candidateSupports)) + ")"
		#Filter out those with a support that is too small
		validCandidates   = filter(lambda e: support(e[1], count) >= minSup, candidateSupports)
		#Add the valid candidates to our return
		newPartial = map(lambda c: [c[0], count*support(c[1], count)], validCandidates)
		if partialFile != None:
			with open(partialFile, "a") as myfile:
				myfile.write(str(newPartial) + "\n")
		ret = ret + newPartial
		#If we would compute a size out of the scope
		if maxSize and size >= maxSize:
			break
		if verbose:
			print "Building next generation\tset size(" + str(size) + ")\tpop size(" + str(len(validCandidates)) + ")"
		#Make the next generation of candidates
		candidateSupports = aprioriSeqGen(validCandidates)
		size += 1
	return ret
