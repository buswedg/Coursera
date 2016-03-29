
#Data Science Capstone
###Course Project: CP_template


###Introduction
This document presents the results of the Course Project for the Coursera course: Data Science Capstone. This assessment required the student to explore data from the 'Yelp Dataset Challenge' [site](http://www.yelp.com/dataset_challenge).


###Data
Each file is composed of a single object type, one json-object per-line.

* yelp_academic_dataset_business.json
* yelp_academic_dataset_checkin.json
* yelp_academic_dataset_review.json
* yelp_academic_dataset_tip.json
* yelp_academic_dataset_user.json


###1. Loading Packages/ Data

```r
for (package in c('RJSONIO', 'R.utils')) {
  if (!require(package, character.only = TRUE, quietly = FALSE)) {
    install.packages(package)
    library(package, character.only = TRUE)
  }
}

val_dfpath <- paste(getwd(), "data", sep = "/")
val_dfname <- c("yelp_academic_dataset_business.json")
```

####yelp_academic_dataset_business.json

{
    'type': 'business',
    'business_id': (encrypted business id),
    'name': (business name),
    'neighborhoods': [(hood names)],
    'full_address': (localized address),
    'city': (city),
    'state': (state),
    'latitude': latitude,
    'longitude': longitude,
    'stars': (star rating, rounded to half-stars),
    'review_count': review count,
    'categories': [(localized category names)]
    'open': True / False (corresponds to closed, not business hours),
    'hours': {
        (day_of_week): {
            'open': (HH:MM),
            'close': (HH:MM)
        },
        ...
    },
    'attributes': {
        (attribute_name): (attribute_value),
        ...
    },
}

```r
val_df <- paste(val_dfpath, val_dfname[1], sep = "/")
data_business.raw <- fromJSON(sprintf("[%s]", paste(readLines(val_df), collapse=",")))

business_id <- sapply(data_business.raw, "[[", "business_id")
name <- sapply(data_business.raw, "[[", "name")
neighborhoods <- sapply(data_business.raw, "[[", "neighborhoods")
full_address <- sapply(data_business.raw, "[[", "full_address")
city <- sapply(data_business.raw, "[[", "city")
state <- sapply(data_business.raw, "[[", "state")
latitude <- sapply(data_business.raw, "[[", "latitude")
longitude <- sapply(data_business.raw, "[[", "longitude")
stars <- sapply(data_business.raw, "[[", "stars")
review_count <- sapply(data_business.raw, "[[", "review_count")
categories <- sapply(data_business.raw, "[[", "categories")
open <- sapply(data_business.raw, "[[", "open")
hours <- sapply(data_business.raw, "[[", "hours")
attributes <- sapply(data_business.raw, "[[", "attributes")

data_business <- do.call(rbind, Map(data.frame, 
  business_id = business_id, 
  name = name, 
  full_address = full_address,
  city = city,
  state = state,
  latitude = latitude,
  longitude = longitude,
  stars = stars,
  review_count = review_count,
  open = open))
```


####yelp_academic_dataset_checkin.json
{
    'type': 'checkin',
    'business_id': (encrypted business id),
    'checkin_info': {
        '0-0': (number of checkins from 00:00 to 01:00 on all Sundays),
        '1-0': (number of checkins from 01:00 to 02:00 on all Sundays),
        ...
        '14-4': (number of checkins from 14:00 to 15:00 on all Thursdays),
        ...
        '23-6': (number of checkins from 23:00 to 00:00 on all Saturdays)
    }, # if there was no checkin for a hour-day block it will not be in the dict
}


####yelp_academic_dataset_review.json
{
    'type': 'review',
    'business_id': (encrypted business id),
    'user_id': (encrypted user id),
    'stars': (star rating, rounded to half-stars),
    'text': (review text),
    'date': (date, formatted like '2012-03-14'),
    'votes': {(vote type): (count)},
}


###yelp_academic_dataset_tip.json
{
    'type': 'tip',
    'text': (tip text),
    'business_id': (encrypted business id),
    'user_id': (encrypted user id),
    'date': (date, formatted like '2012-03-14'),
    'likes': (count),
}


####yelp_academic_dataset_user.json
{
    'type': 'user',
    'user_id': (encrypted user id),
    'name': (first name),
    'review_count': (review count),
    'average_stars': (floating point average, like 4.31),
    'votes': {(vote type): (count)},
    'friends': [(friend user_ids)],
    'elite': [(years_elite)],
    'yelping_since': (date, formatted like '2012-03'),
    'compliments': {
        (compliment_type): (num_compliments_of_this_type),
        ...
    },
    'fans': (num_fans),
}



