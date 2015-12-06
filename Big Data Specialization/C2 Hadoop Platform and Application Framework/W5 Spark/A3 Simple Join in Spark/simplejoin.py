PYSPARK_DRIVER_PYTHON=ipython pyspark

fileA = sc.textFile("input/join1_FileA.txt")
fileB = sc.textFile("input/join1_FileB.txt")

fileA.collect()
fileB.collect()

# Mapper for fileA
def split_fileA(line):
    # split the input line in word and count on the comma
    word,count=line.split(",")
    # turn the count to an integer  
    count=int(count)
    return (word, count)

test_line = "able,991"
split_fileA(test_line)

# Map transformation
fileA_data = fileA.map(split_fileA)
fileA_data.collect()

# Mapper for fileB
def split_fileB(line):
    # split the input line into word, date and count_string
    wordDate,count_string=line.split(",")
    count=int(count_string)
    date,word=wordDate.split(" ")
    return (word, date + " " + count_string)

# Map transformation
fileB_data = fileB.map(split_fileB)   
fileB_data.collect() 

# Run join
fileB_joined_fileA = fileB_data.join(fileA_data)

# Verify the result
fileB_joined_fileA.collect()
