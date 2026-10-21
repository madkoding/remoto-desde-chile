# Remoto desde Chile

[![test](https://github.com/madkoding/remoto-desde-chile/actions/workflows/test.yml/badge.svg)](https://github.com/madkoding/remoto-desde-chile/actions/workflows/test.yml)
[![build](https://github.com/madkoding/remoto-desde-chile/actions/workflows/build.yml/badge.svg)](https://github.com/madkoding/remoto-desde-chile/actions/workflows/build.yml)
[![links](https://github.com/madkoding/remoto-desde-chile/actions/workflows/links.yml/badge.svg)](https://github.com/madkoding/remoto-desde-chile/actions/workflows/links.yml)

Guía para desarrolladores que trabajan para el extranjero desde Chile: cómo cobrar, emitir boletas, cotizar y declarar impuestos en 2026. Incluye un simulador de impuestos y cotizaciones.

**Sitio:** https://madkoding.github.io/remoto-desde-chile/

## Qué hay en este repositorio

| Archivo | Para qué sirve |
| ------- | -------------- |
| [`GUIA.md`](GUIA.md) | El contenido de la guía (fuente única) |
| `index.html` | El sitio, generado desde la guía con `build.py` |
| `assets/` | Simulador (`simulador.js`, `calc.js`), parámetros (`params.json`), estilos y fuentes |
| `tests/` | Pruebas del simulador (`node --test`) |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Cómo cambiar contenido y actualizar tasas |

## Cómo se mantiene

- La UF se actualiza sola cada lunes y las tasas con un workflow manual; cada tasa guarda su fecha de verificación y su fuente.
- Cada mes se revisan los enlaces, y en enero y julio se abre un issue para revisar SIS, tope imponible y retención.
- Lo que no se pudo verificar está marcado en la guía y listado, con su estado, en la sección "Pendientes por verificar".

Esta información no constituye asesoramiento legal, financiero ni tributario.
