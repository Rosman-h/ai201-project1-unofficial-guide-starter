import os

def load_documents(folder="documents"):
    docs = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append({
                "source": filename,
                "text": text
            })
    print(f"Loaded {len(docs)} documents")
    return docs

def clean_text(text):
    import re
    # Remove photo references
    text = re.sub(r'Photo \d+ in review by .+', '', text)
    # Remove owner response headers
    text = re.sub(r'.+\(Owner\)', '', text)
    # Remove emoji-heavy reaction lines
    text = re.sub(r'[❤️🙏👎😡💔]+\d*', '', text)
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    return text

def chunk_text(text, max_size=500):
    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 30]
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) <= max_size:
            current += " " + para if current else para
        else:
            if current:
                chunks.append(current.strip())
            current = para
    if current:
        chunks.append(current.strip())
    return chunks

def process_documents(folder="documents"):
    docs = load_documents(folder)
    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_index": i,
                "text": chunk
            })
    print(f"Total chunks: {len(all_chunks)}")
    return all_chunks

if __name__ == "__main__":
    chunks = process_documents()
    # Print 5 sample chunks to inspect
    print("\n--- SAMPLE CHUNKS ---")
    for chunk in chunks[:5]:
        print(f"\nSource: {chunk['source']}")
        print(f"Chunk {chunk['chunk_index']}: {chunk['text']}")
        print("-" * 40)