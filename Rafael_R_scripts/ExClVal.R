#read the data in and eliminate the class variable for the clustering process
dataSet = iris 
dataSet$Species = as.factor(dataSet$Species)
dataForClustering = dataSet[,-5]

#Perform EM clustering through EMCluster algorithm package
set.seed(100)
emobj = simple.init(dataForClustering, nclass=3)
clusterResult = emcluster(dataForClustering, emobj, assign.class=TRUE)

# Plotting the clustering results
plotem(clusterResult, dataForClustering)

#separate individual clusters from clustering result
cluster1 = dataForClustering[(clusterResult$class==1),]
cluster2 = dataForClustering[(clusterResult$class==2),]
cluster3 = dataForClustering[(clusterResult$class==3),]


#separate individual classes from original classification
class1 = dataSet[(dataSet$Species  == "setosa"),-5]
class2 = dataSet[(dataSet$Species  == "versicolor"),-5]
class3 = dataSet[(dataSet$Species  == "virginica"),-5]


clust<-Mclust(iris[,1:4],G=6)
class<-iris$Species

# Function to performe cluster comparison
ExClVal <- function(class = class, clust = clust){
class  <- as.factor(class)

# Find number of clusters and classes
Nclass <- length(levels(class))
Ncluster <- clust$G

cluster_sep <- list()
# Separate individual clusters 
for(i in 1:Ncluster){
cluster_sep[[i]] = as.data.frame(clust$data[(clust$classification ==i),])
cluster_sep[[i]] = cbind(cluster_sep[[i]],label=rep(LETTERS[i],nrow(cluster_sep[[i]])),
                         deparse.level = 2)
}

class_sep <- list()
# Separate individual clusters 
for(i in 1:Nclass){
  class_sep[[i]] = as.data.frame(clust$data[(class == levels(class)[i]),])
  class_sep[[i]] = cbind(class_sep[[i]],label=class[class == levels(class)[i]])
  
}


#Perform LDA on data containing both cluster and class for each combination

# Loop over clusters and classes
data <- matrix(list(),nrow=Ncluster,ncol=Nclass)
ldaResult <- matrix(list(),nrow=Ncluster,ncol=Nclass)
prediction <- matrix(list(),nrow=Ncluster,ncol=Nclass)
clusterProjected <- matrix(list(),nrow=Ncluster,ncol=Nclass)
classProjected <- matrix(list(),nrow=Ncluster,ncol=Nclass)
for (i in 1:Ncluster){
for (j in 1:Nclass){  
 data[[i,j]] = rbind(cluster_sep[[i]], class_sep[[j]])
 data[[i,j]]$label <- droplevels(data[[i,j]]$label)
  ldaResult[[i,j]] = lda(label ~ ., data[[i,j]])
  prediction[[i,j]] =  predict(ldaResult[[i,j]])
#Getting projected matrices for cluster and class from predicted values
clusterProjected[[i,j]] = prediction[[i,j]]$x[1:nrow(cluster_sep[[i]]),]
classProjected[[i,j]] = prediction[[i,j]]$x[(nrow(cluster_sep[[i]])+1):(dim(data[[i,j]])[1]),]  
}
}






  

#Extending the range so that both densities are within minimum 
#and maximum of obtained density values
  minRange = min(clusterProjected, classProjected)
  maxRange = max(clusterProjected, classProjected)
  
 pdfCluster = density(clusterProjected, from= minRange-1, to=maxRange+1)
 pdfClass = density(classProjected, from= minRange-1, to=maxRange+1) 
  
  #Get probability density from the densities
  pdfCluster$y = pdfCluster$y/sum(pdfCluster$y)
  pdfClass$y = pdfClass$y/sum(pdfClass$y)
  
  #Plot the probability densities of cluster and class
  plot(range(pdfCluster$x, pdfClass$x), range(pdfCluster$y, pdfClass$y), 
       type="n", xlab="X values for both distributions", ylab="Probability Density",
       main="Probability density plots")
  lines(pdfClass, col="blue")
  lines(pdfCluster, col="red")
  legend("topleft", legend=c("Cluster", "Class"), col=c("red", "blue"), 
         lty=c(1,1))
  
  #Create a vector for kl-distance calculation
  klD.Cluster.Class = rep(Inf, length(pdfCluster$y))
  
  #Calculate kl-distance for both distributions
  for (i in 1:length(pdfCluster$y)) {
    if(pdfClass$y[i] != 0 && pdfCluster$y[i] != 0){
      klD.Cluster.Class[i] <- pdfCluster$y[i] * (log(pdfCluster$y[i]) - 
                                                   log(pdfClass$y[i]))
    }
  }
  
  #Obtain overall KL-distance as sum of values in kl-distance vector
  klDistance = sum(klD.Cluster.Class[klD.Cluster.Class != Inf])
  
  if (klDistance == 0)
    klDistance = Inf
  
  #Output Kullback-Leibler distance between cluster and class
  klDistance
  
  
  
  
  
  
}