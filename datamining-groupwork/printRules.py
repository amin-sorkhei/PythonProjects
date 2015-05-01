#!/usr/bin/env python
# -*- coding: utf8 -*-
import graduatingRules
import notGraduatingRules
import popularArches



for s in graduatingRules.seqs:
	#Support
	print "S(\{"+"},{".join(map(lambda e: ",".join(e), s[0]))+"\} \rightarrow \mbox{Graduation}) = " + str(s[1])
	#Confidence
	print "C(\{"+"},{".join(map(lambda e: ",".join(e), s[0]))+"\} \rightarrow \mbox{Graduation}) = " + str(s[2])


for s in notGraduatingRules.seqs:
	#Support
	print "S(\{"+"},{".join(map(lambda e: ",".join(e), s[0]))+"\} \rightarrow \mbox{Not Graduation}) = " + str(s[1])
	#Confidence
	print "C(\{"+"},{".join(map(lambda e: ",".join(e), s[0]))+"\} \rightarrow \mbox{Not Graduation}) = " + str(s[2])
	
for s in popularArches.seqs:
	#Support
	print "S(\{"+"},{".join(map(lambda e: ",".join(e), s[0]))+"\} = " + str(s[1])
