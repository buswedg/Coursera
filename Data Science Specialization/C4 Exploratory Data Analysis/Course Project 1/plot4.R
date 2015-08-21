## Exploratory Data Analysis
## Course Project 1: Plot 4
## plot4.R

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

## Return relevant field data
Global_active_power <- as.numeric(datasubset$Global_active_power)
Global_reactive_power <- as.numeric(datasubset$Global_reactive_power)
Voltage <- as.numeric(datasubset$Voltage)
Sub_metering_1 <- as.numeric(datasubset$Sub_metering_1) 
Sub_metering_2 <- as.numeric(datasubset$Sub_metering_2) 
Sub_metering_3 <- as.numeric(datasubset$Sub_metering_3) 

## Create 2x2 plot file
png("plot4.png", width = 480, height = 480)
par(mfrow = c(2, 2)) 

## Create plot 1
plot(datetime, Global_active_power, type = "l", xlab = "", ylab = "Global Active Power", cex = 0.2)

## Create plot 2
plot(datetime, Voltage, type="l", xlab="datetime", ylab="Voltage")

## Create plot 3
plot(datetime, Sub_metering_1, type = "l", ylab = "Energy sub metering", xlab = "") 
lines(datetime, Sub_metering_2, type = "l", col = "red") 
lines(datetime, Sub_metering_3, type = "l", col = "blue") 
legend("topright", c("Sub_metering_1", "Sub_metering_2", "Sub_metering_3"), lty = , lwd = 2.5, col = c("black", "red", "blue"), bty = "o") 

## Create plot 4
plot(datetime, Global_reactive_power, type = "l", xlab = "datetime", ylab = "Global_reactive_power")

## Return number and name of new active device
dev.off()