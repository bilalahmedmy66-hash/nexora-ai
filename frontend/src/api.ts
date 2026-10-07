const BASE = "/api/v1";
const KEY = "nexora.tokens";

export type Role = "admin" | "manager" | "member" | "viewer";
export interface User { id: number; email: string; full_name: string; role: Role; is_active: boolean; created_at: string; last_login_at: string | null }
export interface Me extends User { permissions: string[] }
export interface Page<T> { items: T[]; total: number; page: number; page_size: number }
type Tokens = { access_token: string; refresh_token: string };

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string, public details: { field: string; message: string }[] = []) {
    super(message);
  }
}

export const tokens = {
  get(): Tokens | null { try { return JSON.parse(localStorage.getItem(KEY) || "null"); } catch { return null; } },
  set(t: Tokens) { try { localStorage.setItem(KEY, JSON.stringify(t)); } catch { /* storage unavailable */ } },
  clear() { try { localStorage.removeItem(KEY); } catch { /* storage unavailable */ } },
};

async function refresh(): Promise<boolean> {
  const t = tokens.get();
  if (!t) return false;
  const res = await fetch(`${BASE}/auth/refresh`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ refresh_token: t.refresh_token }) });
  if (!res.ok) return false;
  tokens.set(await res.json());
  return true;
}

export async function api<T>(path: string, init: { method?: string; body?: unknown } = {}, canRetry = true): Promise<T> {
  const t = tokens.get();
  let res: Response;
  try {
    res = await fetch(BASE + path, {
      method: init.method ?? "GET",
      headers: { "Content-Type": "application/json", ...(t ? { Authorization: `Bearer ${t.access_token}` } : {}) },
      body: init.body === undefined ? undefined : JSON.stringify(init.body),
    });
  } catch {
    throw new ApiError(0, "network_error", "Cannot reach the server. Check that the API is running.");
  }
  if (res.status === 401 && canRetry && t && path !== "/auth/login") {
    if (await refresh()) return api<T>(path, init, false);
    tokens.clear();
    window.dispatchEvent(new Event("nexora:logout"));
  }
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    const e = data?.error;
    throw new ApiError(res.status, e?.code ?? "error", e?.message ?? "Something went wrong.", e?.details ?? []);
  }
  return data as T;
}
