from vector_store_setup import get_vector_store
from ollama import Client

def process_query(query):
    # Load the vector store and embedding model
    vector_store, embedding_model = get_vector_store()

    # Perform similarity search
    results = vector_store.similarity_search(query, k=5)

    # Prepare the context for the prompt
    context = "\n\n".join([doc.page_content for doc in results])
    prompt = f"""You are a compassionate mental health therapist.
Using the following counseling examples, respond empathetically to the user.
and the output should be in the form of a conversation between a therapist and a user.
it should not be more than 30 words.

Context:
{context}

User: {query}
Therapist:"""

    # Use the Ollama client to get the response
    client = Client(host='http://localhost:11434')
    response = client.chat(model='mistral', messages=[{"role": "user", "content": prompt}])

    # # Print the response separately
    # print("\n🧠 Mistral's Response:\n")
    # print(response['message']['content'])
    return response['message']['content']

print (process_query("I am feeling very depressed."))