## Getting and Cleaning Data
## Course Project 1: Tidy Data
## run_analysis.R

## Load plyr library
library(plyr)

val_dfpath <- getwd()
val_dfdlink <- "https://d396qusza40orc.cloudfront.net/getdata%2Fprojectfiles%2FUCI%20HAR%20Dataset.zip"

tryCatch({
  
  temp_data <- tempfile()
  
  download.file(val_dfdlink, temp_data)
  
  unzip(temp_data, exdir = val_dfpath)
  
  unlink(temp_data, force = TRUE)
  
  rm(temp_data)
  
}, error = function(e){
  
  stop("Datafile error")
  
})

## Read 'test' data
data_x_test <- read.table("UCI HAR Dataset/test/X_test.txt") 
data_y_test <- read.table("UCI HAR Dataset/test/y_test.txt") 
data_subject_test <- read.table("UCI HAR Dataset/test/subject_test.txt") 

## Read 'train' data
data_x_train <- read.table("UCI HAR Dataset/train/X_train.txt") 
data_y_train <- read.table("UCI HAR Dataset/train/y_train.txt") 
data_subject_train <- read.table("UCI HAR Dataset/train/subject_train.txt") 

## Combine 'test' and 'train' data
data_sensor_train <- cbind(cbind(data_x_train, data_subject_train), data_y_train)
data_sensor_test <- cbind(cbind(data_x_test, data_subject_test), data_y_test)
data_sensor <- rbind(data_sensor_train, data_sensor_test)

## Read 'features' data
data_features <- read.table("UCI HAR Dataset/features.txt", colClasses = c("character"))

## Set field names for sensor data
data_sensor_labels <- rbind(rbind(data_features, c(562, "Subject")), c(563, "ActivityId"))[, 2]
names(data_sensor) <- data_sensor_labels

## Extract only mean/standard deviation data from sensor data
data_sensor_meanstd <- data_sensor[, grepl("mean|std|Subject|ActivityId", names(data_sensor))]

## Read 'activities' data
data_activities <- read.table("UCI HAR Dataset/activity_labels.txt", col.names = c("ActivityId", "Activity"))

## Use descriptive activity names to name activities in sensor data
data_sensor_meanstd <- join(data_sensor_meanstd, data_activities, by = "ActivityId", match = "first")
data_sensor_meanstd <- data_sensor_meanstd[, -1]

## Clean up data fields for sensor data
names(data_sensor_meanstd) <- gsub('\\(|\\)', "", names(data_sensor_meanstd), perl = TRUE)
names(data_sensor_meanstd) <- make.names(names(data_sensor_meanstd))
names(data_sensor_meanstd) <- gsub('Acc', "Acceleration", names(data_sensor_meanstd))
names(data_sensor_meanstd) <- gsub('GyroJerk', "AngularAcceleration", names(data_sensor_meanstd))
names(data_sensor_meanstd) <- gsub('Gyro', "AngularSpeed", names(data_sensor_meanstd))
names(data_sensor_meanstd) <- gsub('Mag', "Magnitude", names(data_sensor_meanstd))
names(data_sensor_meanstd) <- gsub('^t', "TimeDomain.", names(data_sensor_meanstd))
names(data_sensor_meanstd) <- gsub('^f', "FrequencyDomain.", names(data_sensor_meanstd))
names(data_sensor_meanstd) <- gsub('\\.mean', ".Mean", names(data_sensor_meanstd))
names(data_sensor_meanstd) <- gsub('\\.std', ".StandardDeviation", names(data_sensor_meanstd))
names(data_sensor_meanstd) <- gsub('Freq\\.', "Frequency.", names(data_sensor_meanstd))
names(data_sensor_meanstd) <- gsub('Freq$', "Frequency", names(data_sensor_meanstd))

## Create new dataframe with average of each variable for each activity and subject
data_sensor_avgactsub = ddply(data_sensor_meanstd, c("Subject", "Activity"), numcolwise(mean))
write.table(data_sensor_avgactsub, row.names = FALSE, file = "data_sensor_avgactsub.txt")

unlink("UCI HAR Dataset", recursive = TRUE, force = TRUE)