l <- read.csv("") # UWB
m <- read.csv("", header = TRUE) # GPS

ly <- c(1:length(m$x))
###---------------------------------------###

gd <- data.frame()
off <- c(-50:50)

diff <- function(off, ly){
for(i in ly){
    if(i+off <=0){
     }
    else{
    a = sqrt((m$x[i]- l$x[i+off+1])^2 + (m$y[i]- l$y[i+off+1])^2)
    output <- data.frame(a)
    gd = rbind(gd, output)
      }
}
  return(gd)
}


val <- data.frame()
for (i in off){
  pop <- diff(ly, i)
  bb <- mean(na.omit(pop$a))
  j <- data.frame("Offset" = i, "Mean Distance" = bb)
  val = rbind(val, j)
  new = data.frame("Offset Index" = val$Offset[which.min(val$Mean.Distance)], 
                   "Mean.Distance" = min(val$Mean.Distance))
}

new12 = rbind(new12, new)
#write.csv(val, "dsdsd.csv")
###---------------------------------------###
new12
