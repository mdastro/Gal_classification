plot_WHAN<-function(CLUST,size=5000){
  #--Get Ellipse info----------------------------------------------------------------#  
  EL68<-df.ellipses(CLUST,level=0.68)
  EL95<-df.ellipses(CLUST,level=0.95)
  EL99<-df.ellipses(CLUST,level=0.997)
  
  El_WHAN68<-subset(EL68,xvar=="yy_WHAN" & yvar=="xx_BPT")
  El_WHAN68$classification <-as.factor(El_WHAN68$classification)
  #
  El_WHAN95<-subset(EL95,xvar=="yy_WHAN" & yvar=="xx_BPT")
  El_WHAN95$classification <-as.factor(El_WHAN95$classification)
  #
  El_WHAN99<-subset(EL99,xvar=="yy_WHAN" & yvar=="xx_BPT")
  El_WHAN99$classification <-as.factor(El_WHAN99$classification)
  #
gdata <- data.frame(x=AGN_short$xx_BPT,y=AGN_short$yy_BPT,z=AGN_short$yy_WHAN, type=as.factor(CLUST$classification),
                      uncertainty = CLUST$uncertainty )
# subset data for plot
index <- sample(seq_len(nrow(gdata)),replace = F, size = size)

gg<-ggplot(data=gdata,aes(x=x,y=z))+
  xlab(expression(paste('log [NII]/H', alpha))) +
  ylab(expression(paste('log EW(H', alpha, ')'))) +
  geom_point(data=gdata[index,],aes(x=x,y=z),color="#11111130",size=1.2)+
  scale_colour_manual(values=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00"))+ 
  scale_fill_manual(values=c("#FF1493", "#7FFF00","#00BFFF", "#FF8C00"))+
  geom_polygon(data=El_WHAN95,aes(x=xval,y=yval,group=classification,
                                 color=classification,fill=classification),
               size=1.1,alpha=0.25)+
  
  geom_polygon(data=El_WHAN68,aes(x=xval,y=yval,group=classification,color=classification,
                                 fill=classification
  ),size=1.1,alpha=0.1)+
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

return(gg)
}