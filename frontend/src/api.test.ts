import { ApiError, api, tokens } from "./api";

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

let fetchMock: ReturnType<typeof vi.fn>;

beforeEach(() => {
  fetchMock = vi.fn();
  vi.stubGlobal("fetch", fetchMock);
  tokens.set({ access_token: "old", refresh_token: "r1" });
});
afterEach(() => vi.unstubAllGlobals());

describe("api client", () => {
  it("refreshes the session once on 401 and retries with the new token", async () => {
    fetchMock
      .mockResolvedValueOnce(json({ error: { code: "unauthorized", message: "Sign in to continue." } }, 401))
      .mockResolvedValueOnce(json({ access_token: "new", refresh_token: "r2", token_type: "bearer" }))
      .mockResolvedValueOnce(json({ ok: true }));

    await expect(api("/users")).resolves.toEqual({ ok: true });

    expect(fetchMock).toHaveBeenCalledTimes(3);
    expect(fetchMock.mock.calls[2][1].headers.Authorization).toBe("Bearer new");
    expect(tokens.get()?.refresh_token).toBe("r2");
  });

  it("signs the user out when the refresh fails", async () => {
    const onLogout = vi.fn();
    window.addEventListener("nexora:logout", onLogout);
    fetchMock
      .mockResolvedValueOnce(json({ error: { code: "unauthorized", message: "Sign in to continue." } }, 401))
      .mockResolvedValueOnce(json({ error: { code: "invalid_token", message: "expired" } }, 401));

    await expect(api("/users")).rejects.toMatchObject({ status: 401 });

    expect(tokens.get()).toBeNull();
    expect(onLogout).toHaveBeenCalled();
    window.removeEventListener("nexora:logout", onLogout);
  });

  it("does not try to refresh a failed login", async () => {
    fetchMock.mockResolvedValueOnce(
      json({ error: { code: "invalid_credentials", message: "Incorrect email or password." } }, 401),
    );
    await expect(api("/auth/login", { method: "POST", body: {} })).rejects.toMatchObject({
      code: "invalid_credentials",
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("turns the API error shape into an ApiError with field details", async () => {
    fetchMock.mockResolvedValueOnce(
      json(
        { error: { code: "validation_error", message: "The request data is invalid.", details: [{ field: "email", message: "bad" }] } },
        422,
      ),
    );
    const err = (await api("/users", { method: "POST", body: {} }).catch((e: unknown) => e)) as ApiError;
    expect(err).toBeInstanceOf(ApiError);
    expect(err.status).toBe(422);
    expect(err.details).toEqual([{ field: "email", message: "bad" }]);
  });

  it("reports a friendly message when the server is unreachable", async () => {
    fetchMock.mockRejectedValueOnce(new TypeError("Failed to fetch"));
    await expect(api("/users")).rejects.toMatchObject({ status: 0, code: "network_error" });
  });
});
