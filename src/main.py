import sys
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, RoomInputOptions
from livekit.plugins import noise_cancellation
from sessions import SessionFactory
from prompts import INSTRUCTIONS

load_dotenv(".env")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=INSTRUCTIONS)


def get_session_name():
    session_name = "base-native-audio"
    
    for i, arg in enumerate(sys.argv):
        if arg.startswith('-') and not arg in ['dev', 'console', 'download-files', 'start']:
            session_name = arg.lstrip('-')
            sys.argv.pop(i)
            break
    
    return session_name


async def entrypoint(ctx: agents.JobContext):
    session_name = get_session_name()
    session = SessionFactory.create_session(session_name)

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