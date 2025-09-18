from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, RoomInputOptions
from livekit.plugins import noise_cancellation
from sessions import SessionFactory

load_dotenv(".env")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="Você é uma assistente de IA prestativa.")


async def entrypoint(ctx: agents.JobContext):
    session = SessionFactory.create_session("realtime")

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
