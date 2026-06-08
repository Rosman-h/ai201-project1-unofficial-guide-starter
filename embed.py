import chromadb
from sentence_transformers import SentenceTransformer
from ingest import process_documents


def embed_and_store():
    chunks = process_documents()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("Model loaded")
    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        client.delete_collection("housing")
    except:
        pass
    collection = client.create_collection("housing")
    print("Embedding chunks...")
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk["text"]).tolist()
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[{"source": chunk["source"], "chunk_index": chunk["chunk_index"]}]
        )
    print(f"Stored {len(chunks)} chunks")


def retrieve(query, k=5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("housing")
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks


if __name__ == "__main__":
    embed_and_store()
    print("\nTesting retrieval...")
    test_queries = [
        "What do students say about noise at Trellis House?",
        "How do Howard students afford off campus housing?",
        "Is Mazza a good place to live for Howard students?"
    ]
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"QUERY: {query}")
        print('='*50)
        results = retrieve(query)
        for r in results:
            print(f"\nSource: {r['source']}")
            print(f"Distance: {r['distance']:.3f}")
            print(f"Text: {r['text'][:200]}")
            print("-"*40)