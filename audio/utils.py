from config import CHUNKS_CHAR_LIMIT

def capture_silence(st_window: list) -> bool:
    for step in st_window:
        if len(step) > 0:
            return False
    
    return True

def list_get(list: list, i: int, default):
    return list[i] if i < len(list) else default

def split_text_into_sentences(text: str) -> list:
    splited = text.strip().split("\n")
    sentences = []
    for par in splited:
        if par:
            par = par.strip()
            if len(par) < CHUNKS_CHAR_LIMIT:
                sentences.append(par.strip())
            else:
                sentences.extend(par.split("."))
            
    return sentences

def cut_responce_to_text_chunks(llm_responce: str) -> list:
    sentences = split_text_into_sentences(llm_responce)
    curr = ""
    chunks = []
    for i in range(len(sentences)):
        curr = f"{curr} {sentences[i]}"

        next_iter_len = len(f"{curr} {list_get(sentences, i+1, ' ')}")
        if next_iter_len < CHUNKS_CHAR_LIMIT and i != len(sentences)-1:
            continue

        chunks.append(curr)
        curr = ""
    
    return chunks
