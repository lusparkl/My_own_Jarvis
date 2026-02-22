from tools.memory import retrieve_memory
from tools.weather import get_current_weather, get_forecast
from tools.keyboard import paste_from_user_keyboard, copy_to_user_keyboard
from tools.todo import add_todo, get_todos, delete_todo
from ollama import chat
from ollama import ChatResponse
import config

available_functions = {
    "retrieve_memory": retrieve_memory,
    "get_current_weather": get_current_weather,
    "get_forecast": get_forecast,
    "copy_to_user_keyboard": copy_to_user_keyboard,
    "paste_from_user_keyboard": paste_from_user_keyboard,
    "add_todo": add_todo,
    "get_todos": get_todos,
    "delete_todo": delete_todo
}

MEMORY_BEHAVIOR_GUARD = {
    "role": "system",
    "content": (
        "Always prioritize the latest user message first. "
        "Use retrieve_memory only as supporting context. "
        "If memory is unrelated or conflicts with the latest user message, ignore it."
    ),
}

def build_request_messages(messages: list) -> list:
    if not messages:
        return [MEMORY_BEHAVIOR_GUARD]

    if messages[0].get("role") == "system":
        return [messages[0], MEMORY_BEHAVIOR_GUARD] + messages[1:]

    return [MEMORY_BEHAVIOR_GUARD] + messages

def get_llm_responce(messages) -> str:
    tool_rounds = 0
    used_tool_calls = set()

    while True:
        request_messages = build_request_messages(messages)
        request_data = {
            "model": config.GPT_MODEL,
            "messages": request_messages,
            "keep_alive": "-1m",
            "tools": [retrieve_memory, get_current_weather, get_forecast, copy_to_user_keyboard, paste_from_user_keyboard, add_todo, delete_todo, get_todos],
            "think": True
        }

        response: ChatResponse = chat(
            **request_data
        )
    
        messages.append(response.message)

        if response.message.tool_calls:
            tool_rounds += 1
            if tool_rounds > 5:
                return (response.message.content or "").strip()

            had_new_tool_result = False
            for tc in response.message.tool_calls:
                if tc.function.name in available_functions:
                    arguments = tc.function.arguments or {}
                    if not isinstance(arguments, dict):
                        arguments = {}

                    tool_call_key = (
                        tc.function.name,
                        tuple(sorted((str(k), str(v)) for k, v in arguments.items()))
                    )
                    if tool_call_key in used_tool_calls:
                        continue
                    used_tool_calls.add(tool_call_key)

                    had_new_tool_result = True
                    result = available_functions[tc.function.name](**arguments)
                    messages.append({'role': 'tool', 'tool_name': tc.function.name, 'content': str(result)})

            if not had_new_tool_result:
                return (response.message.content or "").strip()
        else:
            return (response.message.content or "").strip()


