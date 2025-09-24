import sys
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, RoomInputOptions, RunContext, function_tool
from livekit.plugins import noise_cancellation
from sessions import SessionFactory
from prompts import INSTRUCTIONS

load_dotenv(".env")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=INSTRUCTIONS)
    
    @function_tool()
    async def end_call(self, context: RunContext) -> dict:
        """Encerra a chamada atual."""
        try:
            if hasattr(context, 'room') and context.room:
                await context.room.disconnect()
            return {"status": "success", "message": "Chamada encerrada com sucesso"}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao encerrar chamada: {str(e)}"}


def get_session_name():
    session_name = "base-native-audio"
    
    for i, arg in enumerate(sys.argv):
        if arg.startswith('-') and arg not in ['dev', 'console', 'download-files', 'start']:
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