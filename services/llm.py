from services.memory import retrieve_memory
from ollama import chat
from ollama import ChatResponse
import config

available_functions = {
    "retrieve_memory": retrieve_memory
}

def get_llm_responce(messages) -> str:
    while True:
            response: ChatResponse = chat(
            model=config.GPT_MODEL,
            messages=messages,
            keep_alive="-1m",
            tools=[retrieve_memory],
            think=True
            )
    
            messages.append(response.message)

            if response.message.tool_calls:
                for tc in response.message.tool_calls:
                    if tc.function.name in available_functions:
                        result = available_functions[tc.function.name](**tc.function.arguments)
                        messages.append({'role': 'tool', 'tool_name': tc.function.name, 'content': str(result)})
            else:
                return response.message.content


