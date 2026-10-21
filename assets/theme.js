// Tema claro/oscuro: respeta la preferencia del sistema hasta que la persona elige uno.
(function () {
  var root = document.documentElement;
  try { var saved = localStorage.getItem("theme"); if (saved === "light" || saved === "dark") root.dataset.theme = saved; } catch (e) {}
  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.getElementById("theme");
    if (!btn) return;
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    var current = function () { return root.dataset.theme || (mq.matches ? "dark" : "light"); };
    var sync = function () { btn.setAttribute("aria-pressed", String(current() === "dark")); };
    btn.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("theme", next); } catch (e) {}
      sync();
    });
    mq.addEventListener("change", sync);
    sync();
  });
})();
