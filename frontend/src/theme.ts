export type Theme = "light" | "dark" | "system";
const KEY = "nexora.theme";

export function getTheme(): Theme {
  try { const v = localStorage.getItem(KEY); return v === "light" || v === "dark" ? v : "system"; } catch { return "system"; }
}
export function applyTheme(t: Theme) {
  const r = document.documentElement;
  if (t === "system") r.removeAttribute("data-theme"); else r.setAttribute("data-theme", t);
}
export function setTheme(t: Theme) {
  try { localStorage.setItem(KEY, t); } catch { /* storage unavailable */ }
  applyTheme(t);
}
