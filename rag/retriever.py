import numpy as np
from services.library_service import LibraryService
from rag.embedder import embed_texts

service = LibraryService()

def _book_to_text(book):
    return f"{book.title} by {book.author}, category: {book.category}, {book.available_copies} copies available"

def retrieve_relevant_books(query, k=5):
    books = service.book_repo.get_all()
    if not books:
        return []
    texts = [_book_to_text(b) for b in books]
    book_vectors = embed_texts(texts)
    query_vector = embed_texts([query])[0]
    scores = book_vectors @ query_vector
    top_indices = np.argsort(scores)[::-1][:k]
    return [books[i] for i in top_indices]


    