"""Orquestador del pipeline Prompt-Engineer → Architect."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from ai_orchestrator.agents import Agent
from ai_orchestrator.config import (
    ARCHITECT_SYSTEM,
    DEFAULT_RESEARCH_TOPIC,
    PROMPT_ENGINEER_SYSTEM,
)
from ai_orchestrator.ollama_client import OllamaManager
from ai_orchestrator.research import web_research

log = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """Salida estructurada del pipeline."""
    master_prompt: str
    plan: str


class Orchestrator:
    """Coordina los agentes y la búsqueda web."""

    def __init__(
        self,
        ollama: OllamaManager,
        research_topic: str = DEFAULT_RESEARCH_TOPIC,
    ) -> None:
        self.ollama = ollama
        self.research_topic = research_topic

    def run_once(self, raw_idea: str) -> PipelineResult:
        """Ejecuta el pipeline completo para una idea cruda."""
        research = web_research(self.research_topic)

        engineer = Agent(
            name="Prompt Engineer",
            system_prompt=PROMPT_ENGINEER_SYSTEM.format(research=research),
            ollama=self.ollama,
            temperature=0.6,
        )
        architect = Agent(
            name="Architect",
            system_prompt=ARCHITECT_SYSTEM,
            ollama=self.ollama,
            temperature=0.2,
        )

        master_prompt = engineer.run(f"Idea cruda: {raw_idea}")
        plan          = architect.run(master_prompt)
        return PipelineResult(master_prompt=master_prompt, plan=plan)
