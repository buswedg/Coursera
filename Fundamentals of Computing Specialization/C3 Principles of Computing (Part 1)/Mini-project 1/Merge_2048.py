## Principles of Computing (Part 1)
## Mini-project 1: 2048 (Merge)
## Merge_2048.py

## Module was initially intended to be run with CodeSkulptor http://www.codeskulptor.org/#poc_2048_merge_template.py


"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    newline = []
    item1 = 0
	
    while True:
        while item1 < len(line) and line[item1] == 0:
            item1 += 1
        if item1 >= len(line):
            break
        item2 = item1 + 1
        while item2 < len(line) and line[item2] == 0:
            item2 += 1
        if item2 >= len(line):
            newline.append(line[item1])
            break
        if line[item1] == line[item2]:
            newline.append(2 * line[item1])
            item1 = item2 + 1
        else:
            newline.append(line[item1])
            item1 = item2
			
    return newline + [0] * (len(line) - len(newline))

def test_merge():
    """
    Test merge function.
    """
    
    print merge([2, 0, 2, 4])
    print merge([0, 0, 2, 2])
    print merge([2, 2, 0, 0])
    print merge([2, 2, 2, 2, 2])
    print merge([8, 16, 16, 8])

## Test merge function
test_merge()
