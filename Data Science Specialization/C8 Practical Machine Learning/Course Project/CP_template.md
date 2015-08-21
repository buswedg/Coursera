
#Practical Machine Learning
###Course Project: CP_template


###Introduction
This document presents the results of the Course Project for the Coursera course: Practical Machine Learning. This assessment required the student to explore personal activity data in order to predict the manner in which they did the exercise.


###Data
This assignment makes use of data collected from accelerometers on the belt, forearm, arm, and dumbell of six participants. More information is available from the website here: [raw data](http://groupware.les.inf.puc-rio.br/har) (see the section on the Weight Lifting Exercise Dataset).

* Training Dataset: [training data](https://d396qusza40orc.cloudfront.net/predmachlearn/pml-training.csv)
* Testing Dataset: [test data](https://d396qusza40orc.cloudfront.net/predmachlearn/pml-testing.csv)


###1. Loading Packages/ Data

```r
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
```


###2. Pre-process the Data
Read data

```r
data_pmltraining.raw <- read.csv(paste(val_dfpath, val_dfname[1], sep = "/"), na.strings = c("NA", "#DIV/0!", ""))
data_pmltesting.raw <- read.csv(paste(val_dfpath, val_dfname[2], sep = "/"), na.strings = c("NA", "#DIV/0!", ""))
```

Check the original data

```r
dim(data_pmltraining.raw)
```

```
## [1] 19622   160
```

```r
## str(data_pmltraining.raw)
## summary(data_pmltraining.raw)
```

Remove near zero covariates

```r
data_pmltraining.nzv <- nearZeroVar(data_pmltraining.raw, saveMetrics = TRUE)
data_pmltraining <- data_pmltraining.raw[, !data_pmltraining.nzv$nzv]
remove(data_pmltraining.nzv)
```

Remove first column of the training dataset

```r
data_pmltraining <- data_pmltraining[, -1]
```

Remove variables with more than 60% NA values

```r
val_pmltraining.nav <- which((colSums(!is.na(data_pmltraining)) >= 0.6 * nrow(data_pmltraining)))
data_pmltraining <- data_pmltraining[, val_pmltraining.nav]
remove(val_pmltraining.nav)
```

Split into training and testing datasets

```r
data_pmltraining.inTrain <- createDataPartition(data_pmltraining$classe, p = 0.6, list = FALSE)
data_pmltraining.train <- data_pmltraining[data_pmltraining.inTrain, ]
data_pmltraining.test <- data_pmltraining[-data_pmltraining.inTrain, ]
remove(data_pmltraining.inTrain)
```

Transform training and testing datasets

```r
val_pmltraining.allcol <- colnames(data_pmltraining.train)
val_pmltraining.datacol <- colnames(data_pmltraining.train[, -ncol(data_pmltraining.train)])
data_pmltraining.test <- data_pmltraining.test[val_pmltraining.allcol]
data_pmltesting <- data_pmltesting.raw[val_pmltraining.datacol]
remove(val_pmltraining.allcol, val_pmltraining.datacol)
```

Coerce data classes between training and final testing datasets

```r
data_pmltesting <- rbind(data_pmltraining.train[2, -ncol(data_pmltraining.train)] , data_pmltesting)
data_pmltesting <- data_pmltesting[-1, ]
```

Check the processed data

```r
dim(data_pmltraining.train)
```

```
## [1] 11776    58
```

```r
## str(data_pmltraining.train)
## summary(data_pmltraining.train)
```


```r
dim(data_pmltraining.test)
```

```
## [1] 7846   58
```

```r
## str(data_pmltraining.test)
## summary(data_pmltraining.test)
```


```r
dim(data_pmltesting)
```

```
## [1] 20 57
```

```r
## str(data_pmltesting)
## summary(data_pmltesting)
```


###3. Prediction Modelling

####Decision tree prediction

```r
set.seed(12345)
val_dtmodel <- rpart(classe ~ ., data = data_pmltraining.train, method = "class")
val_dtmodel.predict <- predict(val_dtmodel, data_pmltraining.test, type = "class")
val_dtcm <- confusionMatrix(val_dtmodel.predict, data_pmltraining.test$classe)
val_dtcm
```

```
## Confusion Matrix and Statistics
## 
##           Reference
## Prediction    A    B    C    D    E
##          A 2148   74   10    2    0
##          B   66 1273  102   60    0
##          C   18  162 1238  216   63
##          D    0    9   18  952  184
##          E    0    0    0   56 1195
## 
## Overall Statistics
##                                           
##                Accuracy : 0.8674          
##                  95% CI : (0.8597, 0.8749)
##     No Information Rate : 0.2845          
##     P-Value [Acc > NIR] : < 2.2e-16       
##                                           
##                   Kappa : 0.8324          
##  Mcnemar's Test P-Value : NA              
## 
## Statistics by Class:
## 
##                      Class: A Class: B Class: C Class: D Class: E
## Sensitivity            0.9624   0.8386   0.9050   0.7403   0.8287
## Specificity            0.9847   0.9640   0.9291   0.9678   0.9913
## Pos Pred Value         0.9615   0.8481   0.7295   0.8186   0.9552
## Neg Pred Value         0.9850   0.9614   0.9789   0.9500   0.9625
## Prevalence             0.2845   0.1935   0.1744   0.1639   0.1838
## Detection Rate         0.2738   0.1622   0.1578   0.1213   0.1523
## Detection Prevalence   0.2847   0.1913   0.2163   0.1482   0.1594
## Balanced Accuracy      0.9735   0.9013   0.9171   0.8541   0.9100
```

Decision tree prediction has a reported accuracy against the training dataset:

```r
round(val_dtcm$overall['Accuracy'], 4)
```

```
## Accuracy 
##   0.8674
```


```r
plot(val_dtcm$table, col = val_dtcm$byClass, main = paste("Decision Tree Confusion Matrix: Accuracy =", round(val_dtcm$overall['Accuracy'], 4)))
```

![](figure/unnamed-chunk-15-1.png) 

#### Random forest prediction

```r
set.seed(12345)
val_rfmodel <- randomForest(classe ~ ., data = data_pmltraining.train)
val_rfmodel.predict <- predict(val_rfmodel, data_pmltraining.test, type = "class")
val_rfcm <- confusionMatrix(val_rfmodel.predict, data_pmltraining.test$classe)
val_rfcm
```

```
## Confusion Matrix and Statistics
## 
##           Reference
## Prediction    A    B    C    D    E
##          A 2232    1    0    0    0
##          B    0 1517    1    0    0
##          C    0    0 1367    3    0
##          D    0    0    0 1283    0
##          E    0    0    0    0 1442
## 
## Overall Statistics
##                                           
##                Accuracy : 0.9994          
##                  95% CI : (0.9985, 0.9998)
##     No Information Rate : 0.2845          
##     P-Value [Acc > NIR] : < 2.2e-16       
##                                           
##                   Kappa : 0.9992          
##  Mcnemar's Test P-Value : NA              
## 
## Statistics by Class:
## 
##                      Class: A Class: B Class: C Class: D Class: E
## Sensitivity            1.0000   0.9993   0.9993   0.9977   1.0000
## Specificity            0.9998   0.9998   0.9995   1.0000   1.0000
## Pos Pred Value         0.9996   0.9993   0.9978   1.0000   1.0000
## Neg Pred Value         1.0000   0.9998   0.9998   0.9995   1.0000
## Prevalence             0.2845   0.1935   0.1744   0.1639   0.1838
## Detection Rate         0.2845   0.1933   0.1742   0.1635   0.1838
## Detection Prevalence   0.2846   0.1935   0.1746   0.1635   0.1838
## Balanced Accuracy      0.9999   0.9996   0.9994   0.9988   1.0000
```

Random forest prediction has a reported accuracy against the training dataset:

```r
round(val_rfcm$overall['Accuracy'], 4)
```

```
## Accuracy 
##   0.9994
```


```r
plot(val_rfcm$table, col = val_rfcm$byClass, main = paste("Random Forest Confusion Matrix: Accuracy =", round(val_rfcm$overall['Accuracy'], 4)))
```

![](figure/unnamed-chunk-18-1.png) 

#### Generalized boosted regression prediction

```r
set.seed(12345)
val_fitControl <- trainControl(method = "repeatedcv", number = 5, repeats = 1)
val_gbmmodel <- train(classe ~ ., data = data_pmltraining.train, method = "gbm", trControl = val_fitControl, verbose = FALSE)
val_gbmmodel.predict <- predict(val_gbmmodel, newdata = data_pmltraining.test)
val_gbmcm <- confusionMatrix(val_gbmmodel.predict, data_pmltraining.test$classe)
val_gbmcm
```

```
## Confusion Matrix and Statistics
## 
##           Reference
## Prediction    A    B    C    D    E
##          A 2231    1    0    0    0
##          B    1 1513    2    0    0
##          C    0    2 1361    4    0
##          D    0    2    5 1280    4
##          E    0    0    0    2 1438
## 
## Overall Statistics
##                                           
##                Accuracy : 0.9971          
##                  95% CI : (0.9956, 0.9981)
##     No Information Rate : 0.2845          
##     P-Value [Acc > NIR] : < 2.2e-16       
##                                           
##                   Kappa : 0.9963          
##  Mcnemar's Test P-Value : NA              
## 
## Statistics by Class:
## 
##                      Class: A Class: B Class: C Class: D Class: E
## Sensitivity            0.9996   0.9967   0.9949   0.9953   0.9972
## Specificity            0.9998   0.9995   0.9991   0.9983   0.9997
## Pos Pred Value         0.9996   0.9980   0.9956   0.9915   0.9986
## Neg Pred Value         0.9998   0.9992   0.9989   0.9991   0.9994
## Prevalence             0.2845   0.1935   0.1744   0.1639   0.1838
## Detection Rate         0.2843   0.1928   0.1735   0.1631   0.1833
## Detection Prevalence   0.2845   0.1932   0.1742   0.1645   0.1835
## Balanced Accuracy      0.9997   0.9981   0.9970   0.9968   0.9985
```

Generalized boosted regression prediction has a reported accuracy against the training dataset:

```r
round(val_gbmcm$overall['Accuracy'], 4)
```

```
## Accuracy 
##   0.9971
```


```r
plot(val_gbmcm$table, col = val_gbmcm$byClass, main = paste("Generalized Boosted Regression Confusion Matrix: Accuracy =", round(val_gbmcm$overall['Accuracy'], 4)))
```

![](figure/unnamed-chunk-21-1.png) 


###4. Model Selection
Random forest prediction model is selected due to its superior accuracy. The expected out-of-sample error is calculated as 1 - accuracy for predictions made against the cross-validation set:

```r
val_ooserror <- 1 - round(val_rfcm$overall['Accuracy'], 4)
val_ooserror
```

```
## Accuracy 
##    6e-04
```

With an accuracy above 99% on the cross-validation data, it is expected that few or none of the test samples will be missclassified.

```r
val_rfmodel.final <- predict(val_rfmodel, data_pmltesting, type = "class")
val_rfmodel.final
```

```
##  2  3 41  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 
##  B  A  B  A  A  E  D  B  A  A  B  C  B  A  E  E  A  B  B  B 
## Levels: A B C D E
```


###5. Coursera Submission

```r
pml_write_files = function(x){
  n = length(x)
  for(i in 1:n){
    filename = paste0("problem_id_",i,".txt")
    write.table(x[i], file = filename,quote = FALSE, row.names = FALSE, col.names = FALSE)
  }
}

pml_write_files(val_rfmodel.final)
```
