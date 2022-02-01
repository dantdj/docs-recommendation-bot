from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

import glob

class DocumentFinder():
    files = []
    corpus = []
    vectorizer = TfidfVectorizer()

    def __init__(self):
        pass

    def preprocess_document(self, raw_file):
        token_list = word_tokenize(raw_file)

        lemmatizer = WordNetLemmatizer()
        token_list = [lemmatizer.lemmatize(token) for token in token_list]

        return token_list

    def noop_tokenizer(self, text):
        return text

    def get_recommended_documents(self, query, configured_directories):
        doc_titles = []
        chosen_directory = {}

        for directory in configured_directories:
            chosen_directory = directory
            file_list = self.get_file_list(directory)
            document_list = self.get_document_list(file_list)
            
            # Using a no-op tokenizer here as we tokenized ourselves during pre-processing
            vectorizer = TfidfVectorizer(tokenizer=self.noop_tokenizer, lowercase=False)
            vector = vectorizer.fit_transform(document_list)

            query_list = [self.preprocess_document(query)]
            query_vec = vectorizer.transform(query_list)

            cosine_similarities = cosine_similarity(vector, query_vec).flatten()
            most_similar_doc_indices = np.argsort(cosine_similarities, axis=0)[:-5-1:-1]

            max_similarity = max(cosine_similarities)
            for index in most_similar_doc_indices:
                # Only include document if the similarity score is at least 75% of the highest similarity score
                # This means we return multiple documents when similar scores are seen, but only one when a document
                # is a clear winner
                if cosine_similarities[index] > max_similarity * 0.75:
                    doc_titles.append(file_list[index])
                    self.print_file_similarity(cosine_similarities[index], file_list[index])
                
        
        return (doc_titles, chosen_directory)

    def print_file_similarity(self, similarity, filename):
        print('Similarity = {}'.format(similarity))
        print('File: {}, '.format(filename))
        print()

    def get_document_list(self, file_list):
        document_list = []
        for file in file_list:
            with open(file) as f:
                preprocessed_document = self.preprocess_document(f.read())
                document_list.append(preprocessed_document)

        return document_list

    def get_file_list(self, directory):
        file_list = glob.glob(f"{directory['path']}/**/*.md", recursive=True)

        # Remove the README files - they're just content pages and can throw things off
        file_list = [filename for filename in file_list if "readme.md" not in filename.lower()]

        return file_list