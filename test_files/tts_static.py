import torch
from TTS.api import TTS

# Get device
device = "cuda"

# Initialize TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

print("starting to compute")

tts.tts_to_file(
  text="""Okay, let's break down Vieta's Theorem.

It essentially relates the coefficients of a polynomial equation to the sums and products of its roots.

**Here's the gist for a quadratic equation (ax² + bx + c = 0):**

*   **Sum of roots:**  -b/a
*   **Product of roots:** c/a

**For a cubic equation (ax³ + bx² + cx + d = 0):**

*   **Sum of roots:** -b/a
*   **Sum of pairwise products of roots:** c/a
*   **Product of roots:** -d/a

And so on for higher-degree polynomials.

**Why is it useful?** It lets you find relationships between roots without actually solving for them""",
  speaker="Jarvis",
  language="en",
  file_path="static_test.wav"
)