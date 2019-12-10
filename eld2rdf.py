import json
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import DC, FOAF

quest = Namespace("http://zasquest.org/")
paradisec = Namespace("http://paradisec.org/")

g = Graph()
g.bind("rdfs", RDFS)
g.bind("dc", DC)
g.bind("quest", quest)
g.bind("paradisec", paradisec)

transcription_dictionary = json.loads(open('transcriptions.json').read())
translation_dictionary = json.loads(open('translations.json').read())

triples = []
for filename in list(translation_dictionary.keys())[:3]: 
    for tierkey in translation_dictionary[filename]: 
        tierlist = translation_dictionary[filename][tierkey] 
        for i, tier in enumerate(tierlist):
            tierID = filename+tierkey+str(i)
            tierID = tierID.replace(" ",'')
            #g.add((paradisec[tierID], RDF.type, quest.Tier))
            #g.add((paradisec[tierID], RDFS.label, " ".join(tier)))
            for j, annotation in enumerate(tier):
                annotationID = Literal("http://paradisec.org/%s/%s/%s/%s"%(filename,tierkey,i,j)).replace(" ",'') #check for underscores in filenames TODO
                g.add( (URIRef(annotationID), RDF.type, quest.Annotation))
                g.add( (URIRef(annotationID), RDFS.label, Literal('"%s"'%annotation)))
                
#for s,p,o in g:
    #print(s,p,o)
    
    
print( g.serialize(format='n3') )

#print( g.serialize(format='n3') )
        
#part of
#labels as translations 
#glosses
#LGR
#topic
