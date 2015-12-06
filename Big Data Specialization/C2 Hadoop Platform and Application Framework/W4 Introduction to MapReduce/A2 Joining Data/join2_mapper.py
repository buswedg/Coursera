#!/usr/bin/env python
import sys

for line in sys.stdin:
    line = line.strip()
    key_value = line.split(",")
    key_in = key_value[0]
    value_in = key_value[1]
    testNum = [int(s) for s in value_in.split() if s.isdigit()]
    
    if len(testNum)>0:
        print( '%s\t%s' % (key_in, value_in))
    else:
        if value_in == 'ABC':
            print( '%s\t%s' % ( value_in, key_in))