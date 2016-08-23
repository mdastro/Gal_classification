library(e1071);require(mclust);library(RColorBrewer)

AGN<- read.csv("/Users/rafael/Dropbox/artigos/Meusartigos/IAA-WGC/Github/AGN_unsupervised/script/clean_AGN_data.csv",header=T)
AGN_high <- data.frame(log(AGN$NII/AGN$H_alpha,10),
                   log(AGN$OIII/AGN$H_beta,10))
test_index <- sample(seq_len(nrow(AGN_high)),replace=F, size = 10000)
AGN_short <- AGN_high[test_index,]



CLUST <- Mclust(AGN_short,G = 1:4)
plot(CLUST)


x <-  AGN_short$log.AGN.NII.AGN.H_alpha..10.
y <-  AGN_short$log.AGN.EW_H_alpha..10.
z <-  AGN_short$log.AGN.OIII.AGN.H_beta..10.

require(car)
require(scatterplot3d)
scatter3d(x,y,z, groups = as.factor(CLUST$classification),
          surface = FALSE)


scatterplot3d(x,y,z,color = CLUST$classification)


AGN_new <- cbind(AGN_short,CLUST$classification)
colnames(AGN_new)<-c("x","y","class_type")




svm.model1 <- svm(class_type ~ y+x, data=WHAN_new, type='C-classification', kernel = 'linear')

plot(svm.model1,WHAN_new,col = brewer.pal(8, "Set3"))



svm.model2 <- svm(class_type ~ y+x, data=WHAN_new, type='C-classification', kernel = 'polynomial', degree=8, gamma=0.1, coef0=1)

plot(svm.model2,WHAN_new)

