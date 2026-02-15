from audio.input.audio_queues import t_audio_q, w_audio_q

def t_audio_callback(indata, frames, time, status):
    if status:
        print(status)
    t_audio_q.put(indata[:, 0].copy())

def w_audio_callback(indata, frames, time, status):
    if status:
        print(status)
    w_audio_q.put(indata[:, 0].copy())