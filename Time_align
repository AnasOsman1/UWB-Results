library(prettydoc)
library(dplyr)
library(ggplot2)
library(ggrepel)
library(ggthemes)
library(ggExtra)
library(knitr)
library(tidyverse)
library(fs)
library(gridExtra)
library(grid)
library(patchwork)
library(gifski)
library(plotly)
library(ggplotlyExtra)
library(kableExtra)
library(readr)
library(extrafont)
library(shiny)
setwd("/Users/anasosman/Downloads/Cohdaf/Cohda/GPS_CAD")
# Reading the Cohda Wireless fiLes
#GPS <-read_csv("novatel_cad.csv")
GPS <-read_csv("05_cad.csv")
#Cohda$Speed <- Cohda$Speed * 3.6
#GPS <- read.csv("GPS_CAD.csv")
#GPS2 <- read.csv("mk5_cad.csv")
GPS$time_stamps <- GPS$time_stamps/10^5
GPS$time_stamps <- GPS$time_stamps - GPS$time_stamps%%1
#GPS$time_stamps <- GPS$time_stamps

path = "/Users/anasosman/Downloads/Expf_Uwb/zigzag/zigzag_UWB_CAD"
setwd(path)

l <- fs::dir_ls(path)

files<-list.files(path)
filer <-files
namess <- files
file_contents<- list()

for (i in seq_along(l)){
  file_contents[[i]]<- read_csv(file = l[[i]])
}

file_contents <- set_names(file_contents, namess)

namess%>%
  map(function(path){
    read_csv(path, show_col_types = FALSE)
  })

setwd("/Users/anasosman/Downloads/Expf_Uwb/zigzag/Cohda_zigzag")
# Time Align
counter = 1
f <- data.frame()
time_filter <- function(time_in){
   b <- filter(GPS,  time_stamps %in% time_in[1]:time_in[length(time_in)])%>%
                  select(time_stamps, x, y)
  GPS <- GPS %>%
    select(time_stamps, x, y)
  for(j in 1:length(time_in)){
   for (i in 1:length(GPS$time_stamps)){
    if (GPS$time_stamps[i] == time_in[j]){
      element <- GPS[i,]
      f = rbind(f,element)
  }
  else{
        next
  }
  }
  }
  # b <- filter(GPS, time_stamps >= time_in[1] & 
  #               time_stamps <= time_in[length(time_in)])%>%
  #   select(time_stamps, x, y)
  
  print(paste("The number of missing elements is ", length(b$time_stamps)- length(time_in), sep = " = "))
  return(f)
}
out <- numeric() # Concatenate for all files

for (i in file_contents) {
  a <- i$time_stamps
  h <- assign(paste("a", i$secs, sep = ""), time_filter(a))
  out <- c(out, h)
}

args_in <- seq(1, length(out), 3) # We are only interested in time, X and Y


for (i in args_in) {
    write.csv(data.frame(out[i], out[i + 1], out[i +2])
          , file = paste0(counter, ".csv"), )
    counter = counter+1
}
