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

## Resultados

### Mistral 7B Q4_K_M — dois instrumentos, dois regimes

| Instrumento | Backend | Prefill (t/s) | Decode (t/s) |
|---|---|---|---|
| `llama-cli` (prompt ~19 tokens) | RX 580 Vulkan | 68,9 | 20,1 |
| `llama-cli` (prompt ~19 tokens) | Xeon CPU pura | 25,8 | 9,0 |
| `llama-bench` (pp512) | RX 580 Vulkan | **115,1 ± 0,1** | **20,6 ± 0,1** |
| `llama-bench` (pp512) | Xeon CPU pura | **91,1 ± 0,2** | **9,7 ± 0,3** |

![Resultados](data/grafico_mistral.png)

O **decode** concorda entre os dois instrumentos (20,1 vs 20,6 na GPU; 9,0 vs 9,7 na CPU). Esse é o sinal mais importante: a velocidade de geração é estável e não depende do comprimento do prompt nem da ferramenta de medição. É o número que determina a experiência de uso.

O **prefill** diverge porque mede regimes diferentes. Com um prompt curto (~19 tokens), o custo fixo de inicialização do grafo e das transferências domina, e a GPU parece 2,7× mais rápida. Com 512 tokens (`pp512`), o hardware satura: o Xeon sobe para 91 t/s, ainda atrás da GPU (115 t/s), mas muito mais perto. **Nenhum dos dois números está errado; eles respondem a perguntas diferentes.** O README reporta os dois, com o instrumento e o comprimento do prompt explícitos.

### O que os números dizem

- **A GPU vence nas duas fases**, mas por margens diferentes: ~2,2× no decode e ~1,3× no prefill saturado (512 tokens).
- **20 tok/s de decode** é confortável para uso interativo. **9,7 tok/s na CPU** é utilizável, mas no limite da paciência para respostas longas.
- **A CPU não é inútil.** Para um modelo 7B, ela entrega respostas em tempo real se você aceitar esperar o dobro.
- O teto real da VRAM é **7.367 MiB**, não 8.192 — o Windows e o driver consomem o resto. Isso define quantas camadas de um modelo maior cabem na GPU.

## O que os números dizem

- **A GPU vence nas duas fases**, mas por margens diferentes: ~2,7× no prefill e ~2,2× no decode.
- **20 tok/s de decode** é confortável para uso interativo. **9 tok/s na CPU** é utilizável, mas no limite da paciência.
- **A CPU não é inútil.** Para um modelo 7B, ela entrega respostas em tempo real se você aceitar esperar o dobro.
- O teto real da VRAM é **7.367 MiB**, não 8.192 — o Windows e o driver consomem o resto. Isso define quantas camadas de um modelo maior cabem na GPU.

## Próximos passos

- [ ] Testar um modelo MoE (~30B) no modo híbrido GPU+CPU, para medir onde os dois colaboram.
- [ ] Medir TTFT (time-to-first-token) separadamente do throughput.
- [ ] Adicionar um modelo denso maior (13B) para encontrar o ponto em que a GPU deixa de caber.