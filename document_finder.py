from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

from pathlib import Path
import glob

class DocumentFinder():
    files = []
    corpus = []

    def __init__(self):
        pass

    def preprocess_document(self, raw_file):
        token_list = word_tokenize(raw_file)
    
        token_list = [token for token in token_list if token not in stopwords.words('english')]

        lemmatizer = WordNetLemmatizer()
        token_list = [lemmatizer.lemmatize(token) for token in token_list]

        ps = PorterStemmer()
        token_list = [ps.stem(token) for token in token_list]

        return token_list

    def get_recommended_documents(self):
        # Read documents
        directory_path = "./test_docs"
        text_files = glob.glob(f"{directory_path}/**/*.txt", recursive=True)
        print(text_files)

        # Produce tf-idf vector 
        vectorizer = TfidfVectorizer(input='filename', stop_words='english')
        vector = vectorizer.fit_transform(text_files)

        query = ['./query.txt']
        # Vectorize the query to the same length as documents
        query_vec = vectorizer.transform(query)
        # Compute the cosine similarity between query_vec and all the documents
        cosine_similarities = cosine_similarity(vector, query_vec).flatten()
        # Sort the similar documents from the most similar to less similar and return the indices
        most_similar_doc_indices = np.argsort(cosine_similarities, axis=0)[:-5-1:-1]

        # Match the indices of similar docs against the original input list to return the relevant docs
        counter = 1
        doc_titles = []
        for index in most_similar_doc_indices:
            doc_titles.append(text_files[index])
            print('Top-{}, Similarity = {}'.format(counter, cosine_similarities[index]))
            print('body: {}, '.format(text_files[index]))
            print()
            counter += 1
        return doc_titles