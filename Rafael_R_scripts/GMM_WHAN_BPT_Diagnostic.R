#----------------------------------------------------------------##----------------------------------------------------------------#
library(e1071);require(mclust);library(RColorBrewer);require(ggthemes);
require(ggpubr);require(ggplot2);require(plotly);require(MASS);require(cluster)
library(fpc);library(plyr);library(reshape);require(ggsci);require(plot3D);require(rgl)
#----------------------------------------------------------------##----------------------------------------------------------------#
set.seed(42)
#----------------------------------------------------------------##----------------------------------------------------------------#
# Read and store data
#AGN<- read.table("/Users/rafael/Dropbox/artigos/Meusartigos/IAA-WGC/Github/Gal_classification/Dataset/class_WHAN_BPT.dat",header=F)
#colnames(AGN)<-c("id", "xx_BPT", "yy_BPT", "class_BPT", "xx_WHAN",
#                         "yy_WHAN", "EW_NII_WHAN", "class_WHAN")

Dat <- read.csv("..//Dataset/Class_WHAN_BPT_D4.csv",header=T)
AGN <- data.frame(xx_BPT = log(Dat$NII/Dat$H_alpha,10),yy_BPT = log(Dat$OIII/Dat$H_beta,10),
                  yy_WHAN = log(Dat$EW_H_alpha,10), dn4000_obs = Dat$dn4000_obs, dn4000_synth = Dat$dn4000_synth)                 

# Subsampling for testing, not necessary in the final run
#test_index <- sample(seq_len(nrow(AGN)),replace=F, size = 10000)
AGN_short <- AGN[,c("xx_BPT", "yy_BPT","yy_WHAN")]
rm(AGN)
#----------------------------------------------------------------##----------------------------------------------------------------#


#----------------------------------------------------------------##----------------------------------------------------------------#

#--Number of Clusters via BIC and ICL----------------------------------------------------------------#
BIC<-c()
ICL<-c()

for(i in 1:10){
CLUST <- Mclust(AGN_short,G = i,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                modelName = "VVV")#Initialization with 1000 for higher speed
BIC <- append(BIC,CLUST$bic)
ICL <- append(ICL,icl(CLUST))
}


gBI<-data.frame(BIC=BIC,ICL=ICL,K=seq(1:10))
ggdata<-melt(gBI,'K')
ggdata$K<-as.factor(ggdata$K)



g1<-ggplot(ggdata,aes(x=K,y=value,group=variable,color=variable,shape=variable,linetype=variable))+
  geom_point()+theme_bw()+scale_color_npg(name = "")+geom_line()+scale_shape_cleveland(name = "")+
  scale_linetype_stata(name = "")+
  theme(legend.background = element_rect(fill="white"),
        legend.key = element_rect(fill = "white",color = "white"),
        plot.background = element_rect(fill = "white"),
        legend.position=c(0.75,0.75),legend.background = element_rect(fill=NA),
        axis.title.y = element_text(vjust = 0.1,margin=margin(0,10,0,0)),
        axis.title.x = element_text(vjust = -0.25),
        text = element_text(size = 20,family="serif"))+ylab("Value")
#----------------------------------------------------------------##----------------------------------------------------------------#

#----------------------------------------------------------------##----------------------------------------------------------------#
# Shinkage of clusters via Entropy analysis, changepoint diagnostics----------------------------------------------------------------#
CLUST2 <- Mclust(AGN_short,G = 1:10,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                modelName = "VVV")
CLUSTCOMBI <- clustCombi(AGN_short, CLUST2)
source("xlog.R")
source("pcws2_reg.R")

# Extract data for Entropy plot using parts of the Mclust functions (sorry if look messy for now  )
zx<- CLUSTCOMBI$MclustOutput$z
combiM <- CLUSTCOMBI$combiM

ent <- numeric()
Kmax <- ncol(zx)
z0 <- zx
for (K in Kmax:1) 
{
  z0 <- t(combiM[[K]] %*% t(z0))
  ent[K] <- -sum(xlog(z0))
}
pcwsreg <- pcws2_reg(1:Kmax,ent)
# Plot using ggplot2
mypal = pal_npg("nrc", alpha = 0.7)(9)
mypal
gent <-data.frame(x=as.factor(1:Kmax),y=ent)
seg1 <- data.frame(x=1:pcwsreg$c,y=pcwsreg$a1*(1:pcwsreg$c) + pcwsreg$b1)
seg2 <- data.frame(x=pcwsreg$c:Kmax,y=pcwsreg$a2*(pcwsreg$c:Kmax) + pcwsreg$b2)
g2<-ggplot(gent,aes(x=x,y=y))+
  geom_point(aes(x=x,y=y),shape=24,size=2)+theme_bw()+
  geom_line(data=seg1,aes(x=x,y=y),color=mypal[1],linetype="dotdash",size=1)+
  geom_line(data=seg2,aes(x=x,y=y),color=mypal[2],linetype="dotted",size=1)+
  theme(legend.background = element_rect(fill="white"),
        legend.key = element_rect(fill = "white",color = "white"),
        plot.background = element_rect(fill = "white"),
        legend.position="none",
        axis.title.y = element_text(vjust = 0.1,margin=margin(0,10,0,0)),
        axis.title.x = element_text(vjust = -0.25),
        text = element_text(size = 20,family="serif"))+xlab("K")+ylab("Entropy")
#+geom_segment(mapping=aes(x=3, y=0.5, xend=3, yend=8750), arrow=arrow(), size=0.25, color="gray50")


#----------------------------------------------------------------##----------------------------------------------------------------#

# Silhouette

#--Number of Clusters via BIC and ICL----------------------------------------------------------------#
index0 <- sample(seq_len(nrow(AGN_short)),replace=F, size = 10000)
SIL<-list()
for(i in 2:10){
  CLUST <- Mclust(AGN_short,G = i,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                  modelName = "VVV")#Initialization with 1000 for higher speed
  ss <- silhouette(CLUST$classification[index0],daisy(AGN_short[index0,]))
  SIL[[i]] <- ss
}

gS <- list()
ggS <-c()
for(i in 2:10){
  gS[[i]] <-data.frame(SIL[[i]][,],K=rep(i,nrow(SIL[[i]][,])))    
  ggS <-rbind(ggS,gS[[i]])
}
ggS$K <- as.factor(ggS$K)


g3<-ggplot(ggS,aes(y=sil_width,x=K,fill=K))+
  #  stat_boxplot(geom ='errorbar') + 
  geom_boxplot(colour="gray90",outlier.shape = NA,outlier.size = NA, coef = 0.25,alpha=0.75)+
  stat_summary(fun.y=median,aes(group = 2),
               geom="line",linetype="dashed",size=1.5)+
  stat_summary(fun.y=median,
               geom="point",size=3.25,shape=21,fill="white",color="white")+
  theme_bw()+
  scale_color_npg(name = "")+
  scale_fill_npg()+
  theme(legend.background = element_rect(fill="white"),
        legend.key = element_rect(fill = "white",color = "white"),
        plot.background = element_rect(fill = "white"),
        legend.position="none",
        axis.title.y = element_text(vjust = 0.1,margin=margin(0,10,0,0)),
        axis.title.x = element_text(vjust = -0.25),
        text = element_text(size = 20,family="serif"))+ylab("Silhouette")+
  xlab("K")+coord_cartesian(ylim=c(-0.25,0.7))
#----------------------------------------------------------------##----------------------------------------------------------------#





library("gridExtra")
grid.arrange(g1, g2,g3, ncol = 3)


quartz.save(type = 'pdf', file = 'Nclust.pdf',width = 16, height = 4.5)

#
#----------------------------------------------------------------##----------------------------------------------------------------#





