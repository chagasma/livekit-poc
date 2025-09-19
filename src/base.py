from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    google,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from prompts import INSTRUCTIONS

load_dotenv(".env")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=INSTRUCTIONS)


async def entrypoint(ctx: agents.JobContext):
    if 1 > -1:
        session = AgentSession(
            llm=google.beta.realtime.RealtimeModel(
                model="gemini-2.5-flash-preview-native-audio-dialog",
                voice="Zephyr",
                instructions=INSTRUCTIONS,
            ),
            vad=silero.VAD.load(),
        )
    else:
        session = AgentSession(
            stt=deepgram.STT(model="nova-3", language="multi"),
            llm=openai.LLM(model="gpt-4o-mini"),
            tts=google.beta.GeminiTTS(
                model="gemini-2.5-flash-preview-tts",
                voice_name="Zephyr",
                instructions=INSTRUCTIONS,
            ),
            vad=silero.VAD.load(),
            turn_detection=MultilingualModel()
        )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions="Cumprimente o usuário e ofereça ajuda."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))