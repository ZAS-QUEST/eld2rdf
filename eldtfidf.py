import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np     

JSONFILE = json.loads(open('glosses-elareafs.json').read()) 
documents = [" ".join([x for x in JSONFILE[f][type_][tier][1] if re.search("^[^a-z]+$", x) and re.search("[A-Z]", x)]) for f in JSONFILE for type_ in JSONFILE[f] for tier in JSONFILE[f][type_] ]
tfidf = TfidfVectorizer().fit_transform(documents)
# no need to normalize, since Vectorizer will return normalized tf-idf
pairwise_similarity = tfidf * tfidf.T

arr = pairwise_similarity.toarray() 
np.fill_diagonal(arr, np.nan)    #no self sim
mostsimilardocnumbers = [np.nanargmax(arr[x]) for x, throwaway in enumerate(arr)]
mostsimilardocs = [docs[np.nanargmax(arr[x])] for x, throwaway in enumerate(arr)]
