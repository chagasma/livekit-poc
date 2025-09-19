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

### test-elevenlabs-tts

```cmd
STT: Deepgram Nova-3 (multilingual)
LLM: GPT-4o-mini
TTS: ElevenLabs Flash v2.5 (voice: EXAVITQu4vr4xnSDxMaL)
VAD: Silero
Turn Detection: Multilingual
```

**Resultados:**

- ❌ **STT inconsistente para português** - transcrições imprecisas
- ✅ **Reasoning forte** - excelente capacidade de raciocínio
- ✅ **Execução de tools eficiente** - boa performance com ferramentas
- ✅ **Qualidade de TTS excelente** - melhor TTS testado

### test-openai-tts

```cmd
STT: Deepgram Nova-3 (português)
LLM: GPT-4o-mini
TTS: OpenAI GPT-4o-mini-TTS (voice: ash)
VAD: Silero
Turn Detection: Multilingual
```

**Resultados:**

- ❌ **STT com problemas** - nova-3 com limitações para português
- ✅ **Reasoning forte** - excelente capacidade de raciocínio
- ✅ **Execução de tools eficiente** - boa performance com ferramentas
- ⚠️ **Qualidade de TTS boa** - melhor que Gemini, inferior ao ElevenLabs

### test-gpt-4o-transcribe-stt

```cmd
STT: OpenAI GPT-4o-transcribe
LLM: GPT-4o-mini
TTS: Gemini 2.5 Flash TTS (Zephyr)
VAD: Silero
Turn Detection: Multilingual
```

**Resultados:**

- ✅ **STT excelente para português** - melhor qualidade de transcrição testada
- ✅ **Reasoning forte** - excelente capacidade de raciocínio
- ✅ **Execução de tools eficiente** - boa performance com ferramentas
- ❌ **Qualidade de TTS mediana** - voz menos natural

## Resumo Comparativo

| Aspecto | base-native-audio | base-stt_llm_tts | test-elevenlabs-tts | test-openai-tts | test-gpt-4o-transcribe-stt |
|---------|-------------------|-------------------|---------------------|-----------------|----------------------------|
| Qualidade de Voz | Excelente | Mediana | **Excelente** | Boa | Mediana |
| Reasoning | Limitado | Forte | Forte | Forte | Forte |
| Tool Execution | Deficiente | Eficiente | Eficiente | Eficiente | Eficiente |
| STT Português | N/A (nativo) | Inconsistente | Inconsistente | Problemas | **Excelente** |
