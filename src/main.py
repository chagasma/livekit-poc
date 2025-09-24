import logging
import sys

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, RoomInputOptions, RunContext, function_tool, get_job_context
from livekit.plugins import noise_cancellation

from prompts import INSTRUCTIONS
from sessions import SessionFactory

load_dotenv(".env")

logger = logging.getLogger(__name__)


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=INSTRUCTIONS)

    @function_tool()
    async def end_call(self, context: RunContext) -> dict:
        """Encerra a chamada atual."""
        logger.info("end_call: Iniciando processo de encerramento da chamada")
        try:
            # Primeiro desconecta da room se disponível
            if hasattr(context, "room") and context.room:
                logger.info("end_call: Desconectando da room")
                await context.room.disconnect()
                logger.info("end_call: Room desconectada com sucesso")
            
            # Obtém o job context e chama shutdown
            try:
                job_ctx = get_job_context()
                logger.info("end_call: Chamando shutdown do job context")
                job_ctx.shutdown(reason="Chamada encerrada pelo usuário")
                logger.info("end_call: Shutdown do job context executado")
            except Exception as job_error:
                logger.warning(f"end_call: Não foi possível chamar shutdown do job context: {job_error}")
            
            logger.info("end_call: Chamada encerrada com sucesso")
            return {"status": "success", "message": "Chamada encerrada com sucesso"}
        except Exception as e:
            logger.error(f"end_call: Erro ao encerrar chamada: {str(e)}", exc_info=True)
            return {"status": "error", "message": f"Erro ao encerrar chamada: {str(e)}"}


def get_session_name():
    session_name = "base-stt_llm_tts"

    for i, arg in enumerate(sys.argv):
        if arg.startswith("-") and arg not in [
            "dev",
            "console",
            "download-files",
            "start",
        ]:
            session_name = arg.lstrip("-")
            sys.argv.pop(i)
            break

    return session_name


async def entrypoint(ctx: agents.JobContext):
    logger.info("entrypoint: Iniciando nova sessão")
    session_name = get_session_name()
    logger.info(f"entrypoint: Usando sessão '{session_name}'")
    
    session = SessionFactory.create_session(session_name)

    logger.info("entrypoint: Iniciando sessão do agente")
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    logger.info("entrypoint: Gerando cumprimento inicial")
    await session.generate_reply(instructions="Cumprimente o usuário e ofereça ajuda.")
    logger.info("entrypoint: Sessão iniciada com sucesso")


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
