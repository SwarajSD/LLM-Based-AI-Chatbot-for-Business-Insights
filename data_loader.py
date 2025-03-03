from faiss_manager import FAISSManager

# Initialize FAISS database
db_manager = FAISSManager()

# Sample business insights data
documents = [
    "The Q4 revenue increased by 20% due to strong product sales.",
    "Customer retention strategies improved engagement by 15%.",
    "AI-driven analytics helped optimize supply chain costs by 12%.",
]

# Store documents in FAISS
db_manager.add_documents(documents)

print("✅ Documents added successfully!")
