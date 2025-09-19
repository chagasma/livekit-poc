# Análise de Performance - LiveKit Agent

## Configurações Implementadas

### base-native-audio

```cmd
LLM: Gemini 2.5 Flash Native Audio Dialog
Voice: Zephyr
VAD: Silero
```

**Resultados:**

- ✅ **Qualidade de voz excelente** - áudio natural e fluido
- ❌ **Reasoning limitado** - performance inferior em raciocínio complexo
- ❌ **Execução de tools deficiente** - falhas na utilização de ferramentas

### base-stt_llm_tts

```cmd
STT: Deepgram Nova-3 (multilingual)
LLM: GPT-4o-mini
TTS: Gemini 2.5 Flash TTS (Zephyr)
VAD: Silero
Turn Detection: Multilingual
```

**Resultados:**

- ❌ **STT inconsistente para português** - transcrições imprecisas
- ✅ **Reasoning forte** - excelente capacidade de raciocínio
- ✅ **Execução de tools eficiente** - boa performance com ferramentas
- ❌ **Qualidade de TTS mediana** - voz menos natural

## Resumo Comparativo

| Aspecto | base-native-audio | base-stt_llm_tts |
|---------|-------------------|-------------------|
| Qualidade de Voz | Excelente | Mediana |
| Reasoning | Limitado | Forte |
| Tool Execution | Deficiente | Eficiente |
| STT Português | N/A (nativo) | Inconsistente |
