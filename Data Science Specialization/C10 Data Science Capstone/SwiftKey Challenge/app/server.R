library(shiny)
source("predict.R")

shinyServer(function(input, output) {
  
  output$str_passedinput <- renderText({input$str_input})
  
  output$str_output <- renderText({
    paste(input$str_input, predict(input$str_input))
  })
  
})