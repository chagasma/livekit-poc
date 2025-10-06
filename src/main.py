import logging

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import (
    Agent,
    MetricsCollectedEvent,
    RoomInputOptions,
    RunContext,
    function_tool,
    get_job_context,
)
from livekit.plugins import noise_cancellation

from metrics import MetricsCollector
from prompts import INSTRUCTIONS
from sessions import SessionFactory

load_dotenv(".env")

logger = logging.getLogger(__name__)


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=INSTRUCTIONS)

    @function_tool()
    async def end_call(self, context: RunContext) -> dict:
        logger.info("end_call: Iniciando processo de encerramento da chamada")
        try:
            if hasattr(context, "room") and context.room:
                logger.info("end_call: Desconectando da room")
                await context.room.disconnect()
                logger.info("end_call: Room desconectada com sucesso")

            try:
                job_ctx = get_job_context()
                logger.info("end_call: Chamando shutdown do job context")
                job_ctx.shutdown(reason="Chamada encerrada pelo usuário")
                logger.info("end_call: Shutdown do job context executado")
            except Exception as job_error:
                logger.warning(
                    f"end_call: Não foi possível chamar shutdown do job context: {job_error}"
                )

            logger.info("end_call: Chamada encerrada com sucesso")
            return {"status": "success", "message": "Chamada encerrada com sucesso"}
        except Exception as e:
            logger.error(f"end_call: Erro ao encerrar chamada: {str(e)}", exc_info=True)
            return {"status": "error", "message": f"Erro ao encerrar chamada: {str(e)}"}


def get_session_name():
    return "base-stt_llm_tts"


async def entrypoint(ctx: agents.JobContext):
    logger.info("Iniciando nova sessão")
    session = SessionFactory.create_session(get_session_name())

    metrics_collector = MetricsCollector()

    @session.on("metrics_collected")
    def on_metrics_collected(ev: MetricsCollectedEvent):
        metrics_collector.log_metrics(ev.metrics)
        metrics_collector.calculate_total_latency(ev.metrics)

    logger.info("Iniciando sessão do agente")
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(instructions="Cumprimente o usuário e ofereça ajuda.")

    ctx.add_shutdown_callback(lambda: metrics_collector.get_usage_summary())


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
