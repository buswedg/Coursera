#Practical Machine Learning
###Course Project: CP_template

for (package in c('caret', 'randomForest', 'rpart', 'rpart.plot')) {
  if (!require(package, character.only = TRUE, quietly = FALSE)) {
    install.packages(package)
    library(package, character.only = TRUE)
  }
}

val_dfpath <- paste(getwd(), "data", sep = "/")
val_dfchk <- c("pmltraining.raw", "pmltesting.raw")
val_dfname <- c("pml-training.csv", "pml-testing.csv")
val_dfdlink <- "https://d396qusza40orc.cloudfront.net/predmachlearn"

for (i in 1:length(val_dfchk)) {
##  tryCatch({
    if (exists(val_dfchk[i]) == FALSE) {
      if (file.exists(paste(val_dfpath, val_dfname[i], sep = "/")) == FALSE) {
        dir.create(val_dfpath)
        download.file(paste(val_dfdlink, val_dfname[i], sep = "/"), paste(val_dfpath, val_dfname[i], sep = "/"))
      }
    }
##  }, error = function(e){
##    stop("Datafile error")
##  })
}

## Read data
data_pmltraining.raw <- read.csv(paste(val_dfpath, val_dfname[1], sep = "/"), na.strings = c("NA", "#DIV/0!", ""))
data_pmltesting.raw <- read.csv(paste(val_dfpath, val_dfname[2], sep = "/"), na.strings = c("NA", "#DIV/0!", ""))

dim(data_pmltraining.raw)
## str(data_pmltraining.raw)
## summary(data_pmltraining.raw)

## Remove near zero covariates
data_pmltraining.nzv <- nearZeroVar(data_pmltraining.raw, saveMetrics = TRUE)
data_pmltraining <- data_pmltraining.raw[, !data_pmltraining.nzv$nzv]
remove(data_pmltraining.nzv)

## Remove first column of the training dataset
data_pmltraining <- data_pmltraining[, -1]

## Remove variables with more than 60% NA values
val_pmltraining.nav <- which((colSums(!is.na(data_pmltraining)) >= 0.6 * nrow(data_pmltraining)))
data_pmltraining <- data_pmltraining[, val_pmltraining.nav]
remove(val_pmltraining.nav)

## Split into training and testing datasets
data_pmltraining.inTrain <- createDataPartition(data_pmltraining$classe, p = 0.6, list = FALSE)
data_pmltraining.train <- data_pmltraining[data_pmltraining.inTrain, ]
data_pmltraining.test <- data_pmltraining[-data_pmltraining.inTrain, ]
remove(data_pmltraining.inTrain)

## Transform training and testing datasets
val_pmltraining.allcol <- colnames(data_pmltraining.train)
val_pmltraining.datacol <- colnames(data_pmltraining.train[, -ncol(data_pmltraining.train)])
data_pmltraining.test <- data_pmltraining.test[val_pmltraining.allcol]
data_pmltesting <- data_pmltesting.raw[val_pmltraining.datacol]
remove(val_pmltraining.allcol, val_pmltraining.datacol)

## Coerce data classes between training and final testing datasets
data_pmltesting <- rbind(data_pmltraining.train[2, -ncol(data_pmltraining.train)] , data_pmltesting)
data_pmltesting <- data_pmltesting[-1, ]

dim(data_pmltraining.train)
## str(data_pmltraining.train)
## summary(data_pmltraining.train)

dim(data_pmltraining.test)
## str(data_pmltraining.test)
## summary(data_pmltraining.test)

dim(data_pmltesting)
## str(data_pmltesting)
## summary(data_pmltesting)

## Decision tree prediction
set.seed(12345)
val_dtmodel <- rpart(classe ~ ., data = data_pmltraining.train, method = "class")
val_dtmodel.predict <- predict(val_dtmodel, data_pmltraining.test, type = "class")
val_dtcm <- confusionMatrix(val_dtmodel.predict, data_pmltraining.test$classe)
val_dtcm
plot(val_dtcm$table, col = val_dtcm$byClass, main = paste("Decision Tree Confusion Matrix: Accuracy =", round(val_dtcm$overall['Accuracy'], 4)))

## Random forest prediction
set.seed(12345)
val_rfmodel <- randomForest(classe ~ ., data = data_pmltraining.train)
val_rfmodel.predict <- predict(val_rfmodel, data_pmltraining.test, type = "class")
val_rfcm <- confusionMatrix(val_rfmodel.predict, data_pmltraining.test$classe)
val_rfcm
plot(val_rfcm$table, col = val_rfcm$byClass, main = paste("Random Forest Confusion Matrix: Accuracy =", round(val_rfcm$overall['Accuracy'], 4)))

## Generalized boosted regression prediction
set.seed(12345)
val_fitControl <- trainControl(method = "repeatedcv", number = 5, repeats = 1)
val_gbmmodel <- train(classe ~ ., data = data_pmltraining.train, method = "gbm", trControl = val_fitControl, verbose = FALSE)
val_gbmmodel.predict <- predict(val_gbmmodel, newdata = data_pmltraining.test)
val_gbmcm <- confusionMatrix(val_gbmmodel.predict, data_pmltraining.test$classe)
val_gbmcm
plot(val_gbmcm$table, col = val_gbmcm$byClass, main = paste("Generalized Boosted Regression Confusion Matrix: Accuracy =", round(val_gbmcm$overall['Accuracy'], 4)))

## Final prediction model against final testing dataset
val_ooserror <- 1 - round(val_rfcm$overall['Accuracy'], 4)
val_ooserror
val_rfmodel.final <- predict(val_rfmodel, data_pmltesting, type = "class")
val_rfmodel.final

## Submit to coursera
pml_write_files = function(x){
  n = length(x)
  for(i in 1:n){
    filename = paste0("problem_id_",i,".txt")
    write.table(x[i], file = filename,quote = FALSE, row.names = FALSE, col.names = FALSE)
  }
}

pml_write_files(val_rfmodel.final)