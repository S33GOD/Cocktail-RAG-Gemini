# Cocktail-RAG-Gemini
## This project allows you to interact with a chat model using FastAPI, Pinecone for vector storage, and HuggingFace embeddings. It also uses the Gemini LLM for processing user input. The app provides an HTML frontend where users can interact with the model.

# Requirements
To run this project locally, you need to install the following dependencies:

## Python Libraries
The following libraries are required:
```
llama_index
pinecone-client
huggingface-hub
fastapi
uvicorn
python-dotenv
```
You can install these dependencies using pip. Create a requirements.txt file with the following contents:

```
llama_index
pinecone-client
huggingface-hub
fastapi
uvicorn
python-dotenv
```
Alternatively, you can install the libraries directly by running:

```
pip install llama_index pinecone-client huggingface-hub fastapi uvicorn python-dotenv
```
#Setup
##Set up your environment variables:

Create a .env file in the root directory of the project.
Add your Pinecone API key and any other necessary environment variables (e.g., HuggingFace API key).
Example .env file:

```.env
PINECONE_API_KEY="your_pinecone_api_key"
EMBEDDING_MODEL_NAME="ibm-granite/granite-embedding-125m-english"
GEMINI_API_KEY="your_gemini_api_key"
```

## To create index in pinecone using tabular data - run upsert.py file

##Running the Application Locally:

You can run the app using the uvicorn server. There is a function in the code that can run uvicorn, or you can manually run it from the terminal.

##To start the FastAPI server:

```
uvicorn app:app --reload
```
The server will start running on http://127.0.0.1:8000. You can access the healthcheck and other routes via this address.

##Running the Frontend (index.html):

The index.html file provides the user interface for interacting with the chat model. To run it:

Open the index.html file in your browser.
Ensure that the backend is running and accessible via http://127.0.0.1:8000.
The frontend will make API calls to the backend for generating responses from the model.
Project Structure
```
/project-root
  |__ static              # frontend
      |_ index.html
      |_ script.js
  |__ app.py              # FastAPI backend
  |__ embedder.py         # Model wrapper for pinecone upsert
  |__ .env                # Environment variables
  |__ final_cocktails.csv # table containing cocktail info
  |__ upsert.py           # Pinecone index creation and upsertion
  |__ RAG.py              # Server class for request handling
  |__ README.md           # Project documentation (this file)
```
## FastAPI Endpoints
POST /chat - Accepts user input and generates a response from the model.
```
{
  "user_input": "your input here"
}
```
GET /healthcheck - Used to check if the server is running.

# Summary
This project successfully implements a RAG system using Gemini as the base model and Pinecone as the vector database. The FastAPI backend efficiently handles queries, while a simple frontend interface ensures easy access to model responses.

Key Results:
Accurate Responses – The model retrieves and generates relevant answers effectively.
Efficient Vector Storage – Pinecone enables fast retrieval of indexed knowledge.

However there is a performance Issue, response times can be slow, indicating potential optimization areas.

Overall, the project achieves its goal of building an accessible RAG-based chatbot but may require performance improvements. 

Thought Process Behind Key Steps
1. Reformatting Tabular Data to Prompts
Goal: Convert structured data (tables) into natural language prompts that an LLM can understand.
- Extract relevant columns and rows from the table.
- Reformat each row into a structured text format (e.g., "Cocktail: Margarita | Ingredients: Tequila, Lime, Triple Sec").
- Ensure consistency in formatting to enhance retrieval quality.
- Store the transformed text data in the vector database for efficient search.
2. Creating a Vector Index Using LlamaIndex
Goal: Enable fast and accurate retrieval of information using an efficient vector index.
- Load data from structured or unstructured sources (e.g., documents, tables, JSON).
- Use LlamaIndex to generate embeddings for each data chunk.
- Store these embeddings in Pinecone for vector-based retrieval.
- Optimize chunk size to balance retrieval accuracy and efficiency.
- Use RetrieverQueryEngine to fetch relevant documents based on user queries.
3. Creating Vector Memory for Better User Interaction
- Implement VectorMemory from LlamaIndex to store past user inputs and responses.
- On each new query, retrieve relevant past interactions and provide context-aware responses.
- Upsert new user information into Pinecone for personalization and recall in future queries.
- Optimize memory size to prevent excessive storage while ensuring effective recall.
4. Creating the Interface and Implementing FastAPI
Frontend (HTML + JS):
- Create a clean input field for user queries.
- Display responses dynamically in an output box.
- Add loading indicators to improve UX while waiting for model responses.
Backend (FastAPI):
- Set up FastAPI endpoints (/chat, /healthcheck).
- Process incoming requests, format queries, and retrieve relevant responses.
- Integrate with LlamaIndex and Pinecone for vector search.
- Implement CORS to allow frontend-backend communication.
Deployment Considerations:
- Optimize FastAPI for better response times (e.g., async processing).
- Handle errors gracefully using logging and exception handling.
