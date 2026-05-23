"""Tests del Orchestrator con OllamaManager mockeado."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from ai_orchestrator.orchestrator import Orchestrator, PipelineResult


def _fake_ollama(prompt_engineer_out: str, architect_out: str) -> MagicMock:
    """Devuelve un OllamaManager fake cuyo chat_stream alterna respuestas."""
    fake = MagicMock()
    fake.chat_stream.side_effect = [
        iter([prompt_engineer_out]),
        iter([architect_out]),
    ]
    return fake


@patch("ai_orchestrator.orchestrator.web_research", return_value="(stub)")
def test_run_once_devuelve_pipeline_result(_mock_research):
    fake = _fake_ollama("PROMPT MAESTRO", "PLAN FINAL")
    result = Orchestrator(fake).run_once("una idea")

    assert isinstance(result, PipelineResult)
    assert result.master_prompt == "PROMPT MAESTRO"
    assert result.plan == "PLAN FINAL"
    assert fake.chat_stream.call_count == 2


@patch("ai_orchestrator.orchestrator.web_research", return_value="(stub)")
def test_idea_se_pasa_al_prompt_engineer(_mock_research):
    fake = _fake_ollama("X", "Y")
    Orchestrator(fake).run_once("construir un bot")

    primer_call = fake.chat_stream.call_args_list[0]
    user_msg = primer_call.kwargs["messages"][1]["content"]
    assert "construir un bot" in user_msg
