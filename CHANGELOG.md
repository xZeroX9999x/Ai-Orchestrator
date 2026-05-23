# Changelog

Todos los cambios notables se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

### Added
- (nada todavía)

## [0.1.0] - 2026-05-22

### Added
- Detección de hardware (RAM, VRAM real vía `nvidia-smi`, CUDA, Android).
- Selección automática de modelo Ollama según tier del equipo.
- `OllamaManager` con `ensure_model`, `health_check` y `chat_stream`.
- Investigación web cacheada con DDG.
- Pipeline multi-agente Prompt Engineer → Architect.
- CLI con argparse, modo one-shot e interactivo.
- Tests unitarios con mocks.
- Dockerfile multi-stage y `docker-compose.yml` con Ollama.
- CI con GitHub Actions: lint, mypy, tests en Linux/macOS/Windows.
- Workflow de release con publicación a PyPI vía OIDC.
- Dependabot y pre-commit hooks.

[Unreleased]: https://github.com/yourname/ai-orchestrator/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourname/ai-orchestrator/releases/tag/v0.1.0
