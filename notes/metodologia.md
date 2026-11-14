# Metodologia

## Hardware

- CPU: Intel Xeon E5-2680 v4 (14 núcleos / 28 threads, Broadwell, sem AVX-512)
- RAM: 32 GB DDR4 quad-channel 2133 MHz
- GPU: AMD Radeon RX 580 2048SP, 8 GB VRAM (7.367 MiB livres reportados pelo Vulkan)
- Disco: SSD SATA (135 GB livres) + HD SATA (293 GB livres)
- SO: Windows 10 (build 19045)

## Software

- llama.cpp build b12384 (commit 3549c274d), compilado com `-DGGML_VULKAN=ON`
- Vulkan SDK 1.4.363.1
- Modelo: Mistral-7B-Instruct-v0.2 Q4_K_M (4,07 GB), de TheBloke

## Protocolo

- Prompt fixo: "Explain in one paragraph why local LLM inference matters."
- 128 tokens gerados por execução
- Contexto: 2048
- Threads: 28 (todos os threads lógicos do Xeon)
- `--no-warmup` desativado o aquecimento; `-st` (single-turn) evita o modo chat interativo
- 3 execuções por configuração; o valor reportado é a **mediana**
- Configurações: GPU (`-ngl 100 --device Vulkan0`) e CPU pura (`-ngl 0`)

## Caveats

- Single-stream: não mede concorrência nem throughput agregado.
- Uma única máquina, um único modelo, uma única quantização.
- O Windows e o driver AMD usam parte da VRAM; 7.367 MiB é o teto real, não 8.192.
- Medições interrompidas (Ctrl+C) não são válidas e foram descartadas.