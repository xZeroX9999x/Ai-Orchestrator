"""Command-line interface."""

from __future__ import annotations

import argparse
import logging
import signal
import sys

from ai_orchestrator.config import setup_logging
from ai_orchestrator.hardware import detect_hardware, model_for_profile
from ai_orchestrator.ollama_client import OllamaError, OllamaManager
from ai_orchestrator.orchestrator import Orchestrator

log = logging.getLogger(__name__)


def _install_signal_handlers() -> None:
    """Ctrl+C / SIGTERM apagado limpio."""
    def _handler(_signum, _frame):
        log.info("Señal recibida. Cerrando.")
        sys.exit(0)
    signal.signal(signal.SIGINT, _handler)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, _handler)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="ai-orchestrator",
        description="Autonomous AI Orchestrator (Ollama local)",
    )
    p.add_argument("--model", help="Override del modelo auto-detectado")
    p.add_argument("--idea", help="Modo one-shot con esta idea")
    p.add_argument("--verbose", action="store_true", help="Logs DEBUG")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    setup_logging(verbose=args.verbose)
    _install_signal_handlers()

    profile = detect_hardware()
    model   = args.model or model_for_profile(profile)
    log.info("Modelo seleccionado: %s", model)

    try:
        ollama = OllamaManager(model)
        ollama.ensure_model()
        ollama.health_check()
    except OllamaError as exc:
        log.critical(str(exc))
        return 1

    orch = Orchestrator(ollama)

    if args.idea:
        orch.run_once(args.idea)
        return 0

    print("\n" + "═" * 60)
    print("AI ORCHESTRATOR — sesión interactiva".center(60))
    print("═" * 60)

    while True:
        try:
            raw = input("\n› Idea (o 'salir'): ").strip()
        except EOFError:
            break
        if not raw:
            continue
        if raw.lower() in {"salir", "exit", "quit"}:
            break
        orch.run_once(raw)

    return 0


if __name__ == "__main__":
    sys.exit(main())
