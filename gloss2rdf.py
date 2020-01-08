"""extract Leipzig Glossing Rules from JSON file and write out as RDF"""

import pprint
import re
import json
import sys
from rdflib import Namespace, Graph, RDFS  # , URIRef, BNode
from rdflib.namespace import NamespaceManager, DCTERMS  # , FOAF
from collections import Counter

LGRLIST = set(
    [
        "1",
        "2",
        "3",
        "A",
        "ABL",
        "ABS",
        "ACC",
        "ADJ",
        "ADV",
        "AGR",
        "ALL",
        "ANTIP",
        "APPL",
        "ART",
        "AUX",
        "BEN",
        "CAUS",
        "CLF",
        "COM",
        "COMP",
        "COMPL",
        "COND",
        "COP",
        "CVB",
        "DAT",
        "DECL",
        "DEF",
        "DEM",
        "DET",
        "DIST",
        "DISTR",
        "DU",
        "DUR",
        "ERG",
        "EXCL",
        "F",
        "FOC",
        "FUT",
        "GEN",
        "IMP",
        "INCL",
        "IND",
        "INDF",
        "INF",
        "INS",
        "INTR",
        "IPFV",
        "IRR",
        "LOC",
        "M",
        "N",
        "NEG",
        "NMLZ",
        "NOM",
        "OBJ",
        "OBL",
        "P",
        "PASS",
        "PFV",
        "PL",
        "POSS",
        "PRED",
        "PRF",
        "PRS",
        "PROG",
        "PROH",
        "PROX",
        "PST",
        "PTCP",
        "PURP",
        "Q",
        "QUOT",
        "RECP",
        "REFL",
        "REL",
        "RES",
        "S",
        "SBJ",
        "SBJV",
        "SG",
        "TOP",
        "TR",
        "VOC",
    ]
)


# define general namespaces
QUEST = Namespace("http://zasquest.org/")
QUESTRESOLVER = Namespace("http://zasquest.org/resolver/")
LGR = Namespace("https://www.eva.mpg.de/lingua/resources/glossing-rules.php/")

# define archive namespaces
NAMESPACE_MANAGER = NamespaceManager(Graph())
NAMESPACE_MANAGER.bind("lgr", LGR)
NAMESPACE_MANAGER.bind("quest", QUEST)  # for ontology
NAMESPACE_MANAGER.bind(
    "QUESTRESOLVER", QUESTRESOLVER
)  # for the bridge for rewritable URLs
NAMESPACE_MANAGER.bind("rdfs", RDFS)
NAMESPACE_MANAGER.bind("dcterms", DCTERMS)

ARCHIVE_NAMESPACES = {
    "paradisec": Namespace("https://cataloGRAPH.paradisec.orGRAPH.au/collections/"),
    "elarcorpus": Namespace("https://lat1.lis.soas.ac.uk/corpora/ELAR/"),
    "elarfiles": Namespace("https://elar.soas.ac.uk/resources/"),
}

for archive in ARCHIVE_NAMESPACES:
    NAMESPACE_MANAGER.bind(archive, ARCHIVE_NAMESPACES[archive])


if __name__ == "__main__":
    personnumberdic = {
        "1SG": ["1","SG"],
        "2SG": ["2","SG"],
        "3SG": ["3","SG"],
        "1DU": ["1","DU"],
        "2DU": ["2","DU"],
        "3DU": ["3","DU"],
        "1PL": ["1","PL"],
        "2PL": ["2","PL"],
        "3PL": ["3","PL"]
        }
                            
    FILENAME = sys.argv[1]
    GRAPH = Graph(namespace_manager=NAMESPACE_MANAGER)
    
    #all_glosses = {}
    with open(FILENAME) as jsoninfile:
        GLOSSJSON = json.loads(jsoninfile.read())
    
    #store and tally all found glosses
    allcapsglosses = Counter()
    for eaffile in GLOSSJSON: 
        glosses = [supergloss 
                      for tiertype in GLOSSJSON[eaffile] 
                      for tier_ID in GLOSSJSON[eaffile][tiertype] 
                      for string in GLOSSJSON[eaffile][tiertype][tier_ID][1] # (words,glosses)
                      for supergloss in re.split("[-=:\. ]", string)
                      if re.search("^[^a-z]+$", supergloss) and re.search("[A-Z]", supergloss)]
        newglosses = Counter(glosses) 
        allcapsglosses += newglosses
        
        #split fused personnumber glosses
        for k in personnumberdic:
            if k in newglosses:
                occurrences = newglosses[k]
                number, person = personnumberdic[k]
                newglosses[person] += occurrences
                newglosses[number] += occurrences
                del newglosses[k]
                          
        found_LGR_glosses = set(newglosses.keys()) & LGRLIST  # set intersection
        for lgr_gloss in found_LGR_glosses:
            GRAPH.add((QUESTRESOLVER[eaffile], DCTERMS.references, LGR[lgr_gloss]))
    
    pprint.pprint(allcapsglosses)
    print("writing output")
    with open(FILENAME.replace("json", "n3"), "wb") as rdfout:
        rdfout.write(GRAPH.serialize(format="n3"))
