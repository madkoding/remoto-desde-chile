import test from "node:test";
import assert from "node:assert/strict";
import { simular, igc, DEFAULTS } from "../assets/simulador.js";

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
  assert.equal(Math.round(r.cotizaciones), 3_663_360);
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
  const esperado = tope * (0.1 + AFP_UNO + 0.07) + tope * 0.0162;
  assert.equal(Math.round(alto.cotizaciones), Math.round(esperado));
});

test("resultado = retenido - cotizaciones - impuesto", () => {
  const r = simular({ mensual: 3_500_000, retencion: 0.16, cobertura: 1, comision: AFP_UNO });
  assert.ok(Math.abs(r.resultado - (r.retenido - r.cotizaciones - r.impuesto)) < 1e-6);
});
