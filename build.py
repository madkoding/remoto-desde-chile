#!/usr/bin/env python3
"""Genera index.html a partir de GUIA.md (fuente única de la guía).

Uso: python3 build.py   (requiere: pip install markdown)
"""
import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
SRC = ROOT / "GUIA.md"
OUT = ROOT / "index.html"
REPO = "https://github.com/madkoding/remoto-desde-chile"

ICONS = {'search': '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>', 'coin': '<circle cx="12" cy="12" r="9.5"/><path d="M12 6.5v11M15 9.5c0-1.2-1.3-2-3-2s-3 .8-3 2 1.3 1.7 3 2 3 .8 3 2-1.3 2-3 2-3-.8-3-2"/>', 'wallet': '<rect x="3" y="6" width="18" height="14" rx="2"/><path d="M3 10h18M16 15h2"/>', 'bank': '<path d="M3 21h18M5 21V10M9.5 21V10M14.5 21V10M19 21V10M12 3l9 5H3z"/>', 'trend': '<path d="m3 17 6-6 4 4 8-8M15 7h6v6"/>', 'home': '<path d="m3 11 9-8 9 8M5 10v10h14V10M10 20v-6h4v6"/>', 'help': '<circle cx="12" cy="12" r="9.5"/><path d="M9.5 9.2a2.6 2.6 0 1 1 3.6 2.4c-.7.4-1.1 1-1.1 1.8M12 17h.01"/>', 'check': '<path d="m9 11 3 3 8-8M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h9"/>', 'book': '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>', 'calc': '<rect x="5" y="2.5" width="14" height="19" rx="2"/><path d="M8.5 6.5h7M8.5 11h.01M12 11h.01M15.5 11h.01M8.5 15h.01M12 15h.01M15.5 15h.01M8.5 18.5h.01M12 18.5h3.5"/>', 'brief': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>', 'clip': '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4h6v3H9zM9 12h6M9 16h4"/>', 'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>', 'swap': '<path d="M4 8h15l-4-4M20 16H5l4 4"/>', 'phone': '<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18.5h2"/>', 'globe': '<circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19M12 2.5c3 3 3 16 0 19M12 2.5c-3 3-3 16 0 19"/>', 'send': '<path d="m21 3-9.5 9.5M21 3l-6.5 18-3-8.5L3 9.5z"/>', 'file': '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>', 'cal': '<rect x="3.5" y="5" width="17" height="16" rx="2"/><path d="M8 3v4M16 3v4M3.5 10h17"/>', 'shield': '<path d="M12 3 4.5 6v5.5c0 4.5 3.2 8.2 7.5 9.5 4.3-1.3 7.5-5 7.5-9.5V6z"/><path d="m9 12 2.2 2.2L15.5 10"/>', 'list': '<path d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01"/>', 'star': '<path d="m12 3 2.8 5.8 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.3l1.1-6.2L3 9.7l6.2-.9z"/>'}

# Icono por título: primera clave que aparezca en el id (h2 y h3).
ICON_FOR = [
    ("encuentra-trabajo", "search"), ("cuanto-cobro", "coin"), ("recibe-tu-sueldo", "wallet"),
    ("paga-impuestos", "bank"), ("stock-options", "trend"), ("creditos-con-bancos", "home"),
    ("pendientes", "check"), ("fuentes", "book"),
    ("formas-de-trabajo", "brief"), ("preparacion", "clip"), ("donde-encontrar", "pin"),
    ("wise", "swap"), ("otras-alternativas", "phone"), ("cuenta-en-el-extranjero", "globe"),
    ("transferencia-bancaria", "send"), ("emision-de-boletas", "file"), ("impuestos-mensuales", "cal"),
    ("cotizaciones", "shield"), ("declaracion-anual", "clip"), ("como-calculan", "calc"),
    ("que-cosas-te-piden", "list"), ("que-cosas-puedes", "star"),
]


def icon(name):
    return ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
            + ICONS[name] + "</svg>")


def add_icons(out):
    def sub(m):
        tag, hid, rest = m.group(1), m.group(2), m.group(3)
        name = next((n for k, n in ICON_FOR if k in hid), "list")
        return f'<{tag} id="{hid}">{icon(name)}<span>{rest}</span></{tag}>'
    return re.sub(r'<(h[23]) id="([^"]+)">(.*?)</\1>', sub, out)


TEMPLATE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Remoto desde Chile</title>
<meta name="description" content="Guía práctica para desarrolladores que trabajan remoto desde Chile: cómo cobrar, emitir boletas, cotizar y declarar impuestos en 2026.">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#161a1e" media="(prefers-color-scheme: dark)">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CL">
<meta property="og:title" content="Remoto desde Chile">
<meta property="og:description" content="Cobra en dólares, cotiza y declara en Chile. Guía 2026 con simulador de impuestos y cotizaciones.">
<meta property="og:url" content="https://madkoding.github.io/remoto-desde-chile/">
<meta property="og:image" content="https://madkoding.github.io/remoto-desde-chile/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="assets/fonts/michroma-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/barlow-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<script src="assets/theme.js"></script>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div class="shell">
  <aside class="rail">
    <a class="brand" href="#top">Remoto<br>desde <span>Chile</span></a>
    <nav aria-label="Secciones">
__NAV__
    </nav>
    <button class="theme" type="button" id="theme" aria-label="Cambiar entre tema claro y oscuro">
      <svg class="ico sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8"/></svg>
      <svg class="ico moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>
      <span>Tema</span>
    </button>
    <p class="meta">Actualizada en octubre 2026.<br><a href="__REPO__">Código y contribuciones</a></p>
  </aside>
  <main id="top">
    <header class="hero">
      <h1>Cobra en dólares, cotiza y declara en Chile.</h1>
      <p class="lead">Guía para desarrolladores que trabajan para el extranjero desde Chile. Las cifras de 2026 vienen del SII y de Previsión Social; lo que no pudimos verificar está marcado.</p>
      <section class="calc" aria-labelledby="calc-title">
        <div class="calc-head">
          <h2 id="calc-title">__CALCICON__<span>Simula tu año</span></h2>
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
          <div class="field">
            <label for="atep">ATEP y SANNA (sin verificar)</label>
            <select id="atep">
              <option value="0" selected>No incluir</option>
              <option value="1">Incluir · 0,93%</option>
            </select>
          </div>
        </div>
        <dl class="readouts" aria-live="polite">
          <div class="readout"><dt>Retenido en boletas</dt><dd id="o-retenido">$0</dd><small id="o-anual"></small></div>
          <div class="readout"><dt>Cotizaciones estimadas</dt><dd id="o-cot">$0</dd><small>AFP, salud y SIS</small></div>
          <div class="readout"><dt>Impuesto global complementario</dt><dd id="o-igc">$0</dd><small id="o-tasa"></small></div>
          <div class="readout result" id="o-res-box"><dt id="o-res-label">Te devolverían</dt><dd id="o-res">$0</dd></div>
        </dl>
        <p class="calc-note">Usa la tabla del Año Tributario 2026, gastos presuntos del 30% (tope 15 UTA) y un tope imponible de 90 UF mensuales (UF de referencia: <span id="o-uf">$41.189</span>). Por defecto excluye ATEP, SANNA y otros créditos.</p>
        <p class="calc-note calc-verif" id="o-verif" aria-label="Estado de verificación de los parámetros"></p>
      </section>
      <p class="disclaimer">__DISCLAIMER__</p>
    </header>
    <article>
__BODY__
    </article>
    <footer>
      <p>¿Falta un dato o está desactualizado? <a href="__REPO__">Abre un pull request</a>.</p>
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
    body = body.replace("(CONTRIBUTING.md)", f"({REPO}/blob/main/CONTRIBUTING.md)")

    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"],
                           extension_configs={"toc": {"permalink": False}})
    out = add_icons(md.convert(body))
    out = re.sub(r"<strong>Sin verificar:</strong>", '<span class="unv">Sin verificar</span>', out)
    out = re.sub(r"<td>(Verificado|Parcial|Pendiente)</td>",
                 lambda m: f'<td><span class="st st-{m.group(1).lower()}">{m.group(1)}</span></td>', out)

    # Tablas con scroll horizontal; enlaces externos en pestaña nueva.
    out = re.sub(r"<table>", '<div class="scroll"><table>', out)
    out = out.replace("</table>", "</table></div>")
    out = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', out)

    short = {
        "paga-impuestos-salud-y-cotizaciones": "Impuestos y cotizaciones",
        "stock-optionsrsus": "Stock options y RSUs",
        "creditos-con-bancos-hipotecario-de-consumo-etc": "Créditos bancarios",
    }
    nav = "\n".join(
        f'      <a href="#{t["id"]}">{html.escape(short.get(t["id"], t["name"]))}</a>'
        for t in md.toc_tokens if t["level"] == 2
    )

    page = (TEMPLATE.replace("__NAV__", nav).replace("__BODY__", out)
            .replace("__DISCLAIMER__", disclaimer).replace("__CALCICON__", icon("calc")).replace("__REPO__", REPO))
    OUT.write_text(page, encoding="utf-8")
    print(f"index.html: {len(page):,} bytes, {len(md.toc_tokens)} secciones")


if __name__ == "__main__":
    main()
