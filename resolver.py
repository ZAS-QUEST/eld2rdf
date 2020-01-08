AILLAMAPPER = dict([(line.strip().split()[::-1]) for line in open("aillaeaf.tsv").readlines()])
ANLAMAPPER = dict([(line.strip().split('/')[::-1][:2]) for line in open('anla-eaffiles').readlines()])

#def get_URI(eaf, archive):
    #if archive == "AILLA": 
        #return get_URI_for_AILLA(eaf)
    
    
def get_URI_for_AILLA(eaf):
    return AILLAMAPPER[eaf].split('/')[-1]


def get_URI_for_ANLA(eaf):
    return ANLAMAPPER[eaf]


