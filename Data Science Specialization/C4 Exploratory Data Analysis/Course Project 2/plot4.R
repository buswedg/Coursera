## Exploratory Data Analysis
## Course Project 2: Plot 4
## plot4.R

## Load plyr library
library(plyr)

## Load ggplot2 library
library(ggplot2)

val_dfpath <- paste(getwd(), "data", sep = "/")
val_dfname <- c("summarySCC_PM25.rds", "Source_Classification_Code.rds")
val_dfdlink <- "https://d396qusza40orc.cloudfront.net/exdata%2Fdata%2FNEI_data.zip"

for (i in val_dfname) {
  
  if(file.exists(paste(val_dfpath, i, sep = "/")) == FALSE){
    
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
  
}

## Set the name of the datafiles
Val_df_em <- paste(val_dfpath, val_dfname[1], sep = "/")
Val_df_scc <- paste(val_dfpath, val_dfname[2], sep = "/")

## Read the datafiles
data_em <- readRDS(Val_df_em)
data_scc <- readRDS(Val_df_scc)

## Show datafile structure
## str(data_em)
## str(data_scc)

## Find unique instances of Coal EI.Sector within SCC datafile
val_sccref_coal <- unique(grep("Coal", data_scc$EI.Sector, ignore.case = TRUE, value = TRUE))

## Subset SCC datafile by unique Coal EI.Sector instances
data_scc_coal <- subset(data_scc, EI.Sector %in% val_sccref_coal)

## Subset Emissions datafile by Coal EI.Sector SCC instances
data_em_coal <- subset(data_em, SCC %in% data_scc_coal$SCC)

## For each instance, sum emission and combine with year value
data_em_coalyear <- ddply(data_em_coal, .(year, type), function(x) sum(x$Emissions))

## Set third column field name of summary dataframe
colnames(data_em_coalyear)[3] <- "emissions"

## Create plot file
png("plot4.png", width = 480, height = 480)

## Create ggplot
ggplot(data_em_coalyear, aes(x = factor(year), y = emissions, fill = type)) +
  geom_bar(stat = "identity") +
  labs(title = "US Coal Combustion Emissions by Type", x = "Year", y = expression(PM[2.5] ~ "Emissions (tons)"))

## Return number and name of new active device
dev.off()