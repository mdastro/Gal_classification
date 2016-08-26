library(e1071);require(mclust);library(RColorBrewer);require(ggthemes);
require(ggpubr)

AGN<- read.csv("/Users/rafael/Dropbox/artigos/Meusartigos/IAA-WGC/Github/AGN_unsupervised/script/clean_AGN_data.csv",header=T)
AGN_high <- data.frame(log(AGN$NII/AGN$H_alpha,10),log(AGN$EW_H_alpha,10))
test_index <- sample(seq_len(nrow(AGN_high)),replace=F, size = 15000)
AGN_short <- AGN_high[test_index,]

CLUST <- Mclust(AGN_short,G = 1:4)
plot(CLUST)

CLUSTCOMBI <- clustCombi(AGN_short, CLUST)
plot(CLUSTCOMBI,AGN_short)

gdata <- data.frame(x=AGN_short[,1],y=AGN_short[,2],type=as.factor(CLUST$classification))

#-----------------------
# WHAN PLOT
#-----------------------
xx = -0.4
SR = 0.61 / (xx - 0.05) + 1.30
gKa <- data.frame(xx,Ka)
#-----------------------
xx1 = seq(-4, 0.4, 0.01)
Ke = 0.61 / (xx1 - 0.47) + 1.19
gKe <- data.frame(xx1,Ke)

#-----------------------
xx2 = seq(-0.43, 5, 0.01)
Sey = 1.05 * xx2 + 0.45
gSey <- data.frame(xx2,Sey)



ggplot(data=gdata,aes(x=x,y=y))+geom_point(aes(color=type))+
  xlab(expression(paste('log ([NII]/H', alpha, ')'))) +
  ylab(expression(paste('log EW (H', alpha, ')'))) +
  scale_colour_manual(values = c("#66c2a5","#fc8d62","#8da0cb","#e78ac3","#fb9a99"))+
  theme_pubr() + 
  coord_cartesian(xlim=c(-1.5,1.3),ylim=c(-1.1,2.5))+
  theme(legend.position = "none",plot.title = element_text(hjust=0.5),
        axis.title.y=element_text(vjust=0.75),
        axis.title.x=element_text(vjust=-0.25),
        text = element_text(size=20))+
  geom_segment(aes(x = -0.4, y = 5, xend = -0.4, yend = 0.5),size=1.25,linetype="dashed",color="gray25")+
  geom_hline(yintercept = 0.5,linetype="dashed",size=1.25,color="gray25")+
geom_segment(aes(x = -0.4, y = 0.78, xend = 2, yend = 0.78),linetype="dashed",size=1.25,color="gray25")
  
  
