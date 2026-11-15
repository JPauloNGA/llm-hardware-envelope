# Diário de uso real

Registro de uma sessão de uso do LLM como assistente de texto, sem voz. O objetivo é registrar a qualidade subjetiva das respostas e a latência percebida, complementando os benchmarks quantitativos.

## Configuração

- LLM: Qwen 2.5 0.5B Q4_K_M em `llama-server` (CPU, `-ngl 0`, 28 threads)
- Contexto: 2048 tokens, `cache_prompt: true`
- Temperatura: 0 (greedy)
- Max tokens: 120

## As 5 perguntas

### 1. Factual

- **Prompt:** "What is the capital of Australia?"
- **Resposta:** "The capital of Australia is Canberra."
- **Latência:** 2.264 ms (cold start do servidor)
- **Útil?** Sim, acertou.
- **Observação:** surpreendeu — modelos de 0.5B costumam errar fatos. O Qwen 2.5 0.5B acertou.

### 2. Raciocínio aritmético

- **Prompt:** "If I have three apples and give away one, how many do I have?"
- **Resposta:** "You have two apples."
- **Latência:** 133 ms
- **Útil?** Sim, direto e correto.

### 3. Explicação curta

- **Prompt:** "Explain in two sentences why the sky is blue."
- **Resposta:** "The sky is blue because of the scattering of sunlight by tiny particles in the Earth's atmosphere."
- **Latência:** 315 ms
- **Útil?** Sim, mas a resposta tem **uma** frase, não duas. O modelo ignorou a instrução de "two sentences". Limitação de instrução.

### 4. Pergunta aberta

- **Prompt:** "Tell me something interesting."
- **Resposta:** "Sure! Here's an interesting fact: The tallest building in the world is the Burj Khalifa in Dubai, United Arab Emirates, which stands at 828 meters (2,717 feet) tall."
- **Latência:** 679 ms
- **Útil?** Sim, fato correto e bem formatado.

### 5. Código

- **Prompt:** "Write a Python function that reverses a string."
- **Resposta:** `def reverse_string(s): return s[::-1]`
- **Latência:** 266 ms
- **Útil?** Sim, idiomático e correto.

## O que funcionou bem

- O Qwen 0.5B é **mais capaz do que o tamanho sugere** para perguntas curtas e comuns.
- A latência com o servidor quente é excelente (133–679 ms), bem abaixo da meta de 1 s.
- O prefix caching funciona: as perguntas 2–5 foram rápidas porque o system prompt já estava em cache.

## O que não funcionou

- **Instruções compostas são ignoradas.** "Explain in two sentences" gerou uma frase. O modelo de 0.5B não segue instruções de formato com confiabilidade.
- **O cold start de 2.264 ms** é perceptível. Manter o servidor sempre no ar resolve, mas consome RAM.

## Decisões para o futuro

- Para perguntas factuais e código simples, o Qwen 0.5B é suficiente.
- Para instruções de formato (listas, número de frases, tom específico), um modelo maior (Mistral 7B na GPU) seria mais confiável.
- O diário de voz (`assistant.py`) fica como demonstração separada; este diário cobre o uso como assistente de texto.