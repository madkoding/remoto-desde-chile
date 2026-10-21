// Lógica pura del simulador (sin DOM), para poder probarla con `node --test`.
// Parámetros: ver README.md ("Paga impuestos, salud y cotizaciones").
// Tabla IGC: Año Tributario 2026 (UTA dic. 2025). Tope imponible: 90 UF mensuales.
// La UF de referencia se actualiza en assets/params.json (workflow update-uf).
export const DEFAULTS = { uf: 41189.24, uta: 834504 };
export const TOPE_UF_MENSUAL = 90;
export const SIS = 0.02; // vigente desde las remuneraciones de julio 2026
export const ATEP_SANNA = 0.0093; // opcional; tasa referencial (0,90% + 0,03%), sin verificar con fuente oficial
export const TRAMOS = [
  [13.5, 0, 0],
  [30, 0.04, 0.54],
  [50, 0.08, 1.74],
  [70, 0.135, 4.49],
  [90, 0.23, 11.14],
  [120, 0.304, 17.8],
  [310, 0.35, 23.32],
  [Infinity, 0.4, 38.82],
];

export const igc = (base, uta = DEFAULTS.uta) => {
  const u = base / uta;
  for (const [hasta, factor, rebaja] of TRAMOS) {
    if (u <= hasta) return Math.max(0, base * factor - rebaja * uta);
  }
  return 0;
};

export function simular({ mensual, retencion, cobertura, comision, atep = false }, { uf, uta } = DEFAULTS) {
  const anual = mensual * 12;
  const retenido = anual * retencion;
  const imponible = Math.min(anual * 0.8, TOPE_UF_MENSUAL * 12 * uf);
  const base = imponible * cobertura;
  const afp = base * (0.1 + comision);
  const salud = base * 0.07;
  const sis = imponible * SIS;
  const extra = atep ? imponible * ATEP_SANNA : 0;
  const cotizaciones = afp + salud + sis + extra;
  const gastos = Math.min(anual * 0.3, 15 * uta);
  const impuesto = igc(anual - gastos, uta);
  const resultado = retenido - cotizaciones - impuesto;
  return { anual, retenido, cotizaciones, impuesto, resultado };
}
