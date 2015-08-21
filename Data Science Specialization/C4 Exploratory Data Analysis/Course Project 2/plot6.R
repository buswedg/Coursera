## Exploratory Data Analysis
## Course Project 2: Plot 6
## plot6.R

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
val_df_em <- paste(val_dfpath, val_dfname[1], sep = "/")
val_df_scc <- paste(val_dfpath, val_dfname[2], sep = "/")

## Read the datafiles
data_em <- readRDS(val_df_em)
data_scc <- readRDS(val_df_scc)

## Show datafile structure
## str(data_em)
## str(data_scc)

## Subset Emissions datafile by LA fips instances
data_em_la <- subset(data_em, data_em$fips == "06037")

## Subset Emissions datafile by Baltimore fips instances
data_em_balt <- subset(data_em, data_em$fips == "24510")

## Find unique instances of Mobile EI.Sector within SCC datafile
val_sccref_veh <- unique(grep("Mobile", data_scc$EI.Sector, ignore.case = TRUE, value = TRUE))

## Subset SCC datafile by each unique veh EI.Sector instance
data_scc_veh1 <- subset(data_scc, EI.Sector %in% val_sccref_veh[1])
data_scc_veh2 <- subset(data_scc, EI.Sector %in% val_sccref_veh[2])
data_scc_veh3 <- subset(data_scc, EI.Sector %in% val_sccref_veh[3])
data_scc_veh4 <- subset(data_scc, EI.Sector %in% val_sccref_veh[4])

## Subset LA Emissions subset by each unique veh EI.Sector SCC instance
data_em_laveh1 <- subset(data_em_la, SCC %in% data_scc_veh1$SCC)
data_em_laveh2 <- subset(data_em_la, SCC %in% data_scc_veh2$SCC)
data_em_laveh3 <- subset(data_em_la, SCC %in% data_scc_veh3$SCC)
data_em_laveh4 <- subset(data_em_la, SCC %in% data_scc_veh4$SCC)

## Subset Baltimore Emissions subset by each unique veh EI.Sector SCC instance
data_em_baltveh1 <- subset(data_em_balt, SCC %in% data_scc_veh1$SCC)
data_em_baltveh2 <- subset(data_em_balt, SCC %in% data_scc_veh2$SCC)
data_em_baltveh3 <- subset(data_em_balt, SCC %in% data_scc_veh3$SCC)
data_em_baltveh4 <- subset(data_em_balt, SCC %in% data_scc_veh4$SCC)

## Create new dataframe for each LA veh EI.Sector emission subset with vehicle and city fields
data_laveh1 <- data.frame(data_em_laveh1, vehicle = "Gasoline - Heavy Duty", city = "Los Angeles")
data_laveh2 <- data.frame(data_em_laveh2, vehicle = "Gasoline - Light Duty", city = "Los Angeles")
data_laveh3 <- data.frame(data_em_laveh3, vehicle = "Diesel - Light Duty", city = "Los Angeles")
data_laveh4 <- data.frame(data_em_laveh4, vehicle = "Diesel - Heavy Duty", city = "Los Angeles")

## Create new dataframe for each Baltimore veh EI.Sector emission subset with vehicle fields
data_baltveh1 <- data.frame(data_em_baltveh1, vehicle = "Gasoline - Heavy Duty", city = "Baltimore")
data_baltveh2 <- data.frame(data_em_baltveh2, vehicle = "Gasoline - Light Duty", city = "Baltimore")
data_baltveh3 <- data.frame(data_em_baltveh3, vehicle = "Diesel - Light Duty", city = "Baltimore")
data_baltveh4 <- data.frame(data_em_baltveh4, vehicle = "Diesel - Heavy Duty", city = "Baltimore")

## Aggregate each LA Mobile dataframe
data_laveh <- rbind(data_laveh1, data_laveh2, data_laveh3, data_laveh4) 

## Aggregate each Baltimore Mobile dataframe
data_baltveh <- rbind(data_baltveh1, data_baltveh2, data_baltveh3, data_baltveh4)

## Aggregate LA and Baltimore Mobile dataframes
data_labaltveh <- rbind(data_laveh, data_baltveh)

## For each instance, sum emission and combine with year value
data_labaltvehyear <- ddply(data_labaltveh, .(year, city, vehicle), function(x) sum(x$Emissions))

## Set third column field name of summary dataframe
colnames(data_labaltvehyear)[4] <- "emissions"

## Create plot file
png("plot6.png", width = 720, height = 480)

## Create ggplot
ggplot(data_labaltvehyear, aes(x = factor(year), y = emissions, fill = vehicle)) +
  geom_bar(stat = "identity") +
  facet_grid(.~city, scales = "free", space = "free") + 
  labs(title = "HMV Related Emissions by Type: Los Angeles vs Baltimore", x = "Year", y = expression(PM[2.5] ~ "Emissions (tons)"))

## Return number and name of new active device
dev.off()