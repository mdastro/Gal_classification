#read the data in and eliminate the class variable for the clustering process
require(mclust)
require(reshape2)
library(plyr)
library(gridExtra)
library(circlize)
Dat <- read.csv("..//Dataset/Class_WHAN_BPT_D4.csv",header=T)
AGN <- data.frame(xx_BPT = log(Dat$NII/Dat$H_alpha,10),yy_BPT = log(Dat$OIII/Dat$H_beta,10),
                  yy_WHAN = log(Dat$EW_H_alpha,10), dn4000_obs = Dat$dn4000_obs, dn4000_synth = Dat$dn4000_synth)                 

# Subsampling for testing, not necessary in the final run
#test_index <- sample(seq_len(nrow(AGN)),replace=F, size = 10000)
AGN_short <- AGN[,c("xx_BPT", "yy_BPT","yy_WHAN")]

set.seed(42)
CLUST4 <- Mclust(AGN_short,G = 4,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                 modelName = "VVV")#Initialization with 1000 for higher speed
Dat$BPT_name = as.factor(Dat$class_BPT)
Dat$WHAN_name = as.factor(Dat$class_WHAN)
#class BPT: (no class, SF, composite, AGN) = (0, 1, 2, 3)
# class WHAN: (no class, SF, sAGN, wAGN, retired, passive) = (0, 1, 2, 3, 4, 5) 
Dat$BPT_name <- revalue(Dat$BPT_name, c("1"="SF","2"="Composite","3"="AGN") )

Dat$WHAN_name <- revalue(Dat$WHAN_name, c("1"="SF","2"="sAGN","3"="wAGN","4"="retired") )


# Plotting the clustering results
clust<-CLUST4

class<-Dat$BPT_name
data <- AGN_short[,1:2]

class2<-Dat$WHAN_name
data2 <- AGN_short[,c(1,3)]




fit0<- ExClVal(class,clust,data=data)
fit<- ExClVal(class2,clust,data=data2)

bbb<-1-fit0$KL
bbb[bbb<=0.93]<-0

pdf("Figs/chord_bpt.pdf",width = 5,height = 5)
chordDiagram(bbb,directional = 1,
row.col=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00"),
grid.col=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00",
                                              "gray","gray","gray"))
dev.off()

www<-1-fit$KL
www[www<=0.95]<-0
pdf("Figs/chord_whan.pdf",width = 5,height = 5)
chordDiagram(www,directional = 1,row.col=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00"),
                       grid.col=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00",
                                  "gray","gray","gray","gray"))
dev.off()





pdf("mosaic_bpt.pdf",width = 12,height = 8)
grid.arrange(fit0$gg[[1,1]],fit0$gg[[2,1]],fit0$gg[[3,1]],fit0$gg[[4,1]],
             fit0$gg[[1,2]],fit0$gg[[2,2]],fit0$gg[[3,2]],fit0$gg[[4,2]],
             fit0$gg[[1,3]],fit0$gg[[2,3]],fit0$gg[[3,3]],fit0$gg[[4,3]],
             ncol=4,nrow=3)
dev.off()



pdf("mosaic_whan.pdf",width = 12,height = 12)
grid.arrange(fit$gg[[1,1]],fit$gg[[2,1]],fit$gg[[3,1]],fit$gg[[4,1]],
             fit$gg[[1,2]],fit$gg[[2,2]],fit$gg[[3,2]],fit$gg[[4,2]],
             fit$gg[[1,3]],fit$gg[[2,3]],fit$gg[[3,3]],fit$gg[[4,3]],
             fit$gg[[1,4]],fit$gg[[2,4]],fit$gg[[3,4]],fit$gg[[4,4]],
             ncol=4,nrow=4)
dev.off()







\