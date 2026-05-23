"""Cliente Ollama: gestión del modelo, health check y chat por streaming."""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
from dataclasses import dataclass, field
from typing import Iterator, Optional

from openai import APIConnectionError, APIError, OpenAI

log = logging.getLogger(__name__)


def _default_base_url() -> str:
    """`OLLAMA_BASE_URL` env var con fallback a localhost."""
    return os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")


@dataclass
class OllamaConfig:
    """Parámetros de conexión al servidor local de Ollama."""

    base_url: str = field(default_factory=_default_base_url)
    api_key: str  = "ollama"          # ignorada por Ollama, requerida por OpenAI SDK
    timeout: float = 120.0


class OllamaError(RuntimeError):
    """Error de alto nivel del cliente Ollama."""


class OllamaManager:
    """Gestiona descarga, verificación y comunicación con Ollama."""

    def __init__(self, model: str, cfg: Optional[OllamaConfig] = None) -> None:
        self.model = model
        self.cfg = cfg or OllamaConfig()
        self.client = OpenAI(
            base_url=self.cfg.base_url,
            api_key=self.cfg.api_key,
            timeout=self.cfg.timeout,
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    @staticmethod
    def _require_cli() -> None:
        if shutil.which("ollama") is None:
            raise OllamaError(
                "Ollama no está instalado. Descárgalo en https://ollama.com"
            )

    def ensure_model(self) -> None:
        """Descarga el modelo si no está disponible (match exacto)."""
        self._require_cli()
        log.info("Comprobando modelo '%s'…", self.model)
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=False,
        )
        installed = {
            line.split()[0]
            for line in result.stdout.splitlines()[1:]   # ignora cabecera
            if line.strip()
        }
        if self.model not in installed:
            log.info("Descargando '%s' (puede tardar)…", self.model)
            subprocess.run(["ollama", "pull", self.model], check=True)
        log.info("Modelo '%s' listo.", self.model)

    def health_check(self) -> None:
        """Verifica que el servidor de Ollama esté escuchando."""
        try:
            self.client.models.list()
        except APIConnectionError as exc:
            raise OllamaError(
                f"No se puede contactar Ollama en {self.cfg.base_url}. "
                "¿Lo arrancaste con `ollama serve`?"
            ) from exc

    # ------------------------------------------------------------------
    # Chat
    # ------------------------------------------------------------------
    def chat_stream(self, messages: list[dict], temperature: float = 0.4
                    ) -> Iterator[str]:
        """Genera la respuesta token a token."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            for chunk in response:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
        except APIError as exc:
            log.error("Fallo de la API de Ollama: %s", exc)
