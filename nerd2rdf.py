import json
import glob
import sys
from rdflib import Namespace, Graph, Literal, RDF, RDFS #, URIRef, BNode
from rdflib.namespace import NamespaceManager, DC #, FOAF


#{
    #"anlaeafs/18106-01f1SylviaJackson.eaf": {
        #"Q108266": "Navajos",
        #"Q2934": "goat",
        #"Q780": "chicken",
        #"Q89": "apple",
        #"Q96": "Mexican"
    #},
    #"anlaeafs/18106-02f1WarlanceChee.eaf": {
        #"Q108266": "Navajo",
        #"Q13310": "Navajo language",
        #"Q266750": "medicine man",
        #"Q2934": "goat",
        #"Q65358": "Gallup",
        #"Q96": "Mexican"
    #},
    
    

#define general namespaces
QUEST = Namespace("http://zasquest.org/")
QUESTRESOLVER = Namespace("http://zasquest.org/resolver/") 
WIKIDATA = Namespace("https://www.wikidata.org/wiki/")

#define archive namespaces
NAMESPACE_MANAGER = NamespaceManager(Graph())
NAMESPACE_MANAGER.bind('wikidata', WIKIDATA)
NAMESPACE_MANAGER.bind('quest', QUEST) #for ontology
NAMESPACE_MANAGER.bind('QUESTRESOLVER', QUESTRESOLVER) #for the bridge for rewritable URLs
NAMESPACE_MANAGER.bind("rdfs", RDFS)
NAMESPACE_MANAGER.bind("dc", DC)

ARCHIVE_NAMESPACES = {
    'paradisec': Namespace("https://cataloGRAPH.paradisec.orGRAPH.au/collections/"),
    'elarcorpus': Namespace("https://lat1.lis.soas.ac.uk/corpora/ELAR/"),
    'elarfiles': Namespace("https://elar.soas.ac.uk/resources/")
    }

for archive in ARCHIVE_NAMESPACES:
    NAMESPACE_MANAGER.bind(archive, ARCHIVE_NAMESPACES[archive])


if __name__ == "__main__":
    GRAPH = Graph(namespace_manager=NAMESPACE_MANAGER)
    filename = sys.argv[1]
    with open(filename) as jsoninfile:
        nerdjson = json.loads(jsoninfile.read())
        
    for eaffile in nerdjson:
        for wikidataID in nerdjson[eaffile]:
            GRAPH.add((QUESTRESOLVER[eaffile],
                        DC.topic,
                        WIKIDATA[wikidataID]))
   
    print("writing output")
    with open(filename.replace('json','n3'), "wb") as rdfout:
        rdfout.write(GRAPH.serialize(format='n3'))
