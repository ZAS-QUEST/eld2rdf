""" transform a json file mapping files to wikidata IDs to JSON"""

import json
import sys
import urllib.parse
from rdflib import Namespace, Graph, RDFS  # , URIRef, BNode
from rdflib.namespace import NamespaceManager, DC  # , FOAF
from resolver import get_URI_for_AILLA, get_URI_for_ANLA, get_URI_for_TLA, get_URI_for_Paradisec, get_URI_for_ELAR


# define general namespaces
#QUEST = Namespace("http://zasquest.org/")
#QUESTRESOLVER = Namespace("http://zasquest.org/resolver/")
WIKIDATA = Namespace("https://www.wikidata.org/wiki/")

# define archive namespaces
NAMESPACE_MANAGER = NamespaceManager(Graph())
NAMESPACE_MANAGER.bind("wikidata", WIKIDATA)
#NAMESPACE_MANAGER.bind("quest", QUEST)  # for ontology
#NAMESPACE_MANAGER.bind(
    #"QUESTRESOLVER", QUESTRESOLVER
#)  # for the bridge for rewritable URLs
NAMESPACE_MANAGER.bind("rdfs", RDFS)
NAMESPACE_MANAGER.bind("dc", DC)

ARCHIVE_NAMESPACES = { 
    'paradisec': Namespace("https://catalog.paradisec.org.au/collections/"),
    #'elarcorpus': Namespace("https://lat1.lis.soas.ac.uk/corpora/ELAR/"),
    'elarcorpus': Namespace("https://elar.soas.ac.uk/Record/"),   
    'elarfiles': Namespace("https://elar.soas.ac.uk/resources/"),
    'ailla': Namespace("http://ailla.utexas.org/islandora/object/"),
    'anla': Namespace("https://www.uaf.edu/anla/collections/search/resultDetail.xml?id="),
    'tla': Namespace("https://archive.mpi.nl/islandora/object/")
    }

for archive in ARCHIVE_NAMESPACES:
    NAMESPACE_MANAGER.bind(archive, ARCHIVE_NAMESPACES[archive])

for archive in ARCHIVE_NAMESPACES:
    NAMESPACE_MANAGER.bind(archive, ARCHIVE_NAMESPACES[archive])


if __name__ == "__main__":
    GRAPH = Graph(namespace_manager=NAMESPACE_MANAGER)
    FILENAME = sys.argv[1]
    if FILENAME.startswith('translations-elareafs'):
        archive_namespace = 'elarcorpus' #we hackishly infer the archive from the filename TODO
        resolver = get_URI_for_ELAR
    if FILENAME.startswith('translations-aillaeafs'):
        archive_namespace = 'ailla' #we hackishly infer the archive from the filename TODO
        resolver = get_URI_for_AILLA
    if FILENAME.startswith('translations-anlaeafs'):
        archive_namespace = 'anla' #we hackishly infer the archive from the filename TODO
        resolver = get_URI_for_ANLA
    if FILENAME.startswith('translations-tlaeafs'):
        archive_namespace = 'tla' #we hackishly infer the archive from the filename TODO
        resolver = get_URI_for_TLA
    if FILENAME.startswith('translations-paradiseceafs'):
        archive_namespace = 'paradisec' #we hackishly infer the archive from the filename TODO
        resolver = get_URI_for_Paradisec
                   
    
    with open(FILENAME) as jsoninfile:
        NERDJSON = json.loads(jsoninfile.read())

    for eaffile in NERDJSON:
        #print(eaffile)
        BASENAME = eaffile.split('/')[-1].strip()
        #print(BASENAME)
        for wikidataID in NERDJSON[eaffile]:
            GRAPH.add((ARCHIVE_NAMESPACES[archive_namespace][resolver(BASENAME)], DC.topic, WIKIDATA[wikidataID]))

    print("writing output")
    with open(FILENAME.replace("json", "n3"), "wb") as rdfout:
        rdfout.write(GRAPH.serialize(format="n3"))
