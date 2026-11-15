# Diário de uso real

Registro de uma semana usando o assistente de voz no dia a dia.

## Configuração

- STT: faster-whisper tiny.en (int8, 28 threads)
- LLM: Qwen 2.5 0.5B Q4_K_M em llama-server (CPU, `-ngl 0`)
- TTS: Piper en_US-lessac-medium (Python)
- Áudio de entrada: WAV 16 kHz mono

## O que funcionou bem

- (preencher: ex. latência de ~1 s para perguntas curtas)
- (preencher: ex. o prefix caching deixa o chat responsivo)

## O que não funcionou

- (preencher: ex. o Qwen 0.5B erra fatos; para perguntas factuais, o Mistral 7B na GPU é melhor)
- (preencher: ex. o Whisper tiny confunde palavras com sotaque forte)
- (preencher: ex. o Piper soa robótico; o modelo `medium` é melhor que o `low`)

## Decisões que mudei

- (preencher: ex. troquei o Whisper tiny pelo small para maior robustez)
- (preencher: ex. mantive o Qwen 0.5B só para comandos, e o Mistral 7B para perguntas)

## Próximas melhorias

- (preencher)