import json
import glob
from rdflib import Namespace, Graph, Literal, RDF, RDFS #, URIRef, BNode
from rdflib.namespace import NamespaceManager, DC #, FOAF
from resolver import get_URI_for_AILLA

def add_tier_set(questtype, dictionary):
    """
    read a json file with tier information into an rdf graph
    questtype is the type of annotation (tier, word, gloss, etc) TODO still have to be defined in an ontology
    """

    limit = 9999999
    for filename in list(dictionary.keys())[:limit]:
        #get basename
        basename = filename.split('/')[-1].strip()
        #uri = getURI(basename, archive)
        file_id = basename.replace(' ', '_')
        #use hashed filename as internal reference for brevity
        filehash = 'x'+hex(hash("%s"%filename.split('/')[-1]))
        #the dictionaries have a hierarchy tiertype>tierID>tiercontent
        #tiertype is eg "transcription", tier ID is "transcription@alfred"
        #the dictionaries groups tiers by tiertype, but the IDs themselves would
        #already be unique
        for tiertype in dictionary[filename]:
            tier_ids = dictionary[filename][tiertype]
            for tier_id in tier_ids:
                tier = dictionary[filename][tiertype][tier_id]
                #sanitize tier names
                output_tier_id = "%s_%s" %(filehash, tier_id.replace(" ", '').replace("\\", '').replace("<", '').replace(">", '')) #needsbetter sanitize
                #define default namespaces and resolveID
                archive_namespace = 'paradisec'
                resolve_id = file_id
                #modify defaults as applicable
                if filename.startswith('elareafs'):
                    archive_namespace = 'elarfiles' #we hackishly infer the archive from the filename TODO
                    resolve_id = file_id.replace('-b-', '/') #better use landing page instead of file location
                if filename.startswith('aillaeafs'):
                    archive_namespace = 'ailla' #we hackishly infer the archive from the filename TODO
                    resolve_id = get_URI_for_AILLA(basename)
                #add information about tier
                GRAPH.add((QUESTRESOLVER[output_tier_id],
                           RDF.type,
                           QUEST.Tier))
                GRAPH.add((QUESTRESOLVER[output_tier_id],
                           DBPEDIA.isPartOf,
                           ARCHIVE_NAMESPACES[archive_namespace][resolve_id]))
                
                GRAPH.add((ARCHIVE_NAMESPACES[archive_namespace][resolve_id],
                           RDFS.label,
                           Literal(basename)))
                #add information about components of tier
                for j, annotation in enumerate(tier): #annotations are utterance length in this context
                    annotation_id = "%s_%s"%(output_tier_id, j)
                    GRAPH.add((QUESTRESOLVER[annotation_id],
                               RDF.type,
                               questtype))
                    GRAPH.add((QUESTRESOLVER[annotation_id],
                               RDFS.label,
                               Literal('%s'%annotation.strip())))
                    GRAPH.add((QUESTRESOLVER[annotation_id],
                               DBPEDIA.isPartOf,
                               QUESTRESOLVER[output_tier_id]))


#define general namespaces
QUEST = Namespace("http://zasquest.org/")
QUESTRESOLVER = Namespace("http://zasquest.org/resolver/")
DBPEDIA = Namespace("http://dbpedia.org/ontology/")

#define archive namespaces
NAMESPACE_MANAGER = NamespaceManager(Graph())
NAMESPACE_MANAGER.bind('dbpedia', DBPEDIA)
NAMESPACE_MANAGER.bind('quest', QUEST) #for ontology
NAMESPACE_MANAGER.bind('QUESTRESOLVER', QUESTRESOLVER) #for the bridge for rewritable URLs
NAMESPACE_MANAGER.bind("rdfs", RDFS)
NAMESPACE_MANAGER.bind("dc", DC)

ARCHIVE_NAMESPACES = {
    'paradisec': Namespace("https://cataloGRAPH.paradisec.orGRAPH.au/collections/"),
    'elarcorpus': Namespace("https://lat1.lis.soas.ac.uk/corpora/ELAR/"),
    'elarfiles': Namespace("https://elar.soas.ac.uk/resources/"),
    'ailla': Namespace("http://ailla.utexas.org/islandora/object/")
    }

for archive in ARCHIVE_NAMESPACES:
    NAMESPACE_MANAGER.bind(archive, ARCHIVE_NAMESPACES[archive])


if __name__ == "__main__":
    GRAPH = Graph(namespace_manager=NAMESPACE_MANAGER)
    #for f in glob.glob('translations*.json'):
    for f in glob.glob('translations-ai*.json'):
        print("preparing translations for %s"%f)
        TRANSLATION_DICTIONARY = json.loads(open(f).read())
        add_tier_set(QUEST.Translation, TRANSLATION_DICTIONARY)

    #for f in glob.glob('*-transcriptions.json'):
        #print("preparing transcriptions for %s"%f)
        #TRANSCRIPTION_DICTIONARY = json.loads(open(f).read())
        #add_tier_set(QUEST.Transcription, TRANSCRIPTION_DICTIONARY)

    print("writing output")
    with open("eld.n3", "wb") as rdfout:
        rdfout.write(GRAPH.serialize(format='n3'))

    #glosses
    #LGR
    #topic with NERD
