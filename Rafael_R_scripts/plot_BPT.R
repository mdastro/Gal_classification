plot_BPT<-function(CLUST,size=5000){
  #--Get Ellipse info----------------------------------------------------------------#
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
  
  #El_WHAN<-subset(EL,xvar=="yy_WHAN" & yvar=="xx_BPT")
  #El_WHAN$classification <-as.factor(El_WHAN$classification)
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

# subset data for plot
index <- sample(seq_len(nrow(gdata)),replace = F, size = size)    
  # BPT projection
  gg<-ggplot(data=gdata,aes(x=x,y=y))+
    xlab(expression(paste('log [NII]/H', alpha))) +
    ylab(expression(paste('log [OIII]/H', beta))) +
    #  stat_ellipse(type="norm",geom = "polygon", alpha = 1/2,aes(group=type,fill=type),level = 0.997)+
#      geom_point(data=gdata[index,],aes(x=x,y=y),color="#11111130",size=1.2)+
    scale_colour_manual(values=c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00","brown","#8E9CA3"))+ 
    scale_fill_manual(values=c("#FF1493", "#7FFF00","#00BFFF", "#FF8C00","brown","#8E9CA3"))+
#    scale_linetype_stata()+
    # geom_path(data=El_BPT99,aes(x=xval,y=yval,group=classification,color=classification
    #                                 ),size=1)+
    geom_polygon(data=El_BPT95,aes(x=xval,y=yval,group=classification,
                                   color=classification,fill=classification),
                 size=1.1,alpha=0.25)+
    
    geom_polygon(data=El_BPT68,aes(x=xval,y=yval,group=classification,color=classification,
                                   fill=classification
    ),size=1.1,alpha=0.35)+
    theme_bw() + 
    geom_line(aes(x=xx,y=Ka),data=gKa,size=1.25,linetype="dashed",color="gray25")+
    geom_line(aes(x=xx1,y=Ke),data=gKe,size=1.25,linetype="dotted",color="gray25")+
    geom_line(aes(x=xx2,y=Sey),data=gSey,size=0.75,linetype="dotdash",color="gray25")+
    
    coord_cartesian(xlim=c(-1.7,1.3),ylim=c(-1.4,1.5))+
    theme(legend.position = "none",plot.title = element_text(hjust=0.5),
          axis.title.y=element_text(vjust=0.75),
          axis.title.x=element_text(vjust=-0.25),
          text = element_text(size=20))
  return(gg)
}