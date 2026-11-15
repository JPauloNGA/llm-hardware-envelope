"""Assistente de voz ponta a ponta: WAV -> texto -> resposta -> WAV.

Mede a latencia de cada etapa e o total. O llama-server deve estar
rodando com o Qwen 0.5B em http://localhost:8080.
"""
import argparse
import json
import time
import urllib.request
import wave
from pathlib import Path

from faster_whisper import WhisperModel
from piper.voice import PiperVoice


def transcrever(modelo, wav_path):
    inicio = time.perf_counter()
    segments, _ = modelo.transcribe(str(wav_path), beam_size=1, language="en")
    texto = "".join(s.text for s in segments).strip()
    return texto, (time.perf_counter() - inicio) * 1000


def gerar_resposta(prompt, url):
    body = json.dumps({
        "model": "local",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Answer in one short sentence."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 40,
        "temperature": 0,
        "cache_prompt": True,
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    inicio = time.perf_counter()
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read().decode("utf-8"))
    texto = data["choices"][0]["message"]["content"].strip()
    return texto, (time.perf_counter() - inicio) * 1000


def sintetizar(voz, texto, out_path):
    inicio = time.perf_counter()
    with wave.open(str(out_path), "wb") as wav_file:
        voz.synthesize_wav(texto, wav_file)
    return (time.perf_counter() - inicio) * 1000


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="WAV de entrada (16kHz mono)")
    p.add_argument("--output", default="resposta.wav")
    p.add_argument("--whisper", default="tiny.en")
    p.add_argument("--piper", default=r"C:\models\voice\python\en_US-lessac-medium.onnx")
    p.add_argument("--server", default="http://localhost:8080/v1/chat/completions")
    args = p.parse_args()

    print("Carregando modelos...")
    t0 = time.perf_counter()
    whisper = WhisperModel(args.whisper, device="cpu", compute_type="int8")
    piper = PiperVoice.load(args.piper)
    print(f"  carregados em {(time.perf_counter()-t0)*1000:.0f} ms")

    print("\n[1/3] STT...")
    texto_user, t_stt = transcrever(whisper, args.input)
    print(f"  '{texto_user}'  ({t_stt:.0f} ms)")

    print("\n[2/3] LLM...")
    resposta, t_llm = gerar_resposta(texto_user, args.server)
    print(f"  '{resposta}'  ({t_llm:.0f} ms)")

    print("\n[3/3] TTS...")
    t_tts = sintetizar(piper, resposta, args.output)
    print(f"  {args.output}  ({t_tts:.0f} ms)")

    total = t_stt + t_llm + t_tts
    print(f"\n=== Latencia ponta a ponta: {total:.0f} ms ===")
    print(f"  STT: {t_stt:.0f} ms ({100*t_stt/total:.0f}%)")
    print(f"  LLM: {t_llm:.0f} ms ({100*t_llm/total:.0f}%)")
    print(f"  TTS: {t_tts:.0f} ms ({100*t_tts/total:.0f}%)")


if __name__ == "__main__":
    main()