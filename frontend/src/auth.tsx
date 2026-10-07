import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { api, tokens, type Me } from "./api";

interface AuthState { user: Me | null; loading: boolean; login(email: string, password: string): Promise<void>; logout(): void; can(permission: string): boolean }
const Ctx = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<Me | null>(null);
  const [loading, setLoading] = useState(Boolean(tokens.get()));

  useEffect(() => {
    if (tokens.get()) api<Me>("/auth/me").then(setUser).catch(() => tokens.clear()).finally(() => setLoading(false));
    const onLogout = () => setUser(null);
    window.addEventListener("nexora:logout", onLogout);
    return () => window.removeEventListener("nexora:logout", onLogout);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const t = await api<{ access_token: string; refresh_token: string }>("/auth/login", { method: "POST", body: { email, password } });
    tokens.set(t);
    setUser(await api<Me>("/auth/me"));
  }, []);
  const logout = useCallback(() => { tokens.clear(); setUser(null); }, []);
  const can = useCallback((p: string) => Boolean(user?.permissions.includes(p)), [user]);
  const value = useMemo(() => ({ user, loading, login, logout, can }), [user, loading, login, logout, can]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useAuth() {
  const c = useContext(Ctx);
  if (!c) throw new Error("useAuth must be used inside AuthProvider");
  return c;
}
