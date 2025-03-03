import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class FAISSManager:
    def __init__(self, model_name="all-MiniLM-L6-v2", index_file="faiss_index"):
        """Initialize FAISS with SentenceTransformers embeddings."""
        self.model = SentenceTransformer(
            model_name)  # Load the embedding model
        self.index_file = index_file
        self.index = None
        self.documents = []  # Store actual documents
        self.id_map = {}  # Track FAISS ID -> Document mapping

        try:
            self.load_index()  # Try to load existing FAISS index
        except Exception:
            self.index = faiss.IndexFlatL2(
                self.model.get_sentence_embedding_dimension())

    def add_documents(self, documents):
        """Add new documents to FAISS index with proper ID mapping."""
        embeddings = self.model.encode(documents, convert_to_numpy=True)

        start_id = len(self.documents)  # Track starting index
        self.documents.extend(documents)  # Store documents

        # Assign FAISS index IDs and store mappings
        for i, doc in enumerate(documents):
            self.id_map[start_id + i] = doc

        # If index is empty, initialize it
        if self.index.is_trained:
            self.index.add(embeddings)
        else:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings)

        self.save_index()

    def retrieve_similar_docs(self, query, top_k=2):
        """Retrieve similar documents from FAISS."""
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)

        results = [self.id_map[i] for i in indices[0] if i in self.id_map]
        return results if results else ["No relevant documents found."]

    def save_index(self):
        """Save FAISS index and documents."""
        faiss.write_index(self.index, self.index_file)
        np.save(self.index_file + "_docs.npy",
                np.array(self.documents, dtype=object))
        np.save(self.index_file + "_id_map.npy", self.id_map)  # Save ID map

    def load_index(self):
        """Load FAISS index and documents."""
        self.index = faiss.read_index(self.index_file)
        self.documents = np.load(
            self.index_file + "_docs.npy", allow_pickle=True).tolist()
        self.id_map = np.load(self.index_file + "_id_map.npy",
                              allow_pickle=True).item()  # Load ID map
