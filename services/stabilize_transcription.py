from typing import Optional

def common_prefix_len(a, b, c) -> int:
    common_len = 0
    for w0, w1, w2 in zip(a, b, c):
        if w0 == w1 == w2:
            common_len += 1
        else: break
    return common_len

def extract_step_words(segments) -> list[str]:
    words: list[str] = []

    for segment in segments:
        for word in segment.words:
            token = word.word.strip().lower()
            if token:
                words.append(token)
    
    return words

def stabilize_transcription(segments, committed_text: str, st_window: list) -> tuple[Optional[str], str]:
    step_words = extract_step_words(segments)
    st_window.append(step_words)
    
    if len(st_window) > 3:
        del st_window[:-3]
            
    if len(st_window) < 3:
        return None, committed_text

    common_len = common_prefix_len(st_window[0], st_window[1], st_window[2])
    stable_text = " ".join(st_window[0][:common_len]).strip()

    if not stable_text or stable_text == committed_text:
        return None, committed_text

    if stable_text.startswith(committed_text):
        new_part = stable_text[len(committed_text):].strip()
        return (new_part if new_part else None), stable_text
    
    return stable_text, stable_text
           