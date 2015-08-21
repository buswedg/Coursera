## Exploratory Data Analysis
## Course Project 1: Plot 2
## plot2.R

val_dfpath <- paste(getwd(), "data", sep = "/")
val_dfname <- "household_power_consumption.txt"
val_dfdlink <- "https://d396qusza40orc.cloudfront.net/exdata%2Fdata%2Fhousehold_power_consumption.zip"

if(file.exists(paste(val_dfpath, val_dfname, sep = "/")) == FALSE){
  
  tryCatch({
    
    temp_data <- tempfile()
    download.file(val_dfdlink, temp_data)
    dir.create(val_dfpath)
    unzip(temp_data, exdir = val_dfpath)
    unlink(temp_data, force = TRUE)
    rm(temp_data)
    
  }, error = function(e){
    
    stop("Datafile error")
    
  })
  
}

## Set the name of the datafile
df <- paste(val_dfpath, val_dfname, sep = "/")

## Read the datafile
data <- read.table(df, header = TRUE, sep = ";", stringsAsFactors = FALSE, dec = ".")

## Subset the data
datasubset <- data[data$Date %in% c("1/2/2007", "2/2/2007") ,]

## Return datetime range
datetime <- strptime(paste(datasubset$Date, datasubset$Time, sep = " "), "%d/%m/%Y %H:%M:%S")

## Return 'Global_active_power' field data
Global_active_power <- as.numeric(datasubset$Global_active_power)

## Create plot file
png("plot2.png", width = 480, height = 480)

## Create plot
plot(datetime, Global_active_power, type = "l", xlab = "", ylab = "Global Active Power (kilowatts)")

## Return number and name of new active device
dev.off()