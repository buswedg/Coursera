library(shiny)
library(ggplot2)
library(markdown)

data_training <- read.csv("data/train.csv")
dataset <- data_training


shinyServer(function(input, output) {
    
  dataset <- reactive(function() { data_training[sample(nrow(data_training), input$sampleSize), ] })
  
  selcolour <- reactive(function() { data_training[, input$colour] })
    
  output$dtable <- renderDataTable({ data_training }, options = list(bSortClasses = TRUE))
    
  output$plot <- renderPlot(function() {
    
    type <- switch(input$type,
                  "Density" = geom_density(),
                  "Dot Plot" = geom_dotplot(),
                  "Histogram" = geom_histogram(),
                  "Scatterplot" = geom_point())
  
    if (input$type == "Scatterplot") {
      
      p <- ggplot(dataset(), aes_string(x = input$x, y = input$y))
      
    } else {
      
      y = paste("as.factor(", input$y, ")", sep = "")
      
      p <- ggplot(dataset(), aes_string(x = input$x, fill = y))
      
    }
    
    p <- p + type
    
    print(p)
    
  }, height = 800)
    
  output$downloadData <- downloadHandler( 
      
    filename = function() { paste(input$dataset, '.csv', sep='') },
    content = function(file) { write.csv(dataset(), file) }
      
  )
  
})