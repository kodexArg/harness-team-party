---
name: gj-sk-reporte
title: Reportes HTML mobile-first de baja verbosidad (castellano)
type: skill
status: active
version: v0.1.0
tags: [skill, report, mobile, diagram-design, castellano]
description: >
  Idéntico a gj-sk-report: convierte un resumen markdown dado en UN HTML oscuro
  self-contained, mobile-first y de baja verbosidad. Diagramas vía diagram-design
  (SVG embed), no Mermaid CDN. Entrega en castellano. Usar ante "reporte",
  "resumen en html", "para el celular/WhatsApp", o /gj-sk-reporte. Reemplaza
  kskill-report en español.
---

# gj-sk-reporte

Skill **idéntico** a [`gj-sk-report`](../gj-sk-report/SKILL.md). Misma
arquitectura, mismos templates (`references/` y `scripts/` son symlinks al
canónico), misma pipeline, mismos gates.

**Única diferencia:** el artefacto se entrega en **castellano** (rioplatense
cuando encaje: *vos*, *mandá*, *acá*). Ver [voice.md](references/voice.md).

## Responsibility

**Un trabajo:** markdown → HTML en este formato fijo.

> Fuente por defecto = última respuesta del asistente si no hay markdown/archivo.
> El contenido explícito del mismo turno gana. No re-resumir desde cero salvo
> pedido. Si no hay respuesta previa ni markdown, preguntá una vez y pará.

## Non-negotiables

1. **Mobile-first**
2. **Baja verbosidad** (salvo pedido explícito: verbose / largo / completo / full)
3. **diagram-design** para visuales — [diagram-bridge.md](references/diagram-bridge.md)
4. Espíritu **kskill-report** + shell en [shell.css](references/shell.css)

## Pipeline

Igual que `gj-sk-report`:

1. Leer shell + voice.
2. Tomar markdown (o última respuesta); comprimir.
3. Diagramas → diagram-design → embed SVG.
4. Elegir template → rellenar.
5. Gate:

```bash
python3 skills/gj-sk-report/scripts/validate_report.py <artifact.html>
```

(o vía el symlink `skills/gj-sk-reporte/scripts/…`)

6. Guardar siempre en `~/Documents/gj-sk-report/<slug>-YYYYMMDD.html`.
7. Auto-Telegram salvo "no lo mandes" / "solo local" (`kskill-send-to-telegram`).

`lang="es"` en el `<html>` del artefacto. Kickers y copy en castellano.

## Template mapping

| Intención | Template |
|---|---|
| estado / progreso | `status.html` |
| concepto + pasos + figura | `concept.html` |
| dos opciones | `comparison.html` |
| comparación con tabs | `comparison-interactive.html` |
| un número que importa | `stat.html` |
| decisión + por qué breve | `decision.html` |

## Self-check

Igual que el gemelo EN, más: prosa en castellano, sin mezclar idiomas salvo que
la fuente ya lo haga.
