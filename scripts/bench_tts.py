import time
from piper.voice import PiperVoice

voice = PiperVoice.load(r"C:\models\voice\python\en_US-lessac-medium.onnx")

frases = [
    "Hello, this is a test.",
    "The quick brown fox jumps over the lazy dog.",
    "Local inference is possible with old hardware.",
]

# Warmup
list(voice.synthesize("Warmup."))

tempos = []
for frase in frases:
    inicio = time.perf_counter()
    list(voice.synthesize(frase))
    fim = time.perf_counter()
    tempos.append((fim - inicio) * 1000)
    print(f"'{frase[:30]}...': {tempos[-1]:.0f} ms")

print(f"\nMediana: {sorted(tempos)[len(tempos)//2]:.0f} ms")