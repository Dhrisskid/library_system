import anthropic
from rag.retriever import retrieve_relevant_books

client = anthropic.Anthropic()

def answer_query(query):
    relevant_books = retrieve_relevant_books(query, k=5)
    if not relevant_books:
        context = "No books currently in the catalog."
    else:
        context = "\n".join(
            f"- {b.title} by {b.author} (category: {b.category}, ISBN: {b.isbn}, available copies: {b.available_copies})"
            for b in relevant_books
        )

    system_prompt = (
        "You are a librarian assistant. Answer the user's question using only the "
        "catalog information provided below. If the answer isn't in the catalog, say so.\n\n"
        f"Catalog:\n{context}"
    )

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=system_prompt,
        messages=[{"role": "user", "content": query}]
    )
    return response.content[0].text


    