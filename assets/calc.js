// Interfaz del simulador. La lógica vive en simulador.js.
import { simular, DEFAULTS } from "./simulador.js";

let params = { ...DEFAULTS };

const clp = new Intl.NumberFormat("es-CL", { style: "currency", currency: "CLP", maximumFractionDigits: 0 });
const pct = (n) => (n * 100).toLocaleString("es-CL", { maximumFractionDigits: 2 }) + "%";

const $ = (id) => document.getElementById(id);
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const shown = {};

// Pinta el valor y su "fantasma" (todos los segmentos encendidos) para el display apagado.
function put(el, n) {
  const t = clp.format(n);
  el.textContent = t;
  el.dataset.ghost = t.replace(/[^.,\s\u00a0]/g, "~");
}

function tween(el, to) {
  const from = shown[el.id] ?? to;
  shown[el.id] = to;
  if (reduce || from === to) { put(el, to); return; }
  const t0 = performance.now();
  const dur = 260;
  const step = (t) => {
    const k = Math.min(1, (t - t0) / dur);
    put(el, from + (to - from) * (1 - Math.pow(1 - k, 3)));
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
    atep: $("atep").value === "1",
  }, params);
  tween($("o-retenido"), r.retenido);
  tween($("o-cot"), r.cotizaciones);
  tween($("o-igc"), r.impuesto);
  tween($("o-res"), Math.abs(r.resultado));
  $("o-res-label").textContent = r.resultado >= 0 ? "Te devolverían" : "Tendrías que pagar";
  $("o-res-box").classList.toggle("owe", r.resultado < 0);
  $("o-anual").textContent = "Ingreso anual " + clp.format(r.anual);
  $("o-tasa").textContent = "Impuesto efectivo " + pct(r.anual ? r.impuesto / r.anual : 0);
}

// UF de referencia: la actualiza un workflow en assets/params.json; si falla, se usa el valor por defecto.
fetch("assets/params.json", { cache: "no-cache" })
  .then((r) => (r.ok ? r.json() : null))
  .then((p) => {
    if (p && p.uf > 0) { params = { ...params, uf: p.uf }; }
    const el = $("o-uf");
    if (el) el.textContent = clp.format(params.uf) + (p && p.fecha ? " al " + p.fecha.split("-").reverse().join("-") : "");
    render();
  })
  .catch(() => {});

const input = $("mensual");
input.addEventListener("input", () => {
  const digits = input.value.replace(/\D/g, "");
  input.value = digits ? Number(digits).toLocaleString("es-CL") : "";
  render();
});
["retencion", "cobertura", "afp", "atep"].forEach((id) => $(id).addEventListener("change", render));
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
