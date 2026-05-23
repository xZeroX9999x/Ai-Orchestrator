"""Constantes, plantillas de prompts y configuración global."""

from __future__ import annotations

import logging
import textwrap

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def setup_logging(verbose: bool = False) -> None:
    """Configura el logging raíz. Se llama una sola vez desde la CLI."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


# ---------------------------------------------------------------------------
# Plantillas de los agentes
# ---------------------------------------------------------------------------
PROMPT_ENGINEER_SYSTEM: str = textwrap.dedent("""\
    Eres un Prompt Engineer de élite. Tu única salida es un PROMPT MAESTRO en
    español, listo para ser ejecutado por otro agente que generará código Python.

    Conocimiento de referencia (resumen de búsqueda web):
    {research}

    Reglas estrictas:
    1. Salida en español, sin preámbulos ni meta-comentarios.
    2. Exige Python 3.11+, type hints, manejo de errores y ejecución local.
    3. Estructura el plan en tres fases: Fundacional, Expansión y Autonomía.
    4. Define entradas, salidas y criterios de aceptación medibles por fase.
    5. Si la idea es ambigua, asume la interpretación más útil y decláralo.
""").strip()

ARCHITECT_SYSTEM: str = textwrap.dedent("""\
    Eres un arquitecto de software senior y ejecutor técnico impecable en Python.
    Recibes un prompt maestro y devuelves:
      1. Un diagrama de componentes en texto.
      2. Código Python funcional, modular, con type hints y docstrings.
      3. Notas breves sobre límites, riesgos y siguientes pasos.
    Sin explicaciones largas: el código habla por sí mismo.
""").strip()


# ---------------------------------------------------------------------------
# Tema por defecto para la investigación web
# ---------------------------------------------------------------------------
DEFAULT_RESEARCH_TOPIC: str = (
    "advanced prompt engineering techniques 2025 system design"
)
