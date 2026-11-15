# Experimentos do `llm_study`

Estes dados vêm do repositório satélite [llm_study](https://github.com/JPauloNGA/llm_study) e complementam o estudo principal. Eles respondem à pergunta: **dentro do envelope de hardware, qual modelo e qual configuração escolher?**

| Arquivo | O que mede | Conexão com o estudo principal |
|---|---|---|
| `kv_caching.csv` | Latência com e sem cache de contexto | Complementa o prefix caching: o cache reduz a latência em todos os modelos testados |
| `quantizacao.csv` | Q4 vs Q8 (tamanho e velocidade) | Explica por que Q4_K_M é a escolha padrão: 9% mais rápido e 40% menor |
| `idioma.csv` | PT-BR vs EN (tokens e tempo) | Inglês gera 28% menos tokens; respostas em inglês são mais rápidas |
| `modelos.csv` | Qwen 1.5B vs Llama 3.2 1B | Qwen 1.5B é ~80% mais rápido e mantém qualidade aceitável |
| `roteador.csv` | Roteamento de especialistas | Versão factível do LD-MoLE: classificador + especialistas por categoria |

## O que cada experimento prova

### KV Caching

A segunda pergunta no mesmo contexto levou **0,32 s** — quase metade do tempo da pergunta isolada (0,58 s), mesmo com um prompt **5× maior** (253 vs 47 tokens). Isso confirma o achado do projeto principal: o cache de contexto é a alavanca mais importante para interação em tempo real.

### Quantização

O Q4 é **~9% mais rápido** e ocupa **quase metade do espaço** do Q8. Para hardware limitado como a RX 580, o Q4 é a escolha ideal.

### Idioma

O modelo gerou **28% menos tokens** em inglês para a mesma tarefa, e o tempo total foi **28% menor**. Em cenários de alto volume, isso representa uma economia significativa.

### Modelos

O **Qwen 2.5 1.5B** foi ~80% mais rápido que o Llama 3.2 1B (39,64 vs 22,11 t/s), apesar de ter mais parâmetros. O tamanho do modelo não é o único fator de velocidade: arquitetura e otimização do backend influenciam significativamente.

### Roteador

O classificador (Qwen 1.5B) decide a categoria em ~2,3 s, e o especialista responde em 7–24 s dependendo da categoria. O roteamento funciona, mas o tempo de classificação é significativo — em um assistente de tempo real, ele precisaria ser mais rápido ou cacheado.
