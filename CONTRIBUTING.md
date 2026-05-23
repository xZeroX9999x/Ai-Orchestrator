# Contribuir a AI Orchestrator

Gracias por tu interés en contribuir. Estas son las reglas del juego.

## Setup de desarrollo

```bash
git clone https://github.com/yourname/ai-orchestrator.git
cd ai-orchestrator

python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate

make install-dev
make pre-commit-install
```

## Flujo de trabajo

1. Abre un issue antes de empezar para cambios grandes — alineamos enfoque.
2. Crea una rama: `git checkout -b feat/nombre-corto` o `fix/nombre-corto`.
3. Programa con tests. Si añades una feature sin test, será rechazada.
4. Ejecuta la suite local antes de hacer push:
   ```bash
   make all      # format + lint + type + test
   ```
5. Commits con [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat: añadir soporte para Mistral`
   - `fix: corregir match de modelo en ensure_model`
   - `docs: aclarar requisitos de VRAM`
   - `refactor: extraer cliente HTTP`
6. Push y abre PR contra `main`. Rellena la plantilla.
7. CI debe estar en verde antes de merge.

## Estilo de código

- **Python 3.11+**, type hints obligatorios en código nuevo.
- **Ruff** para lint y formato.
- **Mypy** para tipos.
- Docstrings estilo Google o NumPy, consistentes con el archivo.
- Nada de `print` en código de librería — usa `logging`. Los `print` solo
  pueden aparecer en la CLI y en el método `Agent.run` (streaming UX).

## Tests

- Usamos `pytest`. Los tests viven en `tests/`.
- Para componentes con efectos externos (Ollama, red, subprocess) usa mocks.
- Apunta a una cobertura razonable; no es una obsesión, pero código nuevo
  sin tests no se mergea.

## Reportar un fallo de seguridad

No abras un issue público. Lee [SECURITY.md](SECURITY.md).
