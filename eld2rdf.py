import json
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import DC, FOAF
from rdflib.namespace import Namespace, NamespaceManager

quest = Namespace("http://zasquest.org/")
paradisec = Namespace("http://paradisec.org/")
namespace_manager = NamespaceManager(Graph())
namespace_manager.bind('paradisec', paradisec)
namespace_manager.bind('quest', quest)

g = Graph(namespace_manager = namespace_manager) 
g.bind("rdfs", RDFS)
g.bind("dc", DC)

transcription_dictionary = json.loads(open('transcriptions.json').read())
translation_dictionary = json.loads(open('translations.json').read())
 
LIMIT = 9999999 
for filename in list(translation_dictionary.keys())[:LIMIT]: 
    for tiertype in translation_dictionary[filename]: 
        tierIDs = translation_dictionary[filename][tiertype] 
        for tierID in tierIDs:
            tier = translation_dictionary[filename][tiertype][tierID]
            output_tierID = tierID.replace(" ",'')
            #g.add((paradisec[tierID], RDF.type, quest.Tier))
            #g.add((paradisec[tierID], RDFS.label, " ".join(tier)))
            for j, annotation in enumerate(tier):
                rdfID = "x%s_%s_%s"%(filename.split('/')[-1][:11],output_tierID.replace('@','_'),j) 
                g.add( ( paradisec[rdfID], RDF.type, quest.Annotation))
                g.add( ( paradisec[rdfID], RDFS.label, Literal('%s'%annotation.strip())))
                
#for s,p,o in g:
    #print(s,p,o)
    
with open("eld.n3", "wb") as rdfout:
    rdfout.write(g.serialize(format='n3'))

#print( g.serialize(format='n3') )
        
#part of
#labels as translations 
#glosses
#LGR
#topic
