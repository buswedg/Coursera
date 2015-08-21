library(shiny)
library(ggplot2)

data_training <- read.csv("data/train.csv")
dataset <- data_training


shinyUI(
  
  navbarPage("Coursera Developing Data Products CP1",
  
    tabPanel("Plot",
    
      sidebarPanel(
      
        h4('Plot Settings'),
        
        sliderInput('sampleSize', 'Sample Size', min = 1, max = nrow(dataset),
          value = min(500, nrow(dataset)), step = 100, round = 0),
        
        selectInput('x', 'X', names(dataset), selected = "Age"),
        selectInput('y', 'Y/Fill', names(dataset), selected = "Survived"),
        selectInput('type', 'Type', list('Density', 'Dot Plot', 'Histogram', 'Scatterplot'), selected = "Histogram"),
        
        br(),
        
        h4('Variable Descriptions'),
        
        tags$ul(
          
          tags$li('survival - Passeger Did/Did Not Survive (0 = No; 1 = Yes)'), 
          tags$li('pclass - Passenger Class (1 = 1st; 2 = 2nd; 3 = 3rd)'), 
          tags$li('name - Name'), 
          tags$li('sex - Sex'), 
          tags$li('age - Age'), 
          tags$li('sibsp - Number of Siblings/Spouses Aboard'), 
          tags$li('parch - Number of Parents/Children Aboard'), 
          tags$li('ticket - Ticket Number'), 
          tags$li('fare - Passenger Fare'), 
          tags$li('cabin - Cabin'),     
          tags$li('embarked - Port of Embarkation (C = Cherbourg; Q = Queenstown; S = Southampton)')
          
        )
        
      ),
      
      mainPanel(
          
          h2('Dataset Plot'),
          
          p('Use the side panel to change which variables are shown in the plot and how they are presented (i.e. X-axis, Y-axis, variable colour).'),
          
          plotOutput('plot')
          
      )
        
    ),
    
    tabPanel("Data",
             
      mainPanel(

        h2('Original Dataset'),
        
        downloadButton('downloadData', 'Download'),
        
        br(),
        br(),
        
        dataTableOutput('dtable')
        
      )
             
    ),
    
    tabPanel("About",
      
      mainPanel(
        
        h2('About'),
        
        includeMarkdown("README.md")
        
      )
      
    )
    
  )
  
)
