import ollama
import numpy as np

# Function to convert text to vector
def convertToVector(text):
    # Check if text is empty and assign zero vector
    if not text.strip():
        return [0] * 1024  # Assuming the embedding size is 1024
    else:
        # Return the embedding from the model
        return ollama.embeddings(model="mxbai-embed-large", prompt=text)['embedding']

# Function to produce similarity result from two vectors
def produceSimilarityResult(jobDescriptionEmbedding, cvEmbedding):
    # Convert embeddings to numpy arrays
    jobDescriptionEmbedding_array = np.array(jobDescriptionEmbedding)
    cvEmbedding_array = np.array(cvEmbedding)

    # Check if any of the embeddings are empty (all zeros)
    if np.all(jobDescriptionEmbedding_array == 0) or np.all(cvEmbedding_array == 0):
        # If one of the embeddings is all zeros, cosine similarity is zero
        return 0.0

    # Compute cosine similarity
    cosine_similarity_value = np.dot(jobDescriptionEmbedding_array, cvEmbedding_array) / (np.linalg.norm(jobDescriptionEmbedding_array) * np.linalg.norm(cvEmbedding_array))

    # Convert cosine similarity to a percentage score
    percentage_score = (cosine_similarity_value + 1) / 2 * 100

    return percentage_score
