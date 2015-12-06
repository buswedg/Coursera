PYSPARK_DRIVER_PYTHON=ipython pyspark

show_views_file = sc.textFile("input/join2_gennum?.txt")
show_channel_file = sc.textFile("input/join2_genchan?.txt")

show_views_file.take(2)
show_channel_file.take(2)

# Parse shows files
def split_show_views(line):
    show,views=line.split(",")
    views=int(views)
    return (show, views)

# Map transformation
show_views = show_views_file.map(split_show_views)
show_views.collect()

# Parse channel files
def split_show_channel(line):
    show,channel=line.split(",")
    return (show, channel)

# Map transformation
show_channel = show_channel_file.map(split_show_channel)
show_channel.collect()

# Join the 2 datasets
joined_dataset = show_views.join(show_channel)
joined_dataset = show_channel.join(show_views)

# Extract channel as key
def extract_channel_views(show_views_channel):
    channel,views=show_views_channel[1]
    return (channel, views)

# Map transformation
channel_views = joined_dataset.map(extract_channel_views)
channel_views.collect()
	
# Sum across all channels
def sum_channel_viewers(a,b):
    return a + b

# Copy the results back to the Driver
channel_views.reduceByKey(sum_channel_viewers).collect()
