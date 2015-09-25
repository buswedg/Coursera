# CodeBook
### Course Project 1: Tidy Data

---------------------


#### Data

Raw data set obtained from UCI Machine Learning repository. Specifically, the Human Activity Recognition Using Smartphones Data Set [1].

&nbsp;

#### Process

Raw data set is processed with run_analysis.R script to generate a new tidy data set [2].

The following steps are applied by the script:

1. **Merge training and test sets:**
Test and training data (X_train.txt, X_test.txt), subject ids (subject_train.txt, subject_test.txt) and activity ids (y_train.txt, y_test.txt) are merged to obtain a single data set. Variables are labelled with the names assigned by original collectors (features.txt).

2. **Extract mean and standard deviation variables:**
From the merged data set is extracted and intermediate data set with only the values of estimated mean (variables with labels that contain "mean") and standard deviation (variables with labels that contain "std").

3. **Use descriptive activity names:**
A new column is added to intermediate data set with the activity description. Activity id column is used to look up descriptions in activity_labels.txt.

4. **Label variables appropriately:**
Labels given from the original collectors were changed:  to obtain valid R names without parentheses, dashes and commas  to obtain more descriptive labels

5. **Create a tidy data set:**
From the intermediate data set is created a final tidy data set where numeric variables are averaged for each activity and each subject.

&nbsp;

#### Result

The tidy data set contains 10299 observations with 81 variables divided in:

- an activity label (Activity): WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS, SITTING, STANDING, LAYING

- an identifier of the subject who carried out the experiment (Subject): 1, 3, 5, 6, 7, 8, 11, 14, 15, 16, 17, 19, 21, 22, 23, 25, 26, 27, 28, 29, 30

- a 79-feature vector with time and frequency domain signal variables (numeric)

The data set is written to the file sensor_avg_by_act_sub.txt [3].

&nbsp;

#### References

1. Human Activity Recognition Using Smartphones Data Set. URL: <http://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones>. Accessed 15/05/2015

2.  Script to generate tidy data set. URL: <https://github.com/buswedg/Coursera/Getting%20and%20Cleaning%20Data/Course%20Project%201/run_analysis.R>.

3. Tidy data set. URL: <https://github.com/buswedg/Coursera/Getting%20and%20Cleaning%20Data/Course%20Project%201/data_sensor_avgactsub.txt>.