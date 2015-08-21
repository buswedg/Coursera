## R Programming
## Programming Assignment 2: Lexical Scoping
## cachematrix.R

## Functions calculate the inverse of a matrix, which is then saved to cache so that
## it may be reused the next time the user attempts to calculate the matrix inverse.


## makeCacheMatrix:
## Function creates "matrix" object, which contains a list of sub-functions to:
## 1. set the value of the matrix
## 2. get the value of the matrix
## 3. set the value of the inverse
## 4. get the value of the inverse

makeCacheMatrix <- function(x = matrix()) {
  
  i <- NULL
  
  ## 'set' subfunction: Accept matrix 'y', store it as matrix 'x' and delete the inverted matrix 'i'. Note: 'a <- makeCacheMatrix(x)' = 'a$set(x)'
  set <- function(y) {
    x <<- y
    i <<- NULL
  }
  
  ## 'get' subfunction: Return matrix 'x'. Note: cachesolve calls this to retrieve matrix 'x' if inversion is required.
  get <- function() x
  
  ## 'setinv' subfunction: Accept inverted matrix 'inverse' and store it as inverted matrix 'i'. Note: cachesolve sends its inverted matrix 'i' to this.
  setinv <- function(inverse) i <<- inverse
  
  ## 'getinv' subfunction: Return inverted matrix 'i'.
  getinv <- function() i
  
  ## Lists the 'set', 'get', 'setinv', 'getinv' subfunctions.
  list(set = set, get = get,
       setinv = setinv,
       getinv = getinv)
}


## cachesolve:
## Function first checks to see if the inverse matrix has already been caclulated.
## If so, it retrieves the matrix from cache. Otherwise, it calculates the matrix
## inverse and sends the matrix to cache.

cachesolve <- function(x, ...) {
  
  ## Call inverted matrix 'i' from 'getinv' subfunction, and store it as inverted matrix 'i'.
  i <- x$getinv()
  
  ## Check if inverted matrix 'i' is not null (cached). If 'i' is cached, return cached inverted matrix 'i'.
  if(!is.null(i)) {
    message("getting cached data")
    return(i)
  }
  
  ## If inverted matrix 'i' is not cached, call matrix 'x' from 'get' subfunction and store it as matrix 'data'.
  data <- x$get()
  
  ## Inverse matrix 'data' and store it as inverted matrix 'i'.
  i <- solve(data, ...)
  
  ## Send inverted matrix 'i' to 'setinv' subfunction.
  x$setinv(i)
  
  i
}

test = function(mat){
  
  temp = makeCacheMatrix(mat)
  
  start.time = Sys.time()
  cachesolve(temp)
  dur = Sys.time() - start.time
  print(dur)
  
  start.time = Sys.time()
  cachesolve(temp)
  dur = Sys.time() - start.time
  print(dur)
  
}

mat1 = matrix(rnorm(1000000), nrow = 1000, ncol = 1000)
test(mat1)