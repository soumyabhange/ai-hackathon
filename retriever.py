import json


def load_documents():
    with open("rag_documents.json", "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_documents(query):
    documents = load_documents()

    query = query.lower()

    results = []

    for document in documents:

        searchable_text = (
            document["endpoint"] + " "
            + document["method"] + " "
            + document["function"] + " "
            + document["parameters"] + " "
            + document["description"]
        ).lower()

        # Check whether words from the query appear in the document
        query_words = query.split()

        score = 0

        for word in query_words:
            if word in searchable_text:
                score += 1

        if score > 0:
            results.append((score, document))

    # Highest matching score first
    results.sort(reverse=True, key=lambda x: x[0])

    return [document for score, document in results]


if __name__ == "__main__":

    query = "get specific user"

    results = retrieve_documents(query)

    print("Search results:")
    print()
    for result in results:
        print(result)