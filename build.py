#!/usr/bin/env python3
"""Genera index.html a partir de README.md (fuente única de la guía).

Uso: python3 build.py   (requiere: pip install markdown)
"""
import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
SRC = ROOT / "README.md"
OUT = ROOT / "index.html"
UPSTREAM = "https://github.com/devschile/remoto-desde-chile"
REPO = "https://github.com/madkoding/remoto-desde-chile"

TEMPLATE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Remoto desde Chile</title>
<meta name="description" content="Guía práctica para desarrolladores que trabajan remoto desde Chile: cómo cobrar, emitir boletas, cotizar y declarar impuestos en 2026.">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#f2f7fb">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Michroma&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div class="shell">
  <aside class="rail">
    <a class="brand" href="#top">Remoto<br>desde <span>Chile</span></a>
    <nav aria-label="Secciones">
__NAV__
    </nav>
    <p class="meta">Actualizada en octubre 2026.<br><a href="__REPO__">Código y contribuciones</a></p>
  </aside>
  <main id="top">
    <header class="hero">
      <h1>Cobra en dólares, cotiza y declara en Chile.</h1>
      <p class="lead">Guía para desarrolladores que trabajan para el extranjero desde Chile. Las cifras de 2026 vienen del SII y de Previsión Social; lo que no pudimos verificar está marcado.</p>
      <section class="calc" aria-labelledby="calc-title">
        <div class="calc-head">
          <h2 id="calc-title">Simula tu año</h2>
          <p>Estimación referencial, no reemplaza tu declaración.</p>
        </div>
        <div class="fields">
          <div class="field">
            <label for="mensual">Ingreso bruto mensual (CLP)</label>
            <input id="mensual" inputmode="numeric" autocomplete="off" value="2.000.000">
          </div>
          <div class="field">
            <label for="retencion">Retención de la boleta</label>
            <select id="retencion">
              <option value="0.145">2025 · 14,5%</option>
              <option value="0.1525" selected>2026 · 15,25%</option>
              <option value="0.16">2027 · 16%</option>
              <option value="0.17">2028 · 17%</option>
            </select>
          </div>
          <div class="field">
            <label for="cobertura">Cobertura de salud y pensión</label>
            <select id="cobertura">
              <option value="1" selected>Total (100%)</option>
              <option value="0.8">Parcial (80%)</option>
            </select>
          </div>
          <div class="field">
            <label for="afp">Comisión de tu AFP</label>
            <select id="afp">
              <option value="0.0046" selected>AFP Uno · 0,46%</option>
              <option value="0.0145">Provida · 1,45%</option>
            </select>
          </div>
        </div>
        <dl class="readouts" aria-live="polite">
          <div class="readout"><dt>Retenido en boletas</dt><dd id="o-retenido">$0</dd><small id="o-anual"></small></div>
          <div class="readout"><dt>Cotizaciones estimadas</dt><dd id="o-cot">$0</dd><small>AFP, salud y SIS</small></div>
          <div class="readout"><dt>Impuesto global complementario</dt><dd id="o-igc">$0</dd><small id="o-tasa"></small></div>
          <div class="readout result" id="o-res-box"><dt id="o-res-label">Te devolverían</dt><dd id="o-res">$0</dd></div>
        </dl>
        <p class="calc-note">Usa la tabla del Año Tributario 2026, gastos presuntos del 30% (tope 15 UTA) y un tope imponible de 90 UF mensuales. Excluye ATEP, SANNA y otros créditos.</p>
      </section>
      <p class="disclaimer">__DISCLAIMER__</p>
    </header>
    <article>
__BODY__
    </article>
    <footer>
      <p>Basada en <a href="__UPSTREAM__">devschile/remoto-desde-chile</a>, un trabajo colaborativo de la comunidad. ¿Falta un dato o está desactualizado? <a href="__REPO__">Abre un pull request</a>.</p>
      <p>Para más preguntas, pásate por el canal #remoto del Slack de <a href="https://devschile.cl/">devschile</a>.</p>
    </footer>
  </main>
</div>
<script type="module" src="assets/calc.js"></script>
</body>
</html>
"""


def main():
    text = SRC.read_text(encoding="utf-8")

    # Separa la introducción (título, aviso) del cuerpo.
    head, body = text.split("\n## ", 1)
    body = "## " + body
    disclaimer = "Ninguno de nosotros es abogado, ni asesor financiero o tributario. Esta información no constituye asesoramiento de ningún tipo; consulta con un profesional."

    body = body.replace("- [ ] ", "- ")
    body = re.sub(r"(?m)^  - ", "    - ", body)  # listas anidadas: python-markdown pide 4 espacios
    body = body.replace("(CONTRIBUTING.md)", f"({UPSTREAM}/blob/master/CONTRIBUTING.md)")

    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"],
                           extension_configs={"toc": {"permalink": False}})
    out = md.convert(body)

    # Tablas con scroll horizontal; enlaces externos en pestaña nueva.
    out = re.sub(r"<table>", '<div class="scroll"><table>', out)
    out = out.replace("</table>", "</table></div>")
    out = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', out)

    short = {
        "paga-impuestos-salud-y-cotizaciones": "Impuestos y cotizaciones",
        "stock-optionsrsus": "Stock options y RSUs",
        "creditos-con-bancos-hipotecario-de-consumo-etc": "Créditos bancarios",
        "tengo-mas-preguntas": "Más preguntas",
    }
    nav = "\n".join(
        f'      <a href="#{t["id"]}">{html.escape(short.get(t["id"], t["name"]))}</a>'
        for t in md.toc_tokens if t["level"] == 2
    )

    page = (TEMPLATE.replace("__NAV__", nav).replace("__BODY__", out)
            .replace("__DISCLAIMER__", disclaimer).replace("__REPO__", REPO).replace("__UPSTREAM__", UPSTREAM))
    OUT.write_text(page, encoding="utf-8")
    print(f"index.html: {len(page):,} bytes, {len(md.toc_tokens)} secciones")


if __name__ == "__main__":
    main()
