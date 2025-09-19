from livekit.agents import AgentSession
from livekit.plugins import (
    openai,
    google,
    deepgram,
    silero,
    elevenlabs,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from prompts import INSTRUCTIONS


class SessionFactory:
    SESSIONS = {
        "base-native-audio": {
            "llm": lambda: google.beta.realtime.RealtimeModel(
                model="gemini-2.5-flash-preview-native-audio-dialog",
                voice="Zephyr",
                instructions=INSTRUCTIONS,
            ),
            "vad": lambda: silero.VAD.load(),
        },
        "base-stt_llm_tts": {
            "stt": lambda: deepgram.STT(model="nova-3", language="multi"),
            "llm": lambda: openai.LLM(model="gpt-4o-mini"),
            "tts": lambda: google.beta.GeminiTTS(
                model="gemini-2.5-flash-preview-tts",
                voice_name="Zephyr",
                instructions=INSTRUCTIONS,
            ),
            "vad": lambda: silero.VAD.load(),
            "turn_detection": lambda: MultilingualModel()
        },
        "test-elevenlabs-tts": {
            "stt": lambda: deepgram.STT(model="nova-3", language="multi"),
            "llm": lambda: openai.LLM(model="gpt-4o-mini"),
            "tts": lambda: elevenlabs.TTS(
                model="flash",
                voice="echo"
            ),
            "vad": lambda: silero.VAD.load(),
            "turn_detection": lambda: MultilingualModel()
        },
        "test-openai-tts": {
            "stt": lambda: deepgram.STT(model="nova-3", language="multi"),
            "llm": lambda: openai.LLM(model="gpt-4o-mini"),
            "tts": lambda: openai.TTS(
                model="gpt-4o-mini-tts",
                voice="ash",
                instructions=INSTRUCTIONS
            ),
            "vad": lambda: silero.VAD.load(),
            "turn_detection": lambda: MultilingualModel()
        }
    }

    @staticmethod
    def create_session(session_name: str) -> AgentSession:
        if session_name not in SessionFactory.SESSIONS:
            raise ValueError(f"Session '{session_name}' not found. Available: {list(SessionFactory.SESSIONS.keys())}")

        config = SessionFactory.SESSIONS[session_name]
        kwargs = {}

        for key, factory in config.items():
            kwargs[key] = factory()

        return AgentSession(**kwargs)
