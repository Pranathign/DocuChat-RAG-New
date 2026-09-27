from sklearn.feature_extraction.text import TfidfVectorizer
import faiss

def chunk_documents(documents, chunk_size=1000):
    chunks = []
    for doc in documents:
        for i in range(0, len(doc), chunk_size):
            chunks.append(doc[i:i + chunk_size])
    return chunks

def vectorize_chunks(chunks):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(chunks).toarray()
    return vectors, vectorizer

def store_vectors_in_faiss(vectors):
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)
    return index
