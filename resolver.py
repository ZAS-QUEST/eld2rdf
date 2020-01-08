import json

AILLAMAPPER = dict([(line.strip().split()[::-1]) for line in open("aillaeaf.tsv").readlines()])
ANLAMAPPER = dict([(line.strip().split('/')[::-1][:2]) for line in open('anla-eaffiles').readlines()])

TLAMAPPER = {}
tlajson = json.loads(open('tla.json').read())
for k in tlajson:
    vs = tlajson[k]
    for v in vs:
        TLAMAPPER[v] = k.replace('/datastream/OBJ/download','').split('/')[-1]
         

#def get_URI(eaf, archive):
    #if archive == "AILLA": 
        #return get_URI_for_AILLA(eaf)
    
    
def get_URI_for_AILLA(eaf):
    return AILLAMAPPER[eaf].split('/')[-1]


def get_URI_for_ANLA(eaf):
    return ANLAMAPPER[eaf]



def get_URI_for_TLA(eaf):
    return TLAMAPPER[eaf]

 

#PARADISEC

#ELAR
