import { applyTheme, getTheme, setTheme } from "./theme";

describe("theme", () => {
  it("defaults to system", () => {
    expect(getTheme()).toBe("system");
  });

  it("sets and remembers an explicit dark theme", () => {
    setTheme("dark");
    expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
    expect(getTheme()).toBe("dark");
  });

  it("removes the attribute for system so the OS setting applies", () => {
    setTheme("light");
    setTheme("system");
    expect(document.documentElement.hasAttribute("data-theme")).toBe(false);
    expect(getTheme()).toBe("system");
  });

  it("applyTheme does not persist anything", () => {
    applyTheme("dark");
    expect(localStorage.getItem("nexora.theme")).toBeNull();
  });
});
