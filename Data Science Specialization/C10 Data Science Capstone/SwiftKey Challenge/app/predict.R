library(tm)
library(NLP)

load(file = "data/df_uniwordfreq.RData")
load(file = "data/df_biwordfreq.RData")
load(file = "data/df_triwordfreq.RData")
load(file = "data/df_quadwordfreq.RData")

predict <- function(input) {
  x <- input
  x <- removePunctuation(x)
  x <- removeNumbers(x)
  x <- tolower(x)
  x <- stripWhitespace(x)
  x <- unlist(strsplit(x , " "))
  
  for(i in min(length(x), 3):1) {
    y <- NA
    match <- NA
    ngram <- paste(tail(x, i), collapse = " ")
    ngram <- paste0("^", ngram, " ")
    if(i == 3) {
      match <- grep(ngram, df_quadwordfreq$ngram)[1]
      y <- df_quadwordfreq[match, 1]
    } else if(i == 2) { 
      match <- grep(ngram, df_triwordfreq$ngram)[1]
      y <- df_triwordfreq[match, 1]
    } else if(i == 1) { 
      match <- grep(ngram, df_biwordfreq$ngram)[1]
      y <- df_biwordfreq[match, 1]
    }
    if(!is.na(y)) {
      return(gsub(ngram, "", y))
      break
    }
  }
  
  return(paste0(df_uniwordfreq[1, 1]))
}