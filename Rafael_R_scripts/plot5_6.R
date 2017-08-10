set.seed(42)
CLUST5 <- Mclust(AGN_short,G = 5,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                 modelName = "VVV")#Initialization with 1000 for higher speed
set.seed(42)
CLUST6 <- Mclust(AGN_short,G = 6,initialization=list(subset=sample(1:nrow(AGN_short), size=1000)),
                 modelName = "VVV")#Initialization with 1000 for higher speed


B5 <- plot_BPT(CLUST5)
B6 <- plot_BPT(CLUST6)
W5 <- plot_WHAN(CLUST5)
W6 <- plot_WHAN(CLUST6)



grid.arrange(B5, B6,W5,W6, ncol = 2,nrow=2)
quartz.save(type = 'pdf', file = 'Figs/Clusters_56.pdf',width = 9, height = 7.5)


plot_word(word = "macaquinho", R = 20, phi = 0, copula = FALSE,
          portion = 0.2, shift = 1.2, orbit = 3000)