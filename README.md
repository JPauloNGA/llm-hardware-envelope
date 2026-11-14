# LLM Hardware Envelope

Medições reproduzíveis de inferência local em hardware heterogêneo e obsoleto: um Xeon de 14 núcleos e uma RX 580 de 8 GB, sem GPU moderna, sem nuvem.

## A pergunta

Qual é o envelope real de utilidade de um LLM local em hardware de 2016? Onde a GPU antiga vence, onde a CPU ainda serve, e onde nenhum dos dois é suficiente?

## Hardware

| Componente | Especificação |
|---|---|
| CPU | Xeon E5-2680 v4 (14c/28t, Broadwell) |
| RAM | 32 GB DDR4 quad-channel 2133 MHz |
| GPU | AMD RX 580 2048SP, 8 GB (Vulkan) |
| SO | Windows 10 |

## Resultados (Mistral 7B Q4_K_M, mediana de 3 execuções)

| Backend | Prefill (t/s) | Decode (t/s) |
|---|---|---|
| RX 580 Vulkan | **68,9** | **20,1** |
| Xeon CPU pura | 25,8 | 9,0 |

Prompt fixo, 128 tokens, contexto 2048, 28 threads. Metodologia completa em `notes/metodologia.md`; dados brutos em `data/medicoes.csv`.

## O que os números dizem

- **A GPU vence nas duas fases**, mas por margens diferentes: ~2,7× no prefill e ~2,2× no decode.
- **20 tok/s de decode** é confortável para uso interativo. **9 tok/s na CPU** é utilizável, mas no limite da paciência.
- **A CPU não é inútil.** Para um modelo 7B, ela entrega respostas em tempo real se você aceitar esperar o dobro.
- O teto real da VRAM é **7.367 MiB**, não 8.192 — o Windows e o driver consomem o resto. Isso define quantas camadas de um modelo maior cabem na GPU.

## Próximos passos

- [ ] Testar um modelo MoE (~30B) no modo híbrido GPU+CPU, para medir onde os dois colaboram.
- [ ] Medir TTFT (time-to-first-token) separadamente do throughput.
- [ ] Adicionar um modelo denso maior (13B) para encontrar o ponto em que a GPU deixa de caber.