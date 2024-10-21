import pinecone
import openai
import json

openai.api_key = OPENAI_API_KEY
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("notes")

# Uploads each chunk from a notes json file to a Pinecone namespace
def upload_json_to_pinecone(json_file_path, namespace):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    for i, entry in enumerate(data):
        page_number = entry.get("page_number")
        text = entry.get("text")
        
        # Get the embedding for the text from OpenAI
        response = openai.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        embedding = response.data[0].embedding
        metadata = {
            "page_number": page_number,
            "text": text
        }
        
        # Upload to Pinecone
        vector_id = f"chunk_{i}"
        index.upsert(vectors=[(vector_id, embedding, metadata)], namespace=namespace)

        print(f"Uploaded {vector_id} to Pinecone.")

def query_pinecone(query_text, namespace, top_k=5):
    # Turn query text into embedding using OpenAI API
    response = openai.embeddings.create(
        input=query_text,
        model="text-embedding-3-small"
    )
    query_embedding = response.data[0].embedding

    results = index.query(namespace=namespace, vector=query_embedding, top_k=top_k, include_metadata=True)
    
    return results

# Example query
query_text = "What is a Jacobian Matrix"
search_results = query_pinecone(query_text, "EXAMPLE-NAMESPACE")

# Print the results
for match in search_results['matches']:
    print(f"Score: {match['score']}")
    print(f"Page Number: {match['metadata']['page_number']}")
    print(f"Text: {match['metadata']['text']}\n")
