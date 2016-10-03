#----------------------------------------------------------------##----------------------------------------------------------------#
library(e1071);require(mclust);library(RColorBrewer);require(ggthemes);
require(ggpubr);require(ggplot2);require(plotly);require(MASS);require(cluster)
library(fpc);library(plyr);library(reshape);require(ggsci);require(plot3D);
require(rgl);library(spatstat);library("gridExtra")
#----------------------------------------------------------------##----------------------------------------------------------------#
source("gg_ellipse.R")
source("plot_BPT.R")
source("plot_WHAN.R")

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


CLUST2 <- Mclust(AGN_short,G = 2,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                modelName = "VVV")#Initialization with 1000 for higher speed
CLUST3 <- Mclust(AGN_short,G = 3,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                 modelName = "VVV")#Initialization with 1000 for higher speed

CLUST4 <- Mclust(AGN_short,G = 4,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                 modelName = "VVV")#Initialization with 1000 for higher speed


B2<-plot_BPT(CLUST2)
B3<-plot_BPT(CLUST3)
B4<-plot_BPT(CLUST4)
W2<-plot_WHAN(CLUST2)
W3<-plot_WHAN(CLUST3)
W4<-plot_WHAN(CLUST4)


grid.arrange(B2, B3,B4,W2,W3,W4, ncol = 3,nrow=2)
quartz.save(type = 'pdf', file = 'Clusters.pdf',width = 16, height = 8)
#----------------------------------------------------------------##----------------------------------------------------------------#


# Residual Analysis 

sim2<-sim(modelName = CLUST2$modelName,
          parameters = CLUST2$parameters,
          n = nrow(AGN_short), seed = 0)
sim3<-sim(modelName = CLUST3$modelName,
          parameters = CLUST3$parameters,
          n = nrow(AGN_short), seed = 0)

sim4<-sim(modelName = CLUST4$modelName,
         parameters = CLUST4$parameters,
         n = nrow(AGN_short), seed = 0)
xrng = range(AGN_short$xx_BPT)
yrng = range(AGN_short$yy_BPT)



d0_BPT = kde2d(AGN_short$xx_BPT, AGN_short$yy_BPT, lims=c(xrng, yrng), n=100,
           h = rep(0.1, 2))
d2_BPT = kde2d(sim2[,2],
           sim2[,3], lims=c(xrng, yrng), n=100,
           h = rep(0.1, 2))
d3_BPT = kde2d(sim3[,2],
           sim3[,3], lims=c(xrng, yrng), n=100,
           h = rep(0.1, 2))
d4_BPT = kde2d(sim4[,2],
           sim4[,3], lims=c(xrng, yrng), n=100,
           h = rep(0.1, 2))


fit2<-lm(d0_BPT$z~d2_BPT$z)
fit3<-lm(d0_BPT$z~d3_BPT$z)
fit4<-lm(d0_BPT$z~d4_BPT$z)
require(plot3D)
image2D(z=fit4$residuals)


filled.contour(d4_BPT,
               color.palette=colorRampPalette(c('white','blue','yellow','red','darkred')))

filled.contour(d0_BPT,
               color.palette=colorRampPalette(c('white','blue','yellow','red','darkred'))
)
diff12 <- d0_BPT  
diff12$z = (d0_BPT$z - d2_BPT$z)
filled.contour(diff12,
               col=colorRampPalette(c('blue','white','red'))(22),nlevels=19)

rownames(diff12$z) = diff12$x
colnames(diff12$z) = diff12$y

# Now melt it to long format
diff12.m = melt(diff12$z, id.var=rownames(diff12))
names(diff12.m) = c("x","y","z")

# Plot difference between geyser2 and geyser1 density
ggplot(diff12.m, aes(x, y, z=z, fill=z)) +
  geom_tile() +
  stat_contour(aes(colour=..level..), binwidth=0.001) +
  scale_fill_gradient2(low="red3",mid="white", high="blue3", midpoint=0) +
  scale_colour_gradient2(low="red3", mid="white", high="blue3", midpoint=0) +
  coord_cartesian(xlim=xrng, ylim=yrng) +
  guides(colour=FALSE)+theme_bw()


















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



