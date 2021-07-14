from cores import coreNode


def multicore(G,alfa=0.3,weight='weight',minsize = 4):
    
  
    #PREPARATION
    g = G.copy()
    core = coreNode(g,alfa,weight)
    communities = list()
    centrality = 1
    k = 0
    borders = set()
    
    for node in g.nodes():
        g.nodes[node]['visited'] = False
        g.nodes[node]['community'] = None
        if node in core: g.nodes[node]['core']=True 
        else : g.nodes[node]['core']=False


    #INITIALIZE COMMUNITIES
    for p in g.nodes():

        if g.nodes[p]['visited'] == True or g.nodes[p]['core'] == False: continue
        
        candidates = set(g.neighbors(p))
        
        communities.append([p])
        g.nodes[p]['community'] = k
        g.nodes[p]['centrality'] = centrality
        g.nodes[p]['visited'] = True
        
        while len(candidates) != 0:

            q = candidates.pop()
           
            if g.nodes[q]['visited'] == False:

                if g.nodes[q]['core'] == True :   
                    communities[k].append(q)
                    g.nodes[q]['community'] = k
                    g.nodes[q]['centrality'] = centrality
                    for x in g.neighbors(q):
                        if g.nodes[x]['visited'] == False : candidates.add(x)
                
                else: borders.add(q)
                g.nodes[q]['visited'] = True

        k = k + 1
        
    
    #PROPAGATION
  
    while len(borders) != 0:
        newborders = set() 
        for p in borders: 
            centrality = None
            votes = [0 for c in communities]
            for q in g.neighbors(p):
                if q not in borders:                        
                    if g.nodes[q]['community'] != None:
                        voteweight = g.nodes[q]['centrality'] + g.edges[(p,q)][weight]
                        if centrality == None or voteweight < centrality:
                            centrality = voteweight
                        votes[g.nodes[q]['community']] += 1 / voteweight
                    else: newborders.add(q)
            k = votes.index(max(votes))
            communities[k].append(p)
            g.nodes[p]['community'] = k
            g.nodes[p]['centrality'] = centrality
            
        borders = newborders
        centrality += 1
        

 
       #OUTLIERS 
    unmarked = list()
    for k,c  in enumerate(communities): 
        if len(c) <= minsize :
            
            for p in c: 
                g.nodes[p]['community'] = None
                
            communities[k] = []    
            unmarked.extend(c)
            
    borders = set()
    for p in unmarked:
        for q in g.neighbors(p):
            if g.nodes[q]['community'] != None:
                borders.add(p)
                break
                
    borders = set(borders)
    
    while len(borders) != 0:
        newborders = set() 
        for p in borders: 
            votes = [0 for c in communities]
            centrality = None
            for q in g.neighbors(p):
                if q not in borders:
                    if g.nodes[q]['community'] != None:
                        voteweight = g.nodes[q]['centrality'] + g.edges[(p,q)][weight]
                        if centrality == None or voteweight < centrality:
                            centrality = voteweight
                        votes[g.nodes[q]['community']] += 1 / voteweight
                    else: newborders.add(q)
            k = votes.index(max(votes))
            communities[k].append(p)
            g.nodes[p]['community'] = k
            g.nodes[p]['centrality'] = centrality
            
        borders = newborders
      
    communities = [c for c in communities if len(c) != 0 ]
    centralities = {node:g.nodes[node]['centrality'] for node in g.nodes}
    return NodeClustering(communities, g, "multicore", method_parameters={"centralities":centralities,"alfa":alfa,"weight":weight,"minsize":minsize, "voteweight":voteweight})