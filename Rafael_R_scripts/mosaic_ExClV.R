#read the data in and eliminate the class variable for the clustering process
require(mclust)
require(reshape2)
library(plyr)
library(gridExtra)
library(circlize)

Dat <- read.csv("..//Dataset/Class_WHAN_BPT_D4.csv",header=T)
AGN <- data.table(xx_BPT = log(Dat$NII/Dat$H_alpha,10),yy_BPT = log(Dat$OIII/Dat$H_beta,10),
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


fit0 <- ExClVal(class,clust,data=data)
fit<- ExClVal(class2,clust,data=data2)



#BPT
bptggclust <- c()
for (i in 1:4){
  for (j in 1:3){ 
 bptggclust <- rbind(bptggclust,data.frame(x=fit0$pdfCluster[[i,j]]$x,y=fit0$pdfCluster[[i,j]]$y,classc = paste("G",i,"/",levels(class)[j],sep=""),
                                           class = paste("G",i,sep="") ))
  }
}

bptggclust$cc <- rep("clust",nrow(bptggclust))

bptggclass <- c()
for (i in 1:4){
  for (j in 1:3){ 
  bptggclass  <- rbind(bptggclass ,data.frame(x=fit0$pdfClass[[i,j]]$x,y=fit0$pdfClass[[i,j]]$y,classc = paste("G",i,"/",levels(class)[j],sep=""),
                                              class = levels(class)[j]))
}
}
bptggclass$cc <- rep("class",nrow(bptggclass))
gg_bpt_all<-rbind(bptggclust,bptggclass)
gg_bpt_all$cc <- as.factor(gg_bpt_all$cc)
gg_bpt_all$classc <- factor(gg_bpt_all$classc,
levels = c("G1/SF","G2/SF","G3/SF","G4/SF","G1/Composite","G2/Composite","G3/Composite","G4/Composite","G1/AGN",               
 "G2/AGN","G3/AGN", "G4/AGN"))

pdf("mosaic_bpt.pdf",width = 7,height = 6)
ggplot(
  data=gg_bpt_all,aes(x=x,y=y,group=cc,fill=class,alpha=cc))+
  geom_polygon()+
  theme_bw()+
  scale_alpha_manual(values=c(0.8,0.7))+
  scale_fill_manual(values=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00","gray80","gray80","gray80"
                               ))+
  scale_y_continuous(breaks=pretty_breaks())+
  theme(legend.position = "none",plot.title = element_text(hjust=0.5),
        axis.title.y=element_text(vjust=0.75),
        axis.title.x=element_text(vjust=-0.25),
        text = element_text(size=18))+xlab("LD1")+ylab("Density")+
  facet_wrap(~classc,ncol=4,nrow=3)
dev.off()



    
# WHAN
whanggclust <- c()
for (i in 1:4){
  for (j in 1:4){ 
    whanggclust <- rbind(whanggclust,data.frame(x=fit$pdfCluster[[i,j]]$x,y=fit$pdfCluster[[i,j]]$y,classc = paste("G",i,"/",levels(class2)[j],sep=""),
                                              class = paste("G",i,sep="") ))
  }
}

whanggclust$cc <- rep("clust",nrow(whanggclust))

whanggclass <- c()
for (i in 1:4){
  for (j in 1:4){ 
    whanggclass  <- rbind(whanggclass ,data.frame(x=fit$pdfClass[[i,j]]$x,y=fit$pdfClass[[i,j]]$y,classc = paste("G",i,"/",levels(class2)[j],sep=""),
                                                class = levels(class2)[j]))
  }
}
whanggclass$cc <- rep("class",nrow(whanggclass))
gg_whan_all<-rbind(whanggclust,whanggclass)
gg_whan_all$cc <- as.factor(gg_whan_all$cc)
gg_whan_all$classc <- factor(gg_whan_all$classc,
                            levels = c("G1/SF","G2/SF","G3/SF","G4/SF","G1/sAGN","G2/sAGN","G3/sAGN","G4/sAGN","G1/wAGN",               
                                       "G2/wAGN","G3/wAGN", "G4/wAGN",
                                       "G1/retired",               
                                       "G2/retired","G3/retired", "G4/retired"))

pdf("mosaic_whan.pdf",width = 7,height = 8)
ggplot(
  data=gg_whan_all,aes(x=x,y=y,group=cc,fill=class,alpha=cc))+
  geom_polygon()+
  theme_bw()+
  scale_alpha_manual(values=c(0.8,0.7))+
  scale_fill_manual(values=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00","gray80","gray80","gray80","gray80"
  ))+
  scale_y_continuous(breaks=pretty_breaks())+
  theme(legend.position = "none",plot.title = element_text(hjust=0.5),
        axis.title.y=element_text(vjust=0.75),
        axis.title.x=element_text(vjust=-0.25),
        text = element_text(size=18))+xlab("LD1")+ylab("Density")+
  facet_wrap(~classc,ncol=4,nrow=4)
dev.off()





## Chord Diagram

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



\