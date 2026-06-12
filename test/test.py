from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer('all-MiniLM-L6-v2')

skill1="predictive learning"
skill2="machine learning"

em1=model.encode(skill1)
em2=model.encode(skill2)