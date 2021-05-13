import json 
with open('tuscany.json') as jf:
    data = json.load(jf)
    
keys  = list(data.keys())

with open(f"tuscanyJ.weighted.edgelist",'w+') as f:
    for i in keys:
        if int(i) % 1000 == 0: print(i, end= ' ')
        if len(data[str(i)])==0: continue
        else: reviewers_i = set([review['username'] for review in data[str(i)] ])


        for j in keys[int(i)+1:]:
            if len(data[str(j)])==0: continue

            reviewers_j = set([review['username'] for review in data[str(j)] ])
            common_reviewers = list(reviewers_i.intersection(reviewers_j))
            union_reviewers = list(reviewers_i.union(reviewers_j))
            
            w = (len(common_reviewers)*10000)/len(union_reviewers) #jeccard's similarity * 10000
            #if len(common_reviewers) >= 1 : 
                #print(len(common_reviewers), len(union_reviewers),w)
                
            if w > 0 : f.write(f'{str(i)} {str(j)} {str( int(w))}\n')