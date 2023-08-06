from claimer import parser

def get_claims(text):
    
    tokens = parser.get_tokens(text)
    print("Num Tokens:",len(tokens))

    clusters = []
    cluster_names = []
    partial_content = []
    current_sentence = None
    for i in tokens:
        t = tokens[i]
        if (len(partial_content)>250):
            if (current_sentence != t['sentence']):
                partial_text = "".join(partial_content)
                (partial_clusters, partial_cluster_names) = parser.get_corefs(partial_text)
                clusters.extend(partial_clusters)
                cluster_names.extend(partial_cluster_names)
                current_sentence = t['sentence']
                partial_content = [t['text_with_ws']]
            else:
                partial_content.append(t['text_with_ws'])                
        else:
            partial_content.append(t['text_with_ws'])
            current_sentence = t['sentence']

    #(clusters, cluster_names) = parser.get_corefs(text)
    print(cluster_names)

    cluster_labels = {}
    for idx, cluster in enumerate(clusters):
        position = 0
        candidates = []
        for (i,j) in cluster:
            level = 99999
            label = cluster_names[idx][position]
            for x in range(i,j):
                if x in tokens:
                    tokens[x]['cluster']=idx
                    t = tokens[x]
                    if (t['level'] < level):
                        level = t['level']
            candidates.append((level,label))
        candidates.sort(key = lambda x:  x[0])
        cluster_labels[idx] = candidates[0][1]
    #print("Cluster Labels:",cluster_labels)        
            

    claims = []
    claim  = []
    is_valid = False
    current_cluster = -1
    for k in tokens:
        t = tokens[k]
        if ('label' in t):
            is_valid = True
        if (t['text'] == '.'):
            if (is_valid):
                claims.append("".join(claim)+".")
            claim = []
            current_cluster = -1
            is_valid = False
            continue
        if ('cluster' in t):
            if (current_cluster == t['cluster']):
                continue
            # pos': 'PRON', 'tag': 'PRP$'
            elif (t['pos'] == 'PRON') and (t['tag'] == 'PRP$'):
                continue
            current_cluster = t['cluster']
            claim.append(cluster_labels[current_cluster]+" ")
        else:
            claim.append(t['text_with_ws'])
            current_cluster = -1
    if (len(claim)>0) and (is_valid):        
        claims.append("".join(claim)+".")
    #print("Num claims:",len(claims))
    return claims
