import json

transcription_dictionary = json.loads(open('transcriptions.json').read())
translation_dictionary = json.loads(open('translations.json').read())

triples = []
for filename in translation_dictionary: 
    for tierkey in translation_dictionary[filename]:
        print(tierkey)
        tierlist = translation_dictionary[filename][tierkey] 
        for i, tier in enumerate(tierlist):
            tierID = filename+tierkey+str(i)
            triples.append((tierID, 'a', 'quest:tier'))
            triples.append((tierID, 'rdfs:label', " ".join(tier)))
            for j, annotation in enumerate(tier):
                annotationID = "%s/%s/%s/%s"%(filename,tierkey,i,j) #check for underscores in filenames TODO
                triples.append((annotationID, 'a', 'quest:tier'))
                triples.append((annotationID, 'rdfs:label', '"%s"'%annotation))
                
        
#print(triples)
print("\n".join([" ".join(triple) for triple in triples]))
        
