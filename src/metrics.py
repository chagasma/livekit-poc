import logging
from typing import Any

from livekit.agents import metrics

logger = logging.getLogger(__name__)


class MetricsCollector:
    def __init__(self):
        self.usage_collector = metrics.UsageCollector()

    def log_metrics(self, metrics_data: Any) -> None:
        try:
            metrics.log_metrics(metrics_data)

            self.usage_collector.collect(metrics_data)

            self._log_detailed_metrics(metrics_data)

        except Exception as e:
            logger.error(f"Erro ao logar métricas: {e}", exc_info=True)

    def _log_detailed_metrics(self, metrics_data: Any) -> None:
        if hasattr(metrics_data, "stt"):
            self._log_stt_metrics(metrics_data.stt)

        if hasattr(metrics_data, "llm"):
            self._log_llm_metrics(metrics_data.llm)

        if hasattr(metrics_data, "tts"):
            self._log_tts_metrics(metrics_data.tts)

        if hasattr(metrics_data, "eou"):
            self._log_eou_metrics(metrics_data.eou)

    def _log_stt_metrics(self, stt: Any) -> None:
        logger.info(
            f"STT Metrics - Duração áudio: {stt.audio_duration:.2f}s, "
            f"Tempo transcrição: {stt.transcription_time:.2f}s"
        )

    def _log_llm_metrics(self, llm: Any) -> None:
        ttft = llm.ttft if hasattr(llm, "ttft") else 0
        tokens_per_sec = (
            llm.tokens_per_second if hasattr(llm, "tokens_per_second") else 0
        )

        logger.info(
            f"LLM Metrics - TTFT: {ttft:.3f}s, "
            f"Tokens: {llm.total_tokens} (prompt: {llm.prompt_tokens}, completion: {llm.completion_tokens}), "
            f"Tokens/s: {tokens_per_sec:.1f}, "
            f"Duração: {llm.duration:.2f}s"
        )

    def _log_tts_metrics(self, tts: Any) -> None:
        ttfb = tts.ttfb if hasattr(tts, "ttfb") else 0

        logger.info(
            f"TTS Metrics - TTFB: {ttfb:.3f}s, "
            f"Caracteres: {tts.characters}, "
            f"Duração áudio: {tts.audio_duration:.2f}s, "
            f"Tempo geração: {tts.generation_time:.2f}s"
        )

    def _log_eou_metrics(self, eou: Any) -> None:
        logger.info(
            f"EOU Metrics - Delay: {eou.end_of_utterance_delay:.3f}s, "
            f"Tempo transcrição: {eou.transcription_delay:.3f}s"
        )

    def get_usage_summary(self) -> dict:
        try:
            summary = self.usage_collector.get_summary()
            logger.info(f"Resumo de uso: {summary}")
            return summary
        except Exception as e:
            logger.error(f"Erro ao obter resumo de uso: {e}", exc_info=True)
            return {}

    def calculate_total_latency(self, metrics_data: Any) -> float:
        try:
            eou_delay = (
                metrics_data.eou.end_of_utterance_delay
                if hasattr(metrics_data, "eou")
                else 0
            )
            llm_ttft = metrics_data.llm.ttft if hasattr(metrics_data, "llm") else 0
            tts_ttfb = metrics_data.tts.ttfb if hasattr(metrics_data, "tts") else 0

            total = eou_delay + llm_ttft + tts_ttfb
            logger.info(
                f"Latência total: {total:.3f}s (EOU: {eou_delay:.3f}s + "
                f"LLM TTFT: {llm_ttft:.3f}s + TTS TTFB: {tts_ttfb:.3f}s)"
            )
            return total
        except Exception as e:
            logger.error(f"Erro ao calcular latência total: {e}", exc_info=True)
            return 0.0
