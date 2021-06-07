def coreNode(g,alfa,weight):
    
    
    def localCloseNeighborThreshold(g,p,weight):     
        geomin = 1   
        for q in g.neighbors(p): geomin *= g.edges[(p,q)][weight]
        return geomin ** (1 / len(list(g.neighbors(p))))
    
    def localCloseNeighbors(g,p,tresholds,weight):
        return [ q for q in g.neighbors(p) if g.edges[(p,q)][weight] <= tresholds[p] and g.edges[(p,q)][weight] <= tresholds[q] ]
    
        
    
    localCloseNeighborThresholds = {p:localCloseNeighborThreshold(g,p,weight) for p in g.nodes()}
    
    corenodes = list()
    for node in g.nodes:
        
        localMinimumClusteringThreshold = alfa * len(list(g.neighbors(node)))
        treshold = localCloseNeighborThresholds[node]
        
        if len(localCloseNeighbors(g,node,localCloseNeighborThresholds,weight)) >= localMinimumClusteringThreshold: 
            
            corenodes.append(node)
        
    return corenodes