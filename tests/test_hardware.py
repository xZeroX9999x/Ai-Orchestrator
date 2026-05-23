"""Tests del módulo hardware (selección de tier y modelo)."""

from __future__ import annotations

from ai_orchestrator.hardware import (
    MODEL_FOR_TIER,
    HardwareProfile,
    Tier,
    model_for_profile,
)


def _profile(**overrides) -> HardwareProfile:
    defaults = dict(
        is_android=False,
        ram_gb=16.0,
        cpu_cores=8,
        has_cuda=False,
        vram_gb=None,
        platform="test-os",
    )
    defaults.update(overrides)
    return HardwareProfile(**defaults)


def test_android_es_mobile():
    assert _profile(is_android=True, ram_gb=64).tier is Tier.MOBILE


def test_poca_ram_es_mobile():
    assert _profile(ram_gb=4).tier is Tier.MOBILE


def test_workstation_requiere_cuda_y_vram_alta():
    p = _profile(has_cuda=True, vram_gb=48, ram_gb=64)
    assert p.tier is Tier.WORKSTATION


def test_gpu_intermedia_es_high():
    p = _profile(has_cuda=True, vram_gb=16, ram_gb=32)
    assert p.tier is Tier.HIGH


def test_sin_gpu_pero_ram_buena_es_mid():
    assert _profile(ram_gb=16).tier is Tier.MID


def test_sin_gpu_y_poca_ram_es_low():
    assert _profile(ram_gb=8).tier is Tier.LOW


def test_mapping_cubre_todos_los_tiers():
    for tier in Tier:
        assert tier in MODEL_FOR_TIER


def test_model_for_profile_devuelve_modelo_correcto():
    p = _profile(has_cuda=True, vram_gb=48, ram_gb=64)
    assert model_for_profile(p) == MODEL_FOR_TIER[Tier.WORKSTATION]
