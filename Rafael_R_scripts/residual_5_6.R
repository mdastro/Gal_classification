# Residual Analysis 

set.seed(42)
CLUST5 <- Mclust(AGN_short,G = 5,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                 modelName = "VVV")#Initialization with 1000 for higher speed

set.seed(42)
CLUST6 <- Mclust(AGN_short,G = 6,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                 modelName = "VVV")#Initialization with 1000 for higher speed

sim5<-sim(modelName = CLUST5$modelName,
          parameters = CLUST5$parameters,
          n = nrow(AGN_short), seed = 0)
xrng = range(AGN_short$xx_BPT)
yrng = range(AGN_short$yy_BPT)

sim6<-sim(modelName = CLUST6$modelName,
          parameters = CLUST6$parameters,
          n = nrow(AGN_short), seed = 0)
xrng = range(AGN_short$xx_BPT)
yrng = range(AGN_short$yy_BPT)


d0_BPT = kde2d(AGN_short$xx_BPT, AGN_short$yy_BPT, lims=c(xrng, yrng), n=100,
               h = rep(0.05, 2))
d5_BPT = kde2d(sim5[,2],
               sim5[,3], lims=c(xrng, yrng), n=100,
               h = rep(0.05, 2))

d6_BPT = kde2d(sim6[,2],
               sim6[,3], lims=c(xrng, yrng), n=100,
               h = rep(0.05, 2))


#---------------------------------##---------------------------------#
# Plot smooth representation for original data and each cluster
rownames(d0_BPT$z) = d0_BPT$x
colnames(d0_BPT$z) = d0_BPT$y
rownames(d5_BPT$z) = d5_BPT$x
colnames(d5_BPT$z) = d5_BPT$y

rownames(d6_BPT$z) = d6_BPT$x
colnames(d6_BPT$z) = d6_BPT$y


# Now melt it to long format
d0_BPT.m = melt(d0_BPT$z, id.var=rownames(d0_BPT))
names(d0_BPT.m) = c("x","y","z")
d5_BPT.m = melt(d5_BPT$z, id.var=rownames(d5_BPT))
names(d5_BPT.m) = c("x","y","z")

d6_BPT.m = melt(d6_BPT$z, id.var=rownames(d6_BPT))
names(d6_BPT.m) = c("x","y","z")


gcomb<-rbind(d5_BPT.m,d6_BPT.m)
gcomb$case <- factor(rep(c("5 clusters","6 clusters"),each=1e4),levels=c("5 clusters","6 clusters"))
library(viridis)

colors <- colorRampPalette(c('white','cyan4','orange','red','darkred'))(30)
colors2 <- c('white',plasma(30))
# Plot difference 
gsim<-ggplot(gcomb, aes(x, y, z=z, fill=z)) +
  xlab(expression(paste('log [NII]/H', alpha))) +
  ylab(expression(paste('log [OIII]/H', beta))) +
  stat_contour(aes(fill =..level..,alpha=..level..), bins=5e2,geom="polygon") +
  scale_fill_gradientn(colours=colors) +
  coord_cartesian(xlim=xrng, ylim=yrng) +
  guides(colour=FALSE)+theme_bw()+
  theme(panel.background = element_rect(fill="white"),
        legend.background = element_rect(fill="white"),
        legend.key = element_rect(fill = "white",color = "white"),
        plot.background = element_rect(fill = "white"),
        legend.position="none",
        axis.title.y = element_text(vjust = 0.1,margin=margin(0,10,0,0)),
        axis.title.x = element_text(vjust = 0.5),
        text = element_text(size = 20))+
  facet_wrap(~case)

quartz.save(type = 'pdf', file = 'Figs/simulation_BPT5.pdf',width = 9, height = 8)
#---------------------------------##---------------------------------#

diff05 <- d0_BPT  
diff05$z = (d0_BPT$z - d5_BPT$z)
diff06 <- d0_BPT  
diff06$z = (d0_BPT$z - d6_BPT$z)

rownames(diff05$z) = diff05$x
colnames(diff05$z) = diff05$y
rownames(diff06$z) = diff06$x
colnames(diff06$z) = diff06$y


# Now melt it to long format
diff05.m = melt(diff05$z, id.var=rownames(diff05))
names(diff05.m) = c("x","y","z")
diff06.m = melt(diff06$z, id.var=rownames(diff06))
names(diff06.m) = c("x","y","z")


diffcomb<-rbind(diff05.m,diff06.m)
diffcomb$case <- factor(rep(c("5 clusters","6 clusters"),each=1e4),levels=c("5 clusters", "6 clusters"))
# 
gdiff<-ggplot(diffcomb , aes(x, y, z=z)) +
  xlab(expression(paste('log [NII]/H', alpha))) +
  ylab(expression(paste('log [OIII]/H', beta))) +
  stat_contour(aes(fill =..level..,alpha=..level..), bins=5e3,geom="polygon")+
  scale_fill_gradient2(low="blue4", mid="white", high="darkred",midpoint = 0) +
  coord_cartesian(xlim=xrng, ylim=yrng) +
  scale_y_continuous(breaks = c(-1,0,1),
                     labels=c("-1","0","1"))+
  guides(colour=FALSE)+theme_bw()+
  theme(panel.background = element_rect(fill="white"),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        legend.background = element_rect(fill="white"),
        legend.key = element_rect(fill = "white",color = "white"),
        plot.background = element_rect(fill = "white"),
        legend.position="none",
        axis.title.y = element_text(vjust = 0.1,margin=margin(0,10,0,0)),
        axis.title.x = element_text(vjust = 0.5),
        text = element_text(size = 20))+
  facet_wrap(~case)
#---------------------------------##---------------------------------#



# Plot prediction vs observed

obs<-as.numeric(d0_BPT$z)
pred5<-as.numeric(d5_BPT$z)
pred6<-as.numeric(d6_BPT$z)

fit5<-lm(obs~pred5)
gfit5<-data.frame(x=obs,y=pred5)

fit6<-lm(obs~pred6)
gfit6<-data.frame(x=obs,y=pred6)

# Labels for R^2
lb5 = paste("R^2==",round(summary(fit5)$r.squared,4))
lb6 = paste("R^2==",round(summary(fit6)$r.squared,4))

gfitcomb<-rbind(gfit5,gfit6)
gfitcomb$case <- factor(rep(c("5 clusters","6 clusters"),each=1e4),
                        levels=c("5 clusters","6 clusters"))

gfit<-ggplot(gfitcomb,aes(x=x,y=y))+geom_point(color="gray80")+
  stat_smooth(formula=y ~ poly(x, 1),se = TRUE,method = "lm",color="green3")+
  theme_bw()+
  scale_y_continuous(breaks = c(-0.01,0,1.5,3,4.5,6),
                     labels=c("",0,1.5,3,4.5,6))+
  scale_x_continuous(breaks = c(0,1.5,3,4.5,6))+
  theme(legend.background = element_rect(fill="white"),
        legend.key = element_rect(fill = "white",color = "white"),
        plot.background = element_rect(fill = "white"),
        legend.position="top",
        axis.title.y = element_text(vjust = 0.1,margin=margin(0,10,0,0)),
        axis.title.x = element_text(vjust = 0.5),
        text = element_text(size = 20))+xlab("Observed")+
  ylab("Predicted")+
  annotate("text",
           label = c(lb5,lb6), size = 5, x = 1.25, y = 5.5,parse=TRUE)+
  facet_wrap(~case)


grid.arrange(gsim, gfit, ncol = 1,nrow=2)
quartz.save(type = 'pdf', file = 'Figs/diag_BPT_56.pdf',width = 9, height = 7)
#

#sum(residuals(fit4, type = "pearson")^2)





# Residual Analysis WHAN

xrng_w = range(AGN_short$xx_BPT)
yrng_w = range(AGN_short$yy_WHAN)



d0_WHAN = kde2d(AGN_short$xx_BPT, AGN_short$yy_WHAN, lims=c(xrng_w, yrng_w), n=100,
                h = rep(0.05, 2))
d5_WHAN = kde2d(sim5[,2],
                sim5[,4], lims=c(xrng_w, yrng_w), n=100,
                h = rep(0.05, 2))

d6_WHAN = kde2d(sim6[,2],
                sim6[,4], lims=c(xrng_w, yrng_w), n=100,
                h = rep(0.05, 2))

#---------------------------------##---------------------------------#
# Plot smooth representation for original data and each cluster
rownames(d0_WHAN$z) = d0_WHAN$x
colnames(d0_WHAN$z) = d0_WHAN$y

rownames(d5_WHAN$z) = d5_WHAN$x
colnames(d5_WHAN$z) = d5_WHAN$y


rownames(d6_WHAN$z) = d6_WHAN$x
colnames(d6_WHAN$z) = d6_WHAN$y

# Now melt it to long format
d0_WHAN.m = melt(d0_WHAN$z, id.var=rownames(d0_WHAN))
names(d0_WHAN.m) = c("x","y","z")

d5_WHAN.m = melt(d5_WHAN$z, id.var=rownames(d5_WHAN))
names(d5_WHAN.m) = c("x","y","z")


d6_WHAN.m = melt(d6_WHAN$z, id.var=rownames(d6_WHAN))
names(d6_WHAN.m) = c("x","y","z")



gcomb_WHAN<-rbind(d5_WHAN.m,d6_WHAN.m)
gcomb_WHAN$case <- factor(rep(c("5 clusters","6 clusters"),each=1e4),levels=c("5 clusters", "6 clusters"))
#colors <- colorRampPalette(c('white','blue','yellow','red','darkred'))(20)
# Plot difference 
gsimw<-ggplot(gcomb_WHAN, aes(x, y, z=z, fill=z)) +
  xlab(expression(paste('log [NII]/H', alpha))) +
  ylab(expression(paste('log EW(H', alpha, ')'))) +
  stat_contour(aes(fill =..level..,alpha=..level..), bins=5e2,geom="polygon") +
  scale_fill_gradientn(colours=colors) +
  coord_cartesian(xlim=xrng_w, ylim=yrng_w) +
  guides(colour=FALSE)+theme_bw()+
  theme(panel.background = element_rect(fill="white"),
        legend.background = element_rect(fill="white"),
        legend.key = element_rect(fill = "white",color = "white"),
        plot.background = element_rect(fill = "white"),
        legend.position="none",
        axis.title.y = element_text(vjust = 0.1,margin=margin(0,10,0,0)),
        axis.title.x = element_text(vjust = 0.5),
        text = element_text(size = 20))+
  facet_wrap(~case)

#---------------------------------##---------------------------------#


# Plot prediction vs observed

obs_WHAN<-as.numeric(d0_WHAN$z)
pred5_WHAN<-as.numeric(d5_WHAN$z)
pred6_WHAN<-as.numeric(d6_WHAN$z)

fit5_WHAN<-lm(obs_WHAN~pred5_WHAN)
fit6_WHAN<-lm(obs_WHAN~pred6_WHAN)

gfit5_WHAN<-data.frame(x=obs_WHAN,y=pred5_WHAN)
gfit6_WHAN<-data.frame(x=obs_WHAN,y=pred6_WHAN)

gfitcombw<-rbind(gfit5_WHAN,gfit6_WHAN)
gfitcombw$case <- factor(rep(c("5 clusters","6 clusters"),each=1e4),
                        levels=c("5 clusters","6 clusters"))


# Labels for R^2

wb5 = paste("R^2==",round(summary(fit5_WHAN)$r.squared,3))
wb6 = paste("R^2==",round(summary(fit6_WHAN)$r.squared,3))

gfit_w<-ggplot(gfitcombw,aes(x=x,y=y))+geom_point(color="gray80")+
  stat_smooth(formula=y ~ poly(x, 1),se = TRUE,method = "lm",color="green3")+
  theme_bw()+
  scale_y_continuous(breaks = c(-0.01,0,1.5,3,4.5,6),
                     labels=c("",0,1.5,3,4.5,6))+
  scale_x_continuous(breaks = c(0,1.5,3,4.5,6))+
  theme(legend.background = element_rect(fill="white"),
        legend.key = element_rect(fill = "white",color = "white"),
        plot.background = element_rect(fill = "white"),
        legend.position="top",
        axis.title.y = element_text(vjust = 0.1,margin=margin(0,10,0,0)),
        axis.title.x = element_text(vjust = 0.5),
        text = element_text(size = 20))+xlab("Observed")+
  ylab("Predicted")+
  annotate("text",
           label = c(wb5,wb6), size = 5, x = 1.25, y = 4.75,parse=TRUE)+
  facet_wrap(~case)


grid.arrange(gsimw, gfit_w, ncol = 1,nrow=2)
quartz.save(type = 'pdf', file = 'Figs/diag_WHAN_56.pdf',width = 9, height = 7)















