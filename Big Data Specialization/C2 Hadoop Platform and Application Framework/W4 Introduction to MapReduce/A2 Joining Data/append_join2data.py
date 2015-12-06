#!/usr/bin/env python
import sys

chvnm=sys.argv[1]  #get number argument, if its n, do numbers not channels,

output=sys.argv[1]

input=[]
input.append(sys.argv[2])
input.append(sys.argv[3])
input.append(sys.argv[4])

appended=[]
for infile in input:
	with open(infile) as f:
		temp=f.read()
		appended.append(temp)

with open(output, "w") as f:
	f.writelines(appended)