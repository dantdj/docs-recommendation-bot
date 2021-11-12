from nltk.corpus import PlaintextCorpusReader, stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
from document_finder import DocumentFinder


document_finder = DocumentFinder()
score = document_finder.get_recommended_documents()