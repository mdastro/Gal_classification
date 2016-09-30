#----------------------------------------------------------------##----------------------------------------------------------------#
library(e1071);require(mclust);library(RColorBrewer);require(ggthemes);
require(ggpubr);require(ggplot2);require(plotly);require(MASS);require(cluster)
library(fpc);library(plyr);library(reshape);require(ggsci);require(plot3D);require(rgl);library(spatstat)
#----------------------------------------------------------------##----------------------------------------------------------------#



#----------------------------------------------------------------##----------------------------------------------------------------#
# Read and store data
AGN<- read.table("/Users/rafael/Dropbox/artigos/Meusartigos/IAA-WGC/Github/Gal_classification/Dataset/class_WHAN_BPT.dat",header=F)
colnames(AGN)<-c("id", "xx_BPT", "yy_BPT", "class_BPT", "xx_WHAN",
                         "yy_WHAN", "EW_NII_WHAN", "class_WHAN")


# Subsampling for testing, not necessary in the final run
#test_index <- sample(seq_len(nrow(AGN)),replace=F, size = 10000)
AGN_short <- AGN[,c("xx_BPT", "yy_BPT","yy_WHAN")]
rm(AGN)
#----------------------------------------------------------------##----------------------------------------------------------------#


#----------------------------------------------------------------##----------------------------------------------------------------#

#--Number of Clusters fixed----------------------------------------------------------------#

CLUST <- Mclust(AGN_short,G = 3,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                modelName = "VVV")#Initialization with 1000 for higher speed

#--Get Ellipse info----------------------------------------------------------------#
#source("gg_ellipse.R")
EL68<-df.ellipses(CLUST,level=0.68)
EL95<-df.ellipses(CLUST,level=0.95)
EL99<-df.ellipses(CLUST,level=0.997)

El_BPT68<-subset(EL68,xvar=="yy_BPT" & yvar=="xx_BPT")
El_BPT68$classification <-as.factor(El_BPT68$classification)
#
El_BPT95<-subset(EL95,xvar=="yy_BPT" & yvar=="xx_BPT")
El_BPT95$classification <-as.factor(El_BPT95$classification)
#
El_BPT99<-subset(EL99,xvar=="yy_BPT" & yvar=="xx_BPT")
El_BPT99$classification <-as.factor(El_BPT99$classification)
#

El_WHAN<-subset(EL,xvar=="yy_WHAN" & yvar=="xx_BPT")
El_WHAN$classification <-as.factor(El_WHAN$classification)
#----------------------------------------------------------------##----------------------------------------------------------------#
# Customized plots via ggplot2
gdata <- data.frame(x=AGN_short$xx_BPT,y=AGN_short$yy_BPT,z=AGN_short$yy_WHAN, type=as.factor(CLUST$classification),
                    uncertainty = CLUST$uncertainty )
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

# BPT projection
ggplot(data=gdata,aes(x=x,y=y))+
  xlab(expression(paste('log ([NII]/H', alpha, ')'))) +
  ylab(expression(paste('log ([OIII]/H', beta, ')'))) +
#  stat_ellipse(type="norm",geom = "polygon", alpha = 1/2,aes(group=type,fill=type),level = 0.997)+
  geom_point(color="gray80",alpha=0.2,size=0.5)+
  scale_colour_manual(values = c("#66c2a5","#fc8d62","#8da0cb","#e78ac3"))+
  scale_fill_manual(values = c("#66c2a5","#fc8d62","#8da0cb","#e78ac3"))+
 # geom_path(data=El_BPT99,aes(x=xval,y=yval,group=classification,color=classification
#                                 ),size=1)+
  geom_polygon(data=El_BPT95,aes(x=xval,y=yval,group=classification,
              color=classification,fill=classification),
               size=1,alpha=0.2)+
  
  geom_polygon(data=El_BPT68,aes(x=xval,y=yval,group=classification,color=classification,
                              fill=classification
                                 ),size=1,alpha=0.4)+

 theme_bw() + 
  geom_line(aes(x=xx,y=Ka),data=gKa,size=1.25,linetype="dashed",color="gray25")+
  geom_line(aes(x=xx1,y=Ke),data=gKe,size=1.25,linetype="dotted",color="gray25")+
  geom_line(aes(x=xx2,y=Sey),data=gSey,size=0.75,linetype="dotdash",color="gray25")+
  
  coord_cartesian(xlim=c(-1.7,1.3),ylim=c(-1.4,1.5))+
  theme(legend.position = "none",plot.title = element_text(hjust=0.5),
        axis.title.y=element_text(vjust=0.75),
        axis.title.x=element_text(vjust=-0.25),
        text = element_text(size=20))

# WHAN projection
ggplot(data=gdata,aes(x=x,y=z))+
  xlab(expression(paste('log ([NII]/H', alpha, ')'))) +
  ylab(expression(paste('log EW (H', alpha, ')'))) +
#  stat_ellipse(type="norm",geom = "polygon", alpha = 1/2,aes(group=type,fill=type),level = 0.997)+
  geom_point(aes(color=type,shape=type),alpha=0.4,size=0.75)+
   scale_colour_manual(values = c("#66c2a5","#fc8d62","#8da0cb","#e78ac3","#fb9a99"))+
  scale_fill_manual(values = c("#66c2a5","#fc8d62","#8da0cb","#e78ac3"))+
  geom_path(data=El_WHAN,aes(x=xval,y=yval,group=classification,color=classification),size=1)+
   theme_bw() + 
  coord_cartesian(xlim=c(-1.5,1.3),ylim=c(-1.1,2.5))+
  theme(legend.position = "none",plot.title = element_text(hjust=0.5),
        axis.title.y=element_text(vjust=0.75),
        axis.title.x=element_text(vjust=-0.25),
        text = element_text(size=20))+
  geom_segment(aes(x = -0.4, y = 5, xend = -0.4, yend = 0.5),size=1.25,linetype="dashed",color="gray25")+
 geom_hline(yintercept = 0.5,linetype="dashed",size=1.25,color="gray25")+
  geom_segment(aes(x = -0.4, y = 0.78, xend = 2, yend = 0.78),linetype="dashed",size=1.25,color="gray25")
#----------------------------------------------------------------##----------------------------------------------------------------#


#----------------------------------------------------------------##----------------------------------------------------------------#

dr = MclustDR(CLUST)


# Residual Analysis 
xrng = range(gdata$x)
yrng = range(gdata$y)

group1<-data.frame(x=CLUST$data[CLUST$classification==1 & CLUST$uncertainty < 0.5,1],
                   y= CLUST$data[CLUST$classification==1 & CLUST$uncertainty < 0.5,2],
                   p=CLUST$z[CLUST$classification==1 & CLUST$uncertainty < 0.5,1])

d1 = kde2d(CLUST$data[CLUST$classification==1 & CLUST$uncertainty < 0.3,1],
           CLUST$data[CLUST$classification==1 & CLUST$uncertainty < 0.3,2], lims=c(xrng, yrng), n=100,
           h = rep(0.1, 2))

d2 = kde2d(CLUST$data[CLUST$classification==2 & CLUST$uncertainty < 0.3,1],
           CLUST$data[CLUST$classification==2 & CLUST$uncertainty < 0.3,2], lims=c(xrng, yrng), n=100,
           h = rep(0.1, 2))

d3 = kde2d(CLUST$data[CLUST$classification==3 & CLUST$uncertainty < 0.3,1],
           CLUST$data[CLUST$classification==3 & CLUST$uncertainty < 0.3,2], lims=c(xrng, yrng), n=100,
           h = rep(0.1, 2))


d0 = kde2d(gdata$x, gdata$y, lims=c(xrng, yrng), n=100,
           h = rep(0.1, 2))

filled.contour(d1,
               color.palette=colorRampPalette(c('white','blue','yellow','red','darkred')))
filled.contour(d2,
               color.palette=colorRampPalette(c('white','blue','yellow','red','darkred')))
filled.contour(d3,
               color.palette=colorRampPalette(c('white','blue','yellow','red','darkred')))
filled.contour(d0,
               color.palette=colorRampPalette(c('white','blue','yellow','red','darkred'))
)

diff12 <- d0 
diff12$z = d0$z - d1$z- d2$z- d3$z

filled.contour(diff12,
               color.palette=colorRampPalette(c('white','blue','yellow','red','darkred'))
)

rownames(diff12$z) = diff12$x
colnames(diff12$z) = diff12$y

# Now melt it to long format
diff12.m = melt(diff12$z, id.var=rownames(diff12))
names(diff12.m) = c("x","y","z")

# Plot difference between geyser2 and geyser1 density
ggplot(diff12.m, aes(x, y, z=z, fill=z)) +
  geom_tile() +
  stat_contour(aes(colour=..level..), binwidth=0.001) +
  scale_fill_gradient2(low="red",mid="white", high="blue", midpoint=0) +
  scale_colour_gradient2(low=muted("red"), mid="white", high=muted("blue"), midpoint=0) +
  coord_cartesian(xlim=xrng, ylim=yrng) +
  guides(colour=FALSE)


















# 3D plot of classifications of ellipses 
CLUST3 <- Mclust(AGN_short[,c(3,1,2)],G = 3,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                 modelName = "VVV")
#----------------------------------------------------------------##----------------------------------------------------------------#
ellips <- ellipse3d(CLUST3$parameters$variance$sigma[,,1], 
                    centre = c(CLUST3$parameters$mean[1,1], CLUST3$parameters$mean[2,1], CLUST3$parameters$mean[3,1]), level = 0.95)
ellips2 <- ellipse3d(CLUST3$parameters$variance$sigma[,,2], 
                     centre = c(CLUST3$parameters$mean[1,2], CLUST3$parameters$mean[2,2], CLUST3$parameters$mean[3,2]), level = 0.95)
ellips3 <- ellipse3d(CLUST3$parameters$variance$sigma[,,3], 
                     centre = c(CLUST3$parameters$mean[1,3], CLUST3$parameters$mean[2,3], CLUST3$parameters$mean[3,3]), level = 0.95)
#ellips4 <- ellipse3d(CLUST3$parameters$variance$sigma[,,4], 
#                     centre = c(CLUST3$parameters$mean[1,4], CLUST3$parameters$mean[2,4], CLUST3$parameters$mean[3,4]), level = 0.95)

index <- sample(seq_len(nrow(AGN_short)),replace=F, size = 5000)
x <-  AGN_short[index,3]
y <-  AGN_short[index,1]
z <-  AGN_short[index,2]  


## Some configuration parameters:
fig.width       <- 1000
fig.height      <- 1000
def.font.size   <- 1.5
label.font.size <- 2
grid.lwd        <- 3
group.col <- c("#D46A6A","#D4B16A","#764B8E")
source("rgl_add_axes.R")
plot3d(x,y, z,  box = FALSE,
       type ="s", size=1,alpha=0.4,xlab = "EWHa", ylab = "LogNII_Ha", 
       zlab = "LogOIII_Hb",col=group.col[CLUST3$classification[index]])
# Add bounding box decoration
#rgl.bbox(color=c("gray90","black"),  shininess=3, alpha=0.8, nticks = 3 ) 
#rgl_add_axes(x, y, z, show.bbox = FALSE)
plot3d(ellips, col = "#D46A6A", alpha = 0.85, type = "wire",add = TRUE)
plot3d(ellips2, col = "#D4B16A", alpha = 0.85, add = TRUE, type = "wire")
plot3d(ellips3, col = "#764B8E", alpha = 0.85, add = TRUE, type = "wire")
#plot3d(ellips4, col = "#fdb462", alpha = 0.85, add = TRUE, type = "wire")
aspect3d(1,1,1)
## Add the grid
grid3d(side = c('x+','y+','z-'), lwd=grid.lwd)


rgl.snapshot("3D_ellipses.png", fmt="png", top=TRUE )



## Add the axes
axes3d("bbox",
       marklen=0.075,
       marklen.rel=FALSE,
       xat=c(-0.4,0,0.4,0.8,1.2,1.6,2),
       xunit=0, yunit=0, zunit=0, lwd=grid.lwd, col="black")



#play3d(spin3d(axis=c(1,0,0), rpm=4), duration=20)
movie3d(spin3d(axis=c(1,0,0), rpm=4), duration=10,
        dir="/Users/rafael/Downloads/")

writeWebGL(width = 500, height = 500)









# 3D plot of classifications

scatter3D_fancy <- function(x, y, z,..., colvar = z,col=col,colkey=colkey,pch=".")
{
  panelfirst <- function(pmat) {
    XY <- trans3D(x, y, z = rep(min(z), length(z)), pmat = pmat)
    scatter2D(XY$x, XY$y,col=col, colvar = colvar, pch = ".", 
              cex = 0.5, add = TRUE, colkey = FALSE)
    
    XY <- trans3D(x = rep(min(x), length(x)), y, z, pmat = pmat)
    scatter2D(XY$x, XY$y,col=col, colvar = colvar, pch = ".", 
              cex = 0.5, add = TRUE, colkey = FALSE)
    
  }
  scatter3D(x, y, z, ...,col=col, colvar = colvar, panel.first=panelfirst,
            colkey = colkey,cex = 2.75,pch=pch) 
}


scatter3D_fancy(x, y, z,colvar = as.integer(CLUST$classification),col = c("#D46A6A","#D4B16A","#764B8E"),
                colkey=F,
                box = T,ticktype = "detailed",theta=40,phi=20,
                zlab = "LogOIII_Hb",ylab="LogNII_Ha", d=20,
                xlab="EWHa",bty = "u",col.panel = "gray95",col.grid = "gray35",contour = T)

quartz.save(type = 'pdf', file = '3D_super.pdf',width = 11, height = 9)




#----------------------------------------------------------------##----------------------------------------------------------------#
# Internal validation

# Diagnostics via SI
S1<-silhouette(CLUST$classification,daisy(AGN_short))

S_BPT<-silhouette(AGN[test_index,]$class_BPT,daisy(AGN_short))

S_WHAN<-silhouette(AGN[test_index,]$class_WHAN,daisy(AGN_short))



# Boxplot of silhouette 
d1 <-data.frame(Si=S1[,3],model=rep("GMM",nrow(S1)))
d2<-data.frame(Si=S_BPT[,3],model=rep("BPT",nrow(S_BPT)))
d3<-data.frame(Si=S_WHAN[,3],model=rep("WHAN",nrow(S_WHAN)))
box_data <- rbind(d3,d2,d1)


ggplot(box_data,aes(x=model,y=Si,fill=model))+geom_boxplot(outlier.colour = "gray70",outlier.shape = 1, outlier.size = 0.75)+
  coord_cartesian(ylim=c(-0.525,.525))+ 
  scale_fill_npg()+ylab("Silhouette")+xlab("Method")+
  theme(legend.background = element_rect(fill="white"),
        legend.key = element_rect(fill = "white",color = "white"),
        plot.background = element_rect(fill = "white"),
        legend.position="none",
        axis.title.y = element_text(vjust = 0.1,margin=margin(0,10,0,0)),
        axis.title.x = element_text(vjust = -0.25),
        text = element_text(size = 25,family="serif"))


ggviolin(box_data, x = "model", y = "Si",fill = "model",add = "boxplot",add.params = list(fill = "white"))+
scale_fill_npg()+ylab("Silhouette")+xlab("Method")+
  theme(legend.background = element_rect(fill="white"),
        legend.key = element_rect(fill = "white",color = "white"),
        plot.background = element_rect(fill = "white"),
        legend.position="none",
        axis.title.y = element_text(vjust = 0.1,margin=margin(0,10,0,0)),
        axis.title.x = element_text(vjust = 0.5),
        text = element_text(size = 25,family="serif"))

quartz.save(type = 'pdf', file = 'boxplot_SI.pdf',width = 11, height = 8)

# External Validation

class_BPT<- as.factor(AGN[test_index,]$class_BPT)
class_BPT<-revalue(class_BPT, c("1"="SF", "2"="Composite","3" = "AGN"))

P_BPT<-as.data.frame(table(class_BPT,CLUST$classification))

ggplot(P_BPT, aes(class_BPT, Var2, fill=Freq)) + geom_tile()+xlab("BPT Class")+ylab("Cluster")+
  geom_text(aes(fill = P_BPT$Freq, label = round(P_BPT$Freq, 1)))+
  scale_fill_continuous_tableau()+theme_pubr()+
  theme(legend.background = element_rect(fill="white"),
        legend.key = element_rect(fill = "white",color = "white"),
        plot.background = element_rect(fill = "white"),
        legend.position="none",
        axis.title.y = element_text(vjust = 0.1,margin=margin(0,10,0,0)),
        axis.title.x = element_text(vjust = -0.25),
        text = element_text(size = 25,family="serif"))
quartz.save(type = 'pdf', file = 'CM.pdf',width = 10, height = 10)


# Stats
stat_BPT<-cluster.stats(daisy(AGN_short), CLUST$classification, as.numeric(class_BPT))
clust_stats <- cluster.stats(d = dist(AGN_short), 
                             types, CLUST$classification)

#----------------------------------------------------------------##----------------------------------------------------------------#





#frames = 360

#  for(i in 1:frames){
  # creating a name for each plot file with leading zeros
#  if (i < 10) {name = paste('000',i,'plot.png',sep='')}
  
#  if (i < 100 && i >= 10) {name = paste('00',i,'plot.png', sep='')}
#  if (i >= 100) {name = paste('0', i,'plot.png', sep='')}
#  ang = i
  #saves the plot as a .png file in the working directory
#  png(name)
#  scatter3D_fancy(x, y, z,colvar = as.integer(CLUST$classification),col = c("#D46A6A","#D4B16A","#764B8E"),
#                  colkey=F,
#                  box = T,ticktype = "detailed",theta=ang,phi=20,
#                  zlab = "LogOIII_Hb",ylab="LogNII_Ha", d=20,
#                  xlab="EWHa",bty = "u",col.panel = "gray95",col.grid = "gray35",contour = T)
#  dev.off()

#}


#text3D(1, 1, -2, labels = expression(theta[1]), add = TRUE, adj = 1)

library("plot3Drgl")
plotrgl()

quartz.save(type = 'pdf', file = '3D_super.pdf',width = 11, height = 9)



  
scatter3D(x, z, y,  pch = 16,colvar = as.integer(CLUST$classification),colkey = FALSE,col = c("#66c2a5","#fc8d62","#8da0cb"),
          pch = ".",
          box = T,ticktype = "detailed",theta=10,phi=15,
          zlab = "LogOIII_Hb",xlab="LogNII_Ha", d=30,
          ylab="EWHa",bty = "u",col.panel = "gray95",col.grid = "gray35",contour = T)





  
  
  

library(plotly)
plot_ly(x = x, y = y, z = z, color  = as.factor(CLUST$classification),type = "scatter3d", mode = "markers") %>% 
  layout(scene = list(
           xaxis = list(title = "LogNII_Ha"), 
           yaxis = list(title = "EWHa"), 
           zaxis = list(title = "LogOIII_Hb")))  



