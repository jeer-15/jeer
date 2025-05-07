# Required packages: 
# pip install beautifulsoup4 sentence-transformers faiss-cpu pdfplumber python-dotenv requests

import os
from bs4 import BeautifulSoup
import pdfplumber
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import requests
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ----------------------------
# 1️⃣ EXTRACT TEXT FROM HTML
# ----------------------------
def extract_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(['script', 'style']):
        script.decompose()
    text = soup.get_text(separator=' ', strip=True)
    return text

# ----------------------------
# 2️⃣ EXTRACT TEXT FROM PDF
# ----------------------------
def extract_text_from_pdf(file_path):
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + ' '
    return text

# ----------------------------
# 3️⃣ LOAD FILES
# ----------------------------
html_pdf_dir = './website_html'
all_docs = []

for filename in os.listdir(html_pdf_dir):
    filepath = os.path.join(html_pdf_dir, filename)
    if filename.endswith('.html') or filename.endswith('.htm'):
        print(f"🔍 Extracting from HTML: {filename}")
        text = extract_text_from_html(filepath)
        all_docs.append(text)
    elif filename.endswith('.pdf'):
        print(f"🔍 Extracting from PDF: {filename}")
        text = extract_text_from_pdf(filepath)
        all_docs.append(text)

print(f"✅ Extracted {len(all_docs)} documents (HTML + PDF)")

# ----------------------------
# 4️⃣ CHUNK TEXT
# ----------------------------
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

all_chunks = []
for doc in all_docs:
    chunks = chunk_text(doc)
    all_chunks.extend(chunks)

print(f"✅ Total chunks: {len(all_chunks)}")

# ----------------------------
# 5️⃣ GENERATE EMBEDDINGS
# ----------------------------
print("🔍 Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("🔍 Generating embeddings...")
embeddings = model.encode(all_chunks, convert_to_numpy=True, show_progress_bar=True)

# ----------------------------
# 6️⃣ STORE EMBEDDINGS IN FAISS
# ----------------------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print(f"✅ Stored {embeddings.shape[0]} vectors in FAISS index")

print("\n🤖 Chatbot is ready! Type 'exit' to quit.\n")

# 🔍 SEARCH FUNCTION
def search_query(query, top_k=3):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    retrieved_chunks = [all_chunks[i] for i in indices[0]]
    return retrieved_chunks

# 🔍 FUNCTION TO CALL OPENROUTER API
def call_openrouter(prompt, model_name="openai/gpt-3.5-turbo", temperature=0.7):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ Error: {e}"

while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        print("🤖 Goodbye!")
        break

    results = search_query(query, top_k=3)
    context = "\n\n".join(results)

    prompt = f"""You are an AI customer support assistant for an education company that provides technical courses, certifications, and internship programs.

Your role is to answer customer queries clearly, warmly, positively, and helpfully, based only on the company’s official website and document content provided below.

The company offers:
- Short-term and long-term internship programs in software development, data science, AI/ML, web development, etc.
- Certification courses with both online and offline options
- Placement assistance for eligible students
- Practical hands-on training opportunities

✅ Always maintain a positive, encouraging, welcoming tone, making the user feel excited about learning opportunities.

✅ If a user asks about eligibility for a course they may be too early for, respond in an uplifting way such as:  
“Great to see your enthusiasm at this stage! While this course is designed for students with prior experience, we’d love to guide you toward beginner-friendly resources so you can build your skills and join us soon.”

✅ If information is not found in the provided content, respond positively:  
“We’d love to assist you further! Please contact our support team for the latest details—we’re happy to help.”

Here is the official website and document content:

{context}

Now answer this customer query positively, encouragingly, and helpfully:

{query}
"""

    answer = call_openrouter(prompt)
    print(f"\n🤖 Chatbot: {answer}\n")
