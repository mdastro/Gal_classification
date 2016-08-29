library(e1071);require(mclust);library(RColorBrewer);require(ggthemes);
require(ggpubr);require(ggplot2)

AGN<- read.table("/Users/rafael/Dropbox/artigos/Meusartigos/IAA-WGC/Github/Gal_classification/Dataset/class_WHAN_BPT.dat",header=F)
colnames(AGN)<-c("id", "xx_BPT", "yy_BPT", "class_BPT", "xx_WHAN",
                         "yy_WHAN", "EW_NII_WHAN", "class_WHAN")

#write.csv(AGN,"class_WHAN_BPT.csv",row.names=F,quote=FALSE)

test_index <- sample(seq_len(nrow(AGN)),replace=F, size = 10000)
AGN_short <- AGN[test_index,c("xx_BPT", "yy_BPT","yy_WHAN")]


CLUST <- Mclust(AGN_short,G = 3)
plot(CLUST)



gdata <- data.frame(x=AGN_short$xx_BPT,y=AGN_short$yy_BPT,z=AGN_short$yy_WHAN, type=as.factor(CLUST$classification))

#-----------------------
# BPT PLOT
#-----------------------
xx = seq(-4, 0.0, 0.01)
Ka = 0.61 / (xx - 0.05) + 1.30
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
  ylab(expression(paste('log ([OIII]/H', beta, ')'))) +
  scale_colour_manual(values = c("#66c2a5","#fc8d62","#8da0cb","#e78ac3"))+
  theme_pubr() + 
  geom_line(aes(x=xx,y=Ka),data=gKa,size=1.25,linetype="dashed",color="gray25")+
  geom_line(aes(x=xx1,y=Ke),data=gKe,size=1.25,linetype="dotted",color="gray25")+
  geom_line(aes(x=xx2,y=Sey),data=gSey,size=0.75,linetype="dotdash",color="gray25")+
  coord_cartesian(xlim=c(-1.8,1.3),ylim=c(-1.5,1.55))+
  theme(legend.position = "none",plot.title = element_text(hjust=0.5),
        axis.title.y=element_text(vjust=0.75),
        axis.title.x=element_text(vjust=-0.25),
        text = element_text(size=20))




ggplot(data=gdata,aes(x=x,y=z))+geom_point(aes(color=type))+
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

# Diagnostics

S1<-silhouette(CLUST$classification,daisy(AGN_short))

S_BPT<-silhouette(AGN[test_index,]$class_BPT,daisy(AGN_short))


S_WHAN<-silhouette(AGN[test_index,]$class_WHAN,daisy(AGN_short))
















# 3D plot

x <-  AGN_short[,1]
y <-  AGN_short[,2]
z <-  AGN_short[,3]

require(car)
require(scatterplot3d)
scatter3d(x,y,z, groups = as.factor(CLUST$classification),
          surface = FALSE)

library(plotly)
plot_ly(x = x, y = y, z = z, color  = as.factor(CLUST$classification),type = "scatter3d", mode = "markers") %>% 
  layout(scene = list(
           xaxis = list(title = "LogNII_Ha"), 
           yaxis = list(title = "EWHa"), 
           zaxis = list(title = "LogOIII_Hb")))  



