"""Agente genérico que envuelve un `OllamaManager` con un system prompt."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from ai_orchestrator.ollama_client import OllamaManager

log = logging.getLogger(__name__)


@dataclass
class Agent:
    """Combina un system prompt con un cliente Ollama y una temperatura."""

    name: str
    system_prompt: str
    ollama: OllamaManager
    temperature: float = 0.4

    def run(self, user_message: str) -> str:
        """Ejecuta el agente imprimiendo la respuesta en streaming."""
        print(f"\n──── {self.name} ────")
        buffer: list[str] = []
        for token in self.ollama.chat_stream(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user",   "content": user_message},
            ],
            temperature=self.temperature,
        ):
            print(token, end="", flush=True)
            buffer.append(token)
        print()
        return "".join(buffer).strip()
