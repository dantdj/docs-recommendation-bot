
from dotenv import load_dotenv

from document_finder import DocumentFinder

load_dotenv()
document_finder = DocumentFinder()
score = document_finder.get_recommended_documents()