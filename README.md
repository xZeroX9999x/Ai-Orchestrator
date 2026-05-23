# AI Orchestrator

[![CI](https://github.com/yourname/ai-orchestrator/actions/workflows/ci.yml/badge.svg)](https://github.com/yourname/ai-orchestrator/actions/workflows/ci.yml)
[![Docker](https://github.com/yourname/ai-orchestrator/actions/workflows/docker.yml/badge.svg)](https://github.com/yourname/ai-orchestrator/actions/workflows/docker.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

Sistema autónomo multi-agente sobre **Ollama local**. Detecta el hardware del
equipo, elige el modelo más adecuado y orquesta un pipeline
**Prompt Engineer → Architect** para transformar una idea cruda en un plan
técnico ejecutable.

---

## Características

- 🔎 **Detección real de hardware** — RAM, núcleos, CUDA y VRAM (vía `nvidia-smi`), con soporte para Android (Termux).
- 🧠 **Selección automática de modelo** por tier: `phi3:mini`, `llama3.1:8b`, `llama3.1:70b`.
- 🚀 **Streaming token-a-token** — ves la respuesta en tiempo real.
- 🌐 **Investigación web cacheada** con DuckDuckGo (`ddgs`).
- 🏥 **Health-check** del servidor Ollama antes de fallar a medio camino.
- 🪵 **Logging estructurado**, CLI con argparse, apagado limpio con SIGINT/SIGTERM.
- 🐳 **Docker + compose** listos para producción.
- ✅ **CI completo**: lint, mypy, tests multi-OS y multi-Python, release a PyPI vía OIDC.

---

## Requisitos

- Python **3.11+**
- [Ollama](https://ollama.com) instalado y corriendo (`ollama serve`)
- *(Opcional)* GPU NVIDIA con drivers para auto-detección de VRAM

---

## Instalación

### Desde fuente

```bash
git clone https://github.com/yourname/ai-orchestrator.git
cd ai-orchestrator

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
```

### Con Docker

```bash
docker compose up -d
docker compose run --rm app --idea "tu idea aquí"
```

El compose levanta también un contenedor de Ollama con volumen persistente
para los modelos. Para GPU NVIDIA, descomenta la sección `deploy` en
`docker-compose.yml`.

---

## Uso

### Modo interactivo

```bash
ai-orchestrator
# o
python -m ai_orchestrator
```

### One-shot

```bash
ai-orchestrator --idea "construir un bot de Discord que resuma URLs"
```

### Opciones

```bash
ai-orchestrator --model llama3.1:8b --verbose
ai-orchestrator --help
```

### Variables de entorno

| Variable           | Default                          | Descripción                       |
|--------------------|----------------------------------|-----------------------------------|
| `OLLAMA_BASE_URL`  | `http://localhost:11434/v1`      | URL del servidor Ollama           |

---

## Arquitectura

```
ai_orchestrator/
├── __init__.py          # API pública del paquete
├── __main__.py          # python -m ai_orchestrator
├── cli.py               # argparse + signal handlers + main()
├── config.py            # logging setup + system prompts
├── hardware.py          # HardwareProfile, Tier, detect_hardware
├── ollama_client.py     # OllamaManager: pull, health, chat_stream
├── research.py          # web_research cacheado
├── agents.py            # Agent dataclass
├── orchestrator.py      # Pipeline Prompt-Engineer → Architect
└── py.typed             # PEP 561 — paquete tipado
```

### Tiers de hardware

| Tier         | Condición                              | Modelo         |
|--------------|----------------------------------------|----------------|
| `mobile`     | Android o RAM < 6 GB                   | `phi3:mini`    |
| `low`        | RAM < 16 GB, sin GPU                   | `phi3:mini`    |
| `mid`        | RAM ≥ 16 GB, sin GPU adecuada          | `llama3.1:8b`  |
| `high`       | GPU con VRAM ≥ 12 GB                   | `llama3.1:8b`  |
| `workstation`| GPU con VRAM ≥ 40 GB y RAM ≥ 32 GB     | `llama3.1:70b` |

---

## Desarrollo

```bash
make install-dev         # instala con dependencias de dev
make pre-commit-install  # hooks de pre-commit

make format              # ruff format + autofix
make lint                # ruff check
make type                # mypy
make test                # pytest
make cov                 # tests con coverage HTML
make all                 # format + lint + type + test
```

Comandos Docker:

```bash
make docker-build
make docker-up
make docker-down
```

---

## Releases

Las releases se disparan al pushear un tag `vX.Y.Z`:

```bash
git tag v0.1.0
git push origin v0.1.0
```

El workflow `release.yml` construye sdist + wheel, publica a PyPI vía OIDC
(trusted publisher) y crea la GitHub Release con notas generadas.

---

## Contribuir

Lee [CONTRIBUTING.md](CONTRIBUTING.md). En resumen: rama → tests → `make all` →
PR con plantilla rellena → CI verde → merge.

Reportes de seguridad: ver [SECURITY.md](SECURITY.md).

Historial de cambios: [CHANGELOG.md](CHANGELOG.md).

---

## Licencia

MIT — ver [LICENSE](LICENSE).
