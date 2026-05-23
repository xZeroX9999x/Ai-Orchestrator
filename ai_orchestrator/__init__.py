"""AI Orchestrator — sistema autónomo de prompts y arquitectura."""

from ai_orchestrator.agents import Agent
from ai_orchestrator.hardware import HardwareProfile, Tier, detect_hardware
from ai_orchestrator.ollama_client import OllamaConfig, OllamaManager
from ai_orchestrator.orchestrator import Orchestrator

__version__ = "0.1.0"

__all__ = [
    "Agent",
    "HardwareProfile",
    "OllamaConfig",
    "OllamaManager",
    "Orchestrator",
    "Tier",
    "detect_hardware",
    "__version__",
]
