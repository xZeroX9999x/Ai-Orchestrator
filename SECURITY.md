# Política de seguridad

## Versiones soportadas

Solo la última versión menor recibe parches de seguridad.

| Versión | Soporte           |
| ------- | ----------------- |
| 0.1.x   | ✅ activa         |

## Reportar una vulnerabilidad

**No abras un issue público.** Para reportar un fallo de seguridad:

1. Abre un **Security Advisory** privado en GitHub:
   `Security` → `Report a vulnerability`.
2. O envía un correo a: **security@example.com** (sustituye por tu correo).

Incluye:
- Descripción del fallo y su impacto.
- Pasos para reproducirlo.
- Versión afectada.
- Si tienes propuesta de fix, mejor.

Te responderé en **72 horas hábiles**. Si el reporte es válido, coordinamos
una ventana de disclosure responsable antes de hacerlo público.

## Alcance

Este proyecto se comunica con un servidor **Ollama local**. No envía datos
a servicios externos salvo:
- DuckDuckGo (consultas de research).
- El servidor Ollama configurado en `OLLAMA_BASE_URL`.

Cualquier exfiltración no documentada a otros endpoints es un fallo de
seguridad y debe reportarse.
