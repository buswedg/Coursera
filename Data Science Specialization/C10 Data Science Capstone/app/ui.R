library(shiny)
library(markdown)

shinyUI(
  navbarPage("Coursera Data Science Specialization",
    
    tabPanel("Text Predictor",
      sidebarPanel(
        textInput("str_input", label = "Input Text", value = "The cat sat"),
        br(),
        submitButton("Make Prediction")
      ),
      mainPanel(
        h2("Text Predictor"),
        h3("Instructions:"),
        p("Use the side panel to input text for the prediction application,
          then click 'Make Prediction' to show the next word in the predicted sentence."),
        br(),
        h3("Predicted Sentence:"),
        textOutput("str_output")
      )
    ),
    
    tabPanel("About",
      mainPanel(
        h2("About"),
        includeMarkdown("README.md")
      )                
    )
    
  )
)