setwd('~/Desktop/uganda')
library(ggplot2)

## read in the data
data <- read.csv("election-results.csv",colClasses=c("numeric", rep("character",5),rep("numeric",12)), header = TRUE)

## get voter turnout number
data$totalper <- data$TOTAL.VOTES / data$REG.VOTERS

## percentage for the winner
data$winnervalid <- data$YOWERI..KAGUTA.MUSEVENI / data$VALID.VOTES

## order
data_sort <- data[order(data$totalper, decreasing = TRUE),]

## make fingerprint plot
d1 <- ggplot(as.data.frame(cbind(data$totalper, data$winnervalid)),aes(data$totalper, data$winnervalid))
d1 + geom_bin2d(bins=100) +
  scale_fill_gradientn(colours= c('blue','green','yellow','yellow','orange','orange','red','red','red')) +
  theme(panel.background = element_rect(fill = 'darkblue'), panel.grid.major = element_line(colour = 'darkblue'), panel.grid.minor = element_line(colour= 'darkblue')) +
  labs(x = "Voter Turnout %", y = "% of votes for winner")
