#from fastcoref import FCoref
from fastcoref import LingMessCoref
from fastcoref import spacy_component
import spacy
import itertools

#model = FCoref(device='cuda:0')
#model = FCoref()

#model = LingMessCoref(device='cuda:0')
model = LingMessCoref()

# initialize language model
nlp = spacy.load("en_core_web_md")
# add coref pipeline
#nlp.add_pipe("fastcoref")
# add pipeline (declared through entry_points in setup.py)
nlp.add_pipe("entityLinker", last=True)

def get_corefs(input_text):
    text = input_text.replace("\t","").replace("\n","")
    preds = model.predict(texts=[text])

    if (len(preds) == 0):
        return text.split(".")

    cluster_num = preds[0].get_clusters(as_strings=False)
    # print("Num Clusters:", len(cluster_num))
    # print("Initial Clusters:",cluster_num)

    # clean clusters
    cluster_spans = {}
    for cluster in cluster_num:
        for (i,j) in cluster:
            size = j-i
            for x in range(i,j):
                if (x in cluster_spans):
                    if (size > (cluster_spans[x][1]-cluster_spans[x][0])):
                        cluster_spans[x] = (i,j)
                else:
                    cluster_spans[x] = (i,j)


    clusters = []
    for cluster in cluster_num:
        cluster_tokens = []
        for (i,j) in cluster:
            if (i in cluster_spans) and (cluster_spans[i] == (i,j)):
                cluster_tokens.append((i,j))
        if (len(cluster_tokens)>0):
            clusters.append(cluster_tokens)
    #print("Cluster Spans:", clusters)

    labels = preds[0].get_clusters()
    print("Cluster Tokens:",labels)

    return (clusters,labels)

def get_tokens(text):
    doc = nlp(text)

    entities = {}
    for e in doc._.linkedEntities:
        span = e.get_span()
        entity = {
            'id'    : e.get_id(),    
            'label' : e.get_label(),
            'level' : len(e.get_sub_entities())
        }
        entities[span.start] = entity
    #print("Entities:",entities)

    tokens = {}
    for id, t in enumerate(doc):
        token = {
            'text' : t.text,
            'text_with_ws' : t.text_with_ws,
            'pos'  : t.pos_,
            'tag'  : t.tag_,
            'sentence': t.sent,
            'level' : 99999
        }
        if (id in entities):
            entity = entities[id]
            token['level'] = entity['level']        
            token['label'] = entity['label']
        tokens[t.idx] = token
    #print("Tokens:",tokens)

    return tokens
