from ollama import chat
from ollama import ChatResponse
from config import SYSTEM_PROMT

responce: ChatResponse = chat(
    model="gemma3:12b-it-qat",
    messages=[{"role":"user", "content": "Repeat the story you told me please"}, {"role":"system", "content":SYSTEM_PROMT}],
    keep_alive="-1m"
)

print(responce.message.content)

