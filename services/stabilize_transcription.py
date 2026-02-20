from typing import Optional

def extract_step_words(segments) -> list[str]:
    words: list[str] = []

    for segment in segments:
        if segment.words:
            for word in segment.words:
                token = word.word.strip().lower()
                if token:
                    words.append(token)
            continue

        text_tokens = getattr(segment, "text", "").strip().lower().split()
        for token in text_tokens:
            if token:
                words.append(token)
    
    return words

def stabilize_transcription(segments, committed_text: str, st_window: list, window_size: int = 3) -> tuple[Optional[str], str]:
    window_size = max(2, int(window_size))
    step_words = extract_step_words(segments)
    st_window.append(step_words)
    
    if len(st_window) > window_size:
        del st_window[:-window_size]
            
    if len(st_window) < window_size:
        return None, committed_text

    common_len = len(st_window[0])
    for words in st_window[1:]:
        common_len = min(common_len, len(words))
        idx = 0
        while idx < common_len and st_window[0][idx] == words[idx]:
            idx += 1
        common_len = idx
        if common_len == 0:
            break

    stable_text = " ".join(st_window[0][:common_len]).strip()

    if not stable_text or stable_text == committed_text:
        return None, committed_text

    if stable_text.startswith(committed_text):
        new_part = stable_text[len(committed_text):].strip()
        return (new_part if new_part else None), stable_text
    
    return stable_text, stable_text
           
