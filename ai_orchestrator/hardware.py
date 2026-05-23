"""Detección de hardware (RAM/VRAM/CUDA/Android) y mapeo a modelos."""

from __future__ import annotations

import logging
import os
import platform
import shutil
import subprocess
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import psutil

log = logging.getLogger(__name__)


class Tier(str, Enum):
    """Nivel de capacidad del hardware."""
    MOBILE       = "mobile"
    LOW          = "low"
    MID          = "mid"
    HIGH         = "high"
    WORKSTATION  = "workstation"


@dataclass(frozen=True)
class HardwareProfile:
    """Snapshot inmutable del hardware del equipo."""

    is_android: bool
    ram_gb: float
    cpu_cores: int
    has_cuda: bool
    vram_gb: Optional[float]
    platform: str

    @property
    def tier(self) -> Tier:
        """Clasifica el hardware en un tier discreto."""
        if self.is_android or self.ram_gb < 6:
            return Tier.MOBILE
        if self.has_cuda and (self.vram_gb or 0) >= 40 and self.ram_gb >= 32:
            return Tier.WORKSTATION
        if self.has_cuda and (self.vram_gb or 0) >= 12:
            return Tier.HIGH
        if self.ram_gb >= 16:
            return Tier.MID
        return Tier.LOW


MODEL_FOR_TIER: dict[Tier, str] = {
    Tier.MOBILE:      "phi3:mini",
    Tier.LOW:         "phi3:mini",
    Tier.MID:         "llama3.1:8b",
    Tier.HIGH:        "llama3.1:8b",
    Tier.WORKSTATION: "llama3.1:70b",
}


def _detect_vram_gb() -> Optional[float]:
    """Lee la VRAM real con nvidia-smi. Devuelve la mayor GPU o None."""
    if not shutil.which("nvidia-smi"):
        return None
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.total",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5, check=True,
        ).stdout
        mibs = [int(x) for x in out.strip().splitlines() if x.strip().isdigit()]
        return max(mibs) / 1024 if mibs else None
    except (subprocess.SubprocessError, ValueError) as exc:
        log.debug("nvidia-smi no devolvió VRAM utilizable: %s", exc)
        return None


def detect_hardware() -> HardwareProfile:
    """Construye un `HardwareProfile` inspeccionando el sistema."""
    profile = HardwareProfile(
        is_android = "ANDROID_ROOT" in os.environ or "ANDROID_STORAGE" in os.environ,
        ram_gb     = psutil.virtual_memory().total / (1024 ** 3),
        cpu_cores  = psutil.cpu_count(logical=False) or psutil.cpu_count() or 1,
        has_cuda   = shutil.which("nvidia-smi") is not None,
        vram_gb    = _detect_vram_gb(),
        platform   = platform.platform(),
    )
    log.info(
        "Hardware: %s | RAM %.1fGB | CPU %d cores | CUDA=%s | VRAM=%s | Tier=%s",
        profile.platform, profile.ram_gb, profile.cpu_cores,
        profile.has_cuda,
        f"{profile.vram_gb:.1f}GB" if profile.vram_gb else "N/A",
        profile.tier.value,
    )
    return profile


def model_for_profile(profile: HardwareProfile) -> str:
    """Devuelve el nombre de modelo Ollama recomendado para el perfil dado."""
    return MODEL_FOR_TIER[profile.tier]
