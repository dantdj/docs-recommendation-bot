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

        lemmatizer = WordNetLemmatizer()
        token_list = [lemmatizer.lemmatize(token) for token in token_list]

        return token_list

    def noop_tokenizer(self, text):
        return text

    def get_recommended_documents(self, query):
        # Read documents
        directory_path = "./test_docs"
        text_files = glob.glob(f"{directory_path}/**/*.txt", recursive=True)
        print(text_files)

        document_list = []
        for file in text_files:
            with open(file) as f:
                preprocessed_document = self.preprocess_document(f.read())
                document_list.append(preprocessed_document)

        # Produce tf-idf vector 
        vectorizer = TfidfVectorizer(tokenizer=self.noop_tokenizer, lowercase=False)
        vector = vectorizer.fit_transform(document_list)

        query_list = [self.preprocess_document(query)]

        # Vectorize the query to the same length as documents
        query_vec = vectorizer.transform(query_list)

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