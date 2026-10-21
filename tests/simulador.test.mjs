import test from "node:test";
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";
import { simular, igc, DEFAULTS, TRAMOS, SIS, ATEP_SANNA } from "../assets/simulador.js";

const UTA = 834504;
const AFP_UNO = 0.0046;

// Los ejemplos de la guía (README, "Declaración anual") y el cálculo de la librería
// tax-cl configurada para la Operación Renta 2026 coinciden en estos IGC.
test("IGC del ejemplo 1 (base $16.800.000)", () => {
  assert.equal(Math.round(igc(16_800_000, UTA)), 221_368);
});

test("IGC del ejemplo 2 (gastos topados en 15 UTA)", () => {
  const base = 60_000_000 - 15 * UTA;
  assert.equal(Math.round(igc(base, UTA)), 2_663_206);
});

test("exento hasta 13,5 UTA", () => {
  assert.equal(igc(13.5 * UTA, UTA), 0);
  assert.equal(igc(5_000_000, UTA), 0);
});

test("cotizaciones del ejemplo (cobertura total, AFP Uno)", () => {
  const r = simular({ mensual: 2_000_000, retencion: 0.145, cobertura: 1, comision: AFP_UNO }, DEFAULTS);
  assert.equal(Math.round(r.cotizaciones), 3_736_320); // AFP 2.008.320 + salud 1.344.000 + SIS 2% 384.000
  assert.equal(Math.round(r.impuesto), 221_368);
  assert.equal(Math.round(r.retenido), 3_480_000);
});

test("cobertura parcial cotiza menos que la total", () => {
  const total = simular({ mensual: 2_000_000, retencion: 0.1525, cobertura: 1, comision: AFP_UNO });
  const parcial = simular({ mensual: 2_000_000, retencion: 0.1525, cobertura: 0.8, comision: AFP_UNO });
  assert.ok(parcial.cotizaciones < total.cotizaciones);
});

test("el tope de 90 UF limita la base imponible", () => {
  const alto = simular({ mensual: 20_000_000, retencion: 0.1525, cobertura: 1, comision: AFP_UNO }, { uf: 40_000, uta: UTA });
  const tope = 90 * 12 * 40_000;
  const esperado = tope * (0.1 + AFP_UNO + 0.07) + tope * SIS;
  assert.equal(Math.round(alto.cotizaciones), Math.round(esperado));
});

test("resultado = retenido - cotizaciones - impuesto", () => {
  const r = simular({ mensual: 3_500_000, retencion: 0.16, cobertura: 1, comision: AFP_UNO });
  assert.ok(Math.abs(r.resultado - (r.retenido - r.cotizaciones - r.impuesto)) < 1e-6);
});

test("ATEP y SANNA suman 0,93% de la renta imponible cuando se incluyen", () => {
  const base = { mensual: 2_000_000, retencion: 0.1525, cobertura: 1, comision: AFP_UNO };
  const sin = simular(base);
  const con = simular({ ...base, atep: true });
  assert.equal(Math.round(con.cotizaciones - sin.cotizaciones), Math.round(24_000_000 * 0.8 * ATEP_SANNA));
});

// El README es la fuente de la guía: su tabla de tramos debe coincidir con el simulador.
test("los tramos del README coinciden con TRAMOS", () => {
  const readme = readFileSync(new URL("../README.md", import.meta.url), "utf8");
  const filas = [...readme.matchAll(/^\| ([\d,]+) \| ([\d,]+|y más) \| [\d.]+ \| ([\d.]+|—) \| (exento|[\d,]+) \| ([\d.]+) \|$/gm)];
  assert.equal(filas.length, TRAMOS.length);
  filas.forEach((f, i) => {
    const [hasta, factor, rebaja] = TRAMOS[i];
    const num = (x) => Number(x.replaceAll(".", "").replace(",", "."));
    if (Number.isFinite(hasta)) assert.equal(num(f[2]), hasta);
    assert.equal(f[4] === "exento" ? 0 : num(f[4]), factor);
    assert.ok(Math.abs(num(f[5]) - rebaja * UTA) < 1, `rebaja tramo ${i}: ${f[5]} vs ${rebaja * UTA}`);
  });
});
