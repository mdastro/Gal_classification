fancy_scientific <- function(l) {
  
  # turn in to character string in scientific notation

  l <- format(l, scientific = TRUE)
  # quote the part before the exponent to keep all the digits
  l <- gsub("^(.*)e", "'\\1'e", l)
  # turn the 'e+' into plotmath format
  l <- gsub("e", "%*%10^", l)
  # return this as an expression
  parse(text=l)

}
# Function to perform cluster comparison
ExClVal <- function(class = class, clust = clust, data = data){
require(LaplacesDemon)
require(scales)
require(MASS)
require(ggplot2)
class  <- as.factor(class)

# Find number of clusters and classes
Nclass <- length(levels(class))
Ncluster <- clust$G

cluster_sep <- list()
# Separate individual clusters 
for(i in 1:Ncluster){
cluster_sep[[i]] = as.data.frame(data[(clust$classification ==i),])
cluster_sep[[i]] = cbind(cluster_sep[[i]],label=rep(LETTERS[i],nrow(cluster_sep[[i]])),
                         deparse.level = 2)
}

class_sep <- list()
# Separate individual clusters 
for(i in 1:Nclass){
  class_sep[[i]] = as.data.frame(data[(class == levels(class)[i]),])
  class_sep[[i]] = cbind(class_sep[[i]],label=class[class == levels(class)[i]])
  
}


#Perform LDA on data containing both cluster and class for each combination

# Loop over clusters and classes
data <- matrix(list(),nrow=Ncluster,ncol=Nclass)
ldaResult <- matrix(list(),nrow=Ncluster,ncol=Nclass)
prediction <- matrix(list(),nrow=Ncluster,ncol=Nclass)
clusterProjected <- matrix(list(),nrow=Ncluster,ncol=Nclass)
classProjected <- matrix(list(),nrow=Ncluster,ncol=Nclass)
minRange <- matrix(list(),nrow=Ncluster,ncol=Nclass)
maxRange <- matrix(list(),nrow=Ncluster,ncol=Nclass)
pdfCluster <- matrix(list(),nrow=Ncluster,ncol=Nclass)
pdfClass <- matrix(list(),nrow=Ncluster,ncol=Nclass)
KL <- matrix(list(),nrow=Ncluster,ncol=Nclass)
gg <- matrix(list(),nrow=Ncluster,ncol=Nclass)
clcolor <- c("#FF1493","#7FFF00", "#00BFFF", "#FF8C00")
for (i in 1:Ncluster){
for (j in 1:Nclass){  
 data[[i,j]] = rbind(cluster_sep[[i]], class_sep[[j]])
 data[[i,j]]$label <- droplevels(data[[i,j]]$label)
  ldaResult[[i,j]] = lda(label ~ ., data[[i,j]])
  prediction[[i,j]] =  predict(ldaResult[[i,j]])
#Getting projected matrices for cluster and class from predicted values
clusterProjected[[i,j]] = prediction[[i,j]]$x[1:nrow(cluster_sep[[i]]),]
classProjected[[i,j]] = prediction[[i,j]]$x[(nrow(cluster_sep[[i]])+1):(dim(data[[i,j]])[1]),]  
#Get probability density for each cluster and class

#Extending the range so that both densities are within minimum 
#and maximum of obtained density values
minRange[[i,j]] = min(clusterProjected[[i,j]], classProjected[[i,j]])
maxRange[[i,j]] = max(clusterProjected[[i,j]], classProjected[[i,j]])

pdfCluster[[i,j]] = density(clusterProjected[[i,j]], from = minRange[[i,j]]-0.1, to=maxRange[[i,j]]+0.1,n=1024)
pdfClass[[i,j]] = density(classProjected[[i,j]], from = minRange[[i,j]]-0.1, to=maxRange[[i,j]]+0.1,n=1024) 
#pdfCluster[[i,j]] = density(clusterProjected[[i,j]])
#pdfClass[[i,j]] = density(classProjected[[i,j]]) 

#Get probability density from the densities
pdfCluster[[i,j]]$y = pdfCluster[[i,j]]$y/sum(pdfCluster[[i,j]]$y)
pdfClass[[i,j]]$y = pdfClass[[i,j]]$y/sum(pdfClass[[i,j]]$y)
# Calcualte K-L distance using package Laplace Demon


KL[[i,j]] <- KLD(pdfCluster[[i,j]]$y,pdfClass[[i,j]]$y,base=2)$mean.sum.KLD

# Plot density of cluster vs classes

gg[[i,j]] <- ggplot(
data=data.frame(x=pdfCluster[[i,j]]$x,y=pdfCluster[[i,j]]$y),aes(x=x,y=y))+
  geom_polygon(data=data.frame(x=pdfClass[[i,j]]$x,y=pdfClass[[i,j]]$y),aes(x=x,y=y),
            fill="gray80",size=1.25,alpha=0.7)+
  geom_polygon(linetype="dashed",fill = clcolor[i],alpha=0.4)+
  theme_bw()+
   scale_y_continuous(labels=fancy_scientific,
                      breaks=pretty_breaks())+
 theme(legend.position = "none",plot.title = element_text(hjust=0.5),
        axis.title.y=element_text(vjust=0.75),
        axis.title.x=element_text(vjust=-0.25),
        text = element_text(size=15))+xlab("LD1")+ylab("Density")+
  ggtitle(paste("G",i,"/",levels(class)[j],sep="")) 
#+

#  annotate("text",  x=Inf, y = Inf, label = paste("Cluster ",i,sep=""), vjust=3, hjust=1.5,size=5,
#           color="red3")+
 # annotate("text",  x=Inf, y = Inf, label = levels(class)[j], vjust=5, hjust=1.5,size=5,
 #          color="blue3")

}
}
z <- matrix(unlist(KL),nrow=nrow(KL),ncol=ncol(KL))
rownames(z) <- c(seq(1:Ncluster))
colnames(z) <- c(levels(class))
return(list(KL=z,
            pdfCluster = pdfCluster,
            pdfClass = pdfClass,
            gg=gg))
}



  
