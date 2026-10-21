// Simulador referencial. Parámetros: ver README.md ("Paga impuestos, salud y cotizaciones").
// Tabla IGC: Año Tributario 2026 (UTA dic. 2025). Tope imponible ≈ 90 UF mensuales.
const UTA = 834504;
const UF = 40828;
const TOPE_ANUAL = 90 * 12 * UF;
const SIS = 0.0162;
const TRAMOS = [
  [13.5, 0, 0],
  [30, 0.04, 0.54],
  [50, 0.08, 1.74],
  [70, 0.135, 4.49],
  [90, 0.23, 11.14],
  [120, 0.304, 17.8],
  [310, 0.35, 23.32],
  [Infinity, 0.4, 38.82],
];

const igc = (base) => {
  const u = base / UTA;
  for (const [hasta, factor, rebaja] of TRAMOS) {
    if (u <= hasta) return Math.max(0, base * factor - rebaja * UTA);
  }
  return 0;
};

const clp = new Intl.NumberFormat("es-CL", { style: "currency", currency: "CLP", maximumFractionDigits: 0 });
const pct = (n) => (n * 100).toLocaleString("es-CL", { maximumFractionDigits: 2 }) + "%";

export function simular({ mensual, retencion, cobertura, comision }) {
  const anual = mensual * 12;
  const retenido = anual * retencion;
  const imponible = Math.min(anual * 0.8, TOPE_ANUAL);
  const base = imponible * cobertura;
  const afp = base * (0.1 + comision);
  const salud = base * 0.07;
  const sis = imponible * SIS;
  const cotizaciones = afp + salud + sis;
  const gastos = Math.min(anual * 0.3, 15 * UTA);
  const impuesto = igc(anual - gastos);
  const resultado = retenido - cotizaciones - impuesto;
  return { anual, retenido, cotizaciones, impuesto, resultado };
}

const $ = (id) => document.getElementById(id);
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const shown = {};

function tween(el, to) {
  const from = shown[el.id] ?? to;
  shown[el.id] = to;
  if (reduce || from === to) { el.textContent = clp.format(to); return; }
  const t0 = performance.now();
  const dur = 260;
  const step = (t) => {
    const k = Math.min(1, (t - t0) / dur);
    el.textContent = clp.format(from + (to - from) * (1 - Math.pow(1 - k, 3)));
    if (k < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

function render() {
  const mensual = Math.max(0, Number($("mensual").value.replace(/\D/g, "")) || 0);
  const r = simular({
    mensual,
    retencion: Number($("retencion").value),
    cobertura: Number($("cobertura").value),
    comision: Number($("afp").value),
  });
  tween($("o-retenido"), r.retenido);
  tween($("o-cot"), r.cotizaciones);
  tween($("o-igc"), r.impuesto);
  tween($("o-res"), Math.abs(r.resultado));
  $("o-res-label").textContent = r.resultado >= 0 ? "Te devolverían" : "Tendrías que pagar";
  $("o-res-box").classList.toggle("owe", r.resultado < 0);
  $("o-anual").textContent = "Ingreso anual " + clp.format(r.anual);
  $("o-tasa").textContent = "Impuesto efectivo " + pct(r.anual ? r.impuesto / r.anual : 0);
}

const input = $("mensual");
input.addEventListener("input", () => {
  const digits = input.value.replace(/\D/g, "");
  input.value = digits ? Number(digits).toLocaleString("es-CL") : "";
  render();
});
["retencion", "cobertura", "afp"].forEach((id) => $(id).addEventListener("change", render));
render();

// Navegación lateral: marca la sección visible.
const links = [...document.querySelectorAll(".rail nav a")];
const targets = links.map((a) => document.getElementById(a.hash.slice(1))).filter(Boolean);
const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      links.forEach((a) => a.setAttribute("aria-current", String(a.hash === "#" + e.target.id)));
    });
  },
  { rootMargin: "-20% 0px -70% 0px" }
);
targets.forEach((t) => io.observe(t));
