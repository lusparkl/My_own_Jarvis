import chromadb
import config
import ollama
from datetime import datetime

client = chromadb.PersistentClient(path=config.MEMORY_DB_PATH)
collection = client.get_or_create_collection(name=config.COLLECTION_NAME, 
    embedding_function=chromadb.utils.embedding_functions.DefaultEmbeddingFunction())

def save_chat(messages: list):
    chat = ""
    
    for m in messages:
        chat += f'{m["role"]}: <<{m["content"]}>>' +'\n\n'
    
    id = str(collection.count() + 1)
    tags = ollama.generate(model=config.GPT_MODEL, prompt=config.SUMMARIZING_PROMT+"\n"+chat)["response"]
    metadata = {
        "tags": tags,
        "date": datetime.today().strftime("%Y-%m-%d"),
        "time": datetime.today().strftime("%H:%M")
    }

    collection.add(ids=[id],documents=[chat], metadatas=[metadata])

def retrieve_memory(query: str):
    """When you need additional knowledge, you can use this tool to retrieve chats history with user.
  
    Args:
      query: The user question or the topic of the current chat.

    Returns:
      Chat history with user, that you can use to respond a question.
    """
   
    res_db = collection.query(query_texts=[query])["documents"][0][0:10]
    history = "".join(res_db).replace("\n", " ")
    return history