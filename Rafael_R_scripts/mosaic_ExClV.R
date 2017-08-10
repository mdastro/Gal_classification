#read the data in and eliminate the class variable for the clustering process
require(mclust)
require(reshape2)
library(plyr)
library(gridExtra)
library(circlize)
require(data.table)
source("ExClVal.R")
Dat <- read.csv("..//Dataset/class_WHAN_BPT_D5.csv",header=T)
AGN <- data.frame(xx_BPT = log(Dat$NII/Dat$H_alpha,10),yy_BPT = log(Dat$OIII/Dat$H_beta,10),
                  yy_WHAN = log(Dat$EW_H_alpha,10), dn4000_obs = Dat$dn4000_obs, dn4000_synth = Dat$dn4000_synth)                 



# Subsampling for testing, not necessary in the final run
#test_index <- sample(seq_len(nrow(AGN)),replace=F, size = 10000)
AGN_short <- AGN[,c("xx_BPT", "yy_BPT","yy_WHAN")]

set.seed(42)
CLUST4 <- Mclust(AGN_short,G = 4,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                 modelName = "VVV")#Initialization with 1000 for higher speed

set.seed(42)
CLUST5 <- Mclust(AGN_short,G = 5,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                 modelName = "VVV")#Initialization with 1000 for higher speed


Dat$BPT_name = as.factor(Dat$class_BPT)
Dat$BPT_name4 = as.factor(Dat$class_BPT4)

Dat$WHAN_name = as.factor(Dat$class_WHAN)
#class BPT: (no class, SF, composite, AGN) = (0, 1, 2, 3)
# class WHAN: (no class, SF, sAGN, wAGN, retired, passive) = (0, 1, 2, 3, 4, 5) 
Dat$BPT_name <- revalue(Dat$BPT_name, c("1"="SF","2"="Composite","3"="AGN") )
Dat$BPT_name4 <-revalue(Dat$BPT_name4, c("1"="SF","2"="Composite","3"="AGN","4"="LINERs") )

Dat$WHAN_name <- revalue(Dat$WHAN_name, c("1"="SF","2"="sAGN","3"="wAGN","4"="retired") )


# Plotting the clustering results
clust<-CLUST5

class<-Dat$BPT_name4
data <- AGN_short[,1:2]

class2<-Dat$WHAN_name
data2 <- AGN_short[,c(1,3)]


fit0 <- ExClVal(class,clust,data=data)
fit<- ExClVal(class2,clust,data=data2)



#BPT
bptggclust <- c()
for (i in 1:4){
  for (j in 1:3){ 
 bptggclust <- rbind(bptggclust,data.frame(x=fit0$pdfCluster[[i,j]]$x,y=fit0$pdfCluster[[i,j]]$y,classc = paste("GC",i,"/",levels(class)[j],sep=""),
                                           class = paste("GC",i,sep="") ))
  }
}

bptggclust$cc <- rep("clust",nrow(bptggclust))

bptggclass <- c()
for (i in 1:4){
  for (j in 1:3){ 
  bptggclass  <- rbind(bptggclass ,data.frame(x=fit0$pdfClass[[i,j]]$x,y=fit0$pdfClass[[i,j]]$y,classc = paste("GC",i,"/",levels(class)[j],sep=""),
                                              class = levels(class)[j]))
}
}
bptggclass$cc <- rep("class",nrow(bptggclass))
gg_bpt_all<-rbind(bptggclust,bptggclass)
gg_bpt_all$cc <- as.factor(gg_bpt_all$cc)
gg_bpt_all$classc <- factor(gg_bpt_all$classc,
levels = c("GC1/SF","GC2/SF","GC3/SF","GC4/SF","GC1/Composite","GC2/Composite","GC3/Composite","GC4/Composite","GC1/AGN",               
 "GC2/AGN","GC3/AGN", "GC4/AGN"))

pdf("mosaic_bpt.pdf",width = 7,height = 6)
ggplot(
  data=gg_bpt_all,aes(x=x,y=y,group=cc,fill=class,alpha=cc))+
  geom_polygon()+
  theme_bw()+
  scale_alpha_manual(values=c(0.8,0.7))+
  scale_fill_manual(values=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00","gray80","gray80","gray80"
                               ))+
  scale_y_continuous(breaks=pretty_breaks())+
  scale_x_continuous(breaks=c(-7.5,0,7.5))+
  theme(legend.position = "none",plot.title = element_text(hjust=0.5),
        axis.title.y=element_text(vjust=0.75),
        axis.title.x=element_text(vjust=-0.25),
        text = element_text(size=18))+xlab("LD1")+ylab("Density")+
  facet_wrap(~classc,ncol=4,nrow=3)+
  coord_cartesian(xlim=c(-8,8.5))
dev.off()



    
# WHAN
whanggclust <- c()
for (i in 1:4){
  for (j in 1:4){ 
    whanggclust <- rbind(whanggclust,data.frame(x=fit$pdfCluster[[i,j]]$x,y=fit$pdfCluster[[i,j]]$y,classc = paste("GC",i,"/",levels(class2)[j],sep=""),
                                              class = paste("GC",i,sep="") ))
  }
}

whanggclust$cc <- rep("clust",nrow(whanggclust))

whanggclass <- c()
for (i in 1:4){
  for (j in 1:4){ 
    whanggclass  <- rbind(whanggclass ,data.frame(x=fit$pdfClass[[i,j]]$x,y=fit$pdfClass[[i,j]]$y,classc = paste("GC",i,"/",levels(class2)[j],sep=""),
                                                class = levels(class2)[j]))
  }
}
whanggclass$cc <- rep("class",nrow(whanggclass))
gg_whan_all<-rbind(whanggclust,whanggclass)
gg_whan_all$cc <- as.factor(gg_whan_all$cc)
gg_whan_all$classc <- factor(gg_whan_all$classc,
                            levels = c("GC1/SF","GC2/SF","GC3/SF","GC4/SF","GC1/sAGN","GC2/sAGN","GC3/sAGN","GC4/sAGN","GC1/wAGN",               
                                       "GC2/wAGN","GC3/wAGN", "GC4/wAGN",
                                       "GC1/retired",               
                                       "GC2/retired","GC3/retired", "GC4/retired"))

pdf("mosaic_whan.pdf",width = 7,height = 8)
ggplot(
  data=gg_whan_all,aes(x=x,y=y,group=cc,fill=class,alpha=cc))+
  geom_polygon()+
  theme_bw()+
  scale_alpha_manual(values=c(0.8,0.7))+
  scale_fill_manual(values=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00","gray80","gray80","gray80","gray80"
  ))+
  scale_y_continuous(breaks=pretty_breaks())+
  scale_x_continuous(breaks=c(-7.5,0,7.5))+
  theme(legend.position = "none",plot.title = element_text(hjust=0.5),
        axis.title.y=element_text(vjust=0.75),
        axis.title.x=element_text(vjust=-0.25),
        text = element_text(size=18))+xlab("LD1")+ylab("Density")+
  facet_wrap(~classc,ncol=4,nrow=4)+
  coord_cartesian(xlim=c(-8,8))
dev.off()





## Chord Diagram

bbb<-1-round(fit0$KL,3)
bbb[bbb<=0.93]<-0
rownames(bbb) <-c("GC1","GC2","GC3","GC4","GC5")

pdf("Figs/chord_bpt5.pdf",width = 5,height = 5)
chordDiagram(bbb,directional = 1,
             row.col=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00","brown"),
             grid.col=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00","brown",
                        "gray","gray","gray","gray"))
dev.off()

www<-1-round(fit$KL,3)
www[www<=0.93]<-0
rownames(www) <-c("GC1","GC2","GC3","GC4","GC5")
pdf("Figs/chord_whan5.pdf",width = 5,height = 5)
chordDiagram(www,directional = 1,row.col=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00",
                                           "brown"),
             grid.col=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00","brown",
                        "gray","gray","gray","gray"))
dev.off()



