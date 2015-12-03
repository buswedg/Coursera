#!/usr/bin/env python
import sys

ABC_dict={}
kvs=[]
 
for line in sys.stdin:
    line = line.strip()
    key_value = line.split('\t')
    kvs.append(key_value)
    
    if key_value[0]=="ABC":
        if ABC_dict.has_key(key_value[1])==False:
            ABC_dict.update({key_value[1]:0})
 
for key_value in kvs:
    if ABC_dict.has_key(key_value[0]):
        ABC_dict[key_value[0]]+=int(key_value[1])

for key, value in ABC_dict.iteritems() :
    print( '%s %s' % (key, value))  