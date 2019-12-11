import json
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import DC, FOAF 
from rdflib.namespace import Namespace, NamespaceManager

quest = Namespace("http://zasquest.org/")
questresolver = Namespace("http://zasquest.org/resolver/")
paradisec = Namespace("https://catalog.paradisec.org.au/collections/")
elar = Namespace("https://lat1.lis.soas.ac.uk/corpora/ELAR/")
elareafs = Namespace("https://elar.soas.ac.uk/resources/")
dbpedia = Namespace("http://dbpedia.org/ontology/")
namespace_manager = NamespaceManager(Graph())
namespace_manager.bind('paradisec', paradisec)
namespace_manager.bind('quest', quest)
namespace_manager.bind('questresolver', questresolver)
namespace_manager.bind('dbpedia', dbpedia)

archive_namespaces = {
    'paradisec': paradisec,
    'elar': elar,
    'elareafs': elareafs
    }

g = Graph(namespace_manager = namespace_manager) 
g.bind("rdfs", RDFS)
g.bind("dc", DC)

transcription_dictionary = json.loads(open('transcriptions.json').read())
translation_dictionary = json.loads(open('translations.json').read())
 
LIMIT = 9999999 
for filename in list(translation_dictionary.keys())[:LIMIT]: 
    fileID = filename.split('/')[-1]
    filehash = 'x'+hex(hash("%s"%filename.split('/')[-1]))
    for tiertype in translation_dictionary[filename]: 
        tierIDs = translation_dictionary[filename][tiertype] 
        for tierID in tierIDs:
            tier = translation_dictionary[filename][tiertype][tierID]
            output_tierID = "%s_%s" %(filehash, tierID.replace(" ",''))
            g.add((questresolver[output_tierID], RDF.type, quest.Tier)) 
            archive_namespace = 'paradisec'
            resolveID = fileID
            if filename.startswith('elareafs'):
                archive_namespace = 'elareafs' #we hackishly infer the archive from the filename TODO 
                resolveID = fileID.replace('-b-','/') #better use landing page instead of file location
            g.add((questresolver[output_tierID], dbpedia.isPartOf, archive_namespaces[archive_namespace][resolveID]))   
            for j, annotation in enumerate(tier):
                rdfID = "%s_%s"%(output_tierID,j) 
                g.add( ( questresolver[rdfID], RDF.type, quest.Annotation))
                g.add( ( questresolver[rdfID], dbpedia.isPartOf, questresolver[output_tierID]))                
                g.add( ( questresolver[rdfID], RDFS.label, Literal('%s'%annotation.strip())))
                
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
