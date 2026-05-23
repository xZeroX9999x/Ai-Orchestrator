# syntax=docker/dockerfile:1.7

# ---------------------------------------------------------------------------
# Stage 1: builder — compila wheels e instala el paquete
# ---------------------------------------------------------------------------
FROM python:3.14-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Copia metadatos primero para aprovechar la caché de capas
COPY pyproject.toml README.md requirements.txt ./
COPY ai_orchestrator ./ai_orchestrator

RUN pip install --upgrade pip build && \
    pip wheel --wheel-dir /wheels .

# ---------------------------------------------------------------------------
# Stage 2: runtime — imagen final mínima
# ---------------------------------------------------------------------------
FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    OLLAMA_BASE_URL=http://ollama:11434/v1

# Usuario no-root
RUN groupadd --system app && \
    useradd  --system --gid app --home /home/app --create-home app

# Instala el paquete desde los wheels pre-construidos
COPY --from=builder /wheels /wheels
RUN pip install --no-index --find-links=/wheels ai-orchestrator && \
    rm -rf /wheels

USER app
WORKDIR /home/app

# Health check ligero — comprueba que el módulo carga sin errores
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import ai_orchestrator; print('ok')" || exit 1

ENTRYPOINT ["ai-orchestrator"]
CMD ["--help"]
