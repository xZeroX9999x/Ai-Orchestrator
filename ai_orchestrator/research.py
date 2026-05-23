"""Investigación web cacheada (DuckDuckGo)."""

from __future__ import annotations

import logging
from functools import lru_cache

try:
    from ddgs import DDGS                              # paquete moderno
except ImportError:                                    # pragma: no cover
    from duckduckgo_search import DDGS                 # fallback legacy

log = logging.getLogger(__name__)


@lru_cache(maxsize=32)
def web_research(topic: str, max_results: int = 3) -> str:
    """Devuelve un resumen breve de los top-N resultados de DDG.

    Cacheado en memoria por (topic, max_results) para no repetir tráfico.
    """
    log.info("Buscando en web: %s", topic)
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(topic, max_results=max_results))
    except Exception as exc:
        log.warning("Búsqueda web falló: %s", exc)
        return f"(offline: {exc})"

    if not results:
        return "(sin resultados)"
    return "\n".join(
        f"- {r.get('title', '')}: {r.get('body', '')}" for r in results
    )
