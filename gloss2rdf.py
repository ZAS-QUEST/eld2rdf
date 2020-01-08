"""extract Leipzig Glossing Rules from JSON file and write out as RDF"""

import re
import json
import sys
from rdflib import Namespace, Graph, RDFS  # , URIRef, BNode
from rdflib.namespace import NamespaceManager, DCTERMS  # , FOAF

LGRLIST = set([
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
   ] )


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
    GRAPH = Graph(namespace_manager=NAMESPACE_MANAGER)
    FILENAME = sys.argv[1]
    with open(FILENAME) as jsoninfile:
        GLOSSJSON = json.loads(jsoninfile.read())

    for eaffile in GLOSSJSON:
        store = {}
        for tiertype in GLOSSJSON[eaffile]:
            for tier_ID in GLOSSJSON[eaffile][tiertype]:
                words, glosses = GLOSSJSON[eaffile][tiertype][tier_ID]
                for gloss in set(glosses): 
                    subglosses = re.split("[-=.:]", gloss)
                    for subgloss in subglosses:  
                        if subgloss == "1SG":
                            store["1"] = True
                            store["SG"] = True
                        elif subgloss == "2SG":
                            store["2"] = True
                            store["SG"] = True
                        elif subgloss == "3SG":
                            store["3"] = True
                            store["SG"] = True
                        elif subgloss == "1DU":
                            store["1"] = True
                            store["DU"] = True
                        elif subgloss == "2DU":
                            store["2"] = True
                            store["DU"] = True
                        elif subgloss == "3DU":
                            store["3"] = True
                            store["DU"] = True
                        elif subgloss == "1PL":
                            store["1"] = True
                            store["PL"] = True
                        elif subgloss == "2PL":
                            store["2"] = True
                            store["PL"] = True
                        elif subgloss == "3PL":
                            store["3"] = True
                            store["PL"] = True
                        else:                        
                            store[subgloss] = True
        found_glosses = set(store.keys())
        found_LGR_glosses = found_glosses & LGRLIST #set intersection
        for lgr_gloss in found_LGR_glosses:
            GRAPH.add((QUESTRESOLVER[eaffile], DCTERMS.references, LGR[lgr_gloss]))

    print("writing output")
    with open(FILENAME.replace("json", "n3"), "wb") as rdfout:
        rdfout.write(GRAPH.serialize(format="n3"))
