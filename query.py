import os
from groq import Groq
from dotenv import load_dotenv
from embed import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(question):
    # Retrieve relevant chunks
    chunks = retrieve(question, k=5)
    
    # Build context from chunks
    context = ""
    sources = []
    for chunk in chunks:
        context += f"\n---\n{chunk['text']}\n"
        if chunk['source'] not in sources:
            sources.append(chunk['source'])
    
    # Build grounded prompt
    prompt = f"""You are a helpful assistant for Howard University students looking for off-campus housing advice.

Answer the question using ONLY the information provided in the documents below.
If the documents don't contain enough information to answer the question, say "I don't have enough information on that in my sources."
Do not use any outside knowledge — only what is in the documents.

Documents:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    
    answer = response.choices[0].message.content
    
    return {
        "answer": answer,
        "sources": sources
    }

if __name__ == "__main__":
    test_questions = [
        "What do students say about noise at Trellis House?",
        "How do Howard students afford off campus housing?",
        "What is the rent like at Mazza?"
    ]
    
    for question in test_questions:
        print(f"\n{'='*50}")
        print(f"Q: {question}")
        print('='*50)
        result = ask(question)
        print(f"A: {result['answer']}")
        print(f"\nSources: {', '.join(result['sources'])}")