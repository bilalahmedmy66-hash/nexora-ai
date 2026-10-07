import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import CommandPalette from "./CommandPalette";

function setup() {
  const usersRun = vi.fn();
  const darkRun = vi.fn();
  const onClose = vi.fn();
  render(
    <CommandPalette
      onClose={onClose}
      commands={[
        { id: "users", label: "Go to Users", run: usersRun },
        { id: "dark", label: "Use dark theme", run: darkRun },
      ]}
    />,
  );
  return { usersRun, darkRun, onClose, user: userEvent.setup() };
}

describe("CommandPalette", () => {
  it("focuses the search box and lists every command", () => {
    setup();
    expect(screen.getByRole("combobox", { name: "Search commands" })).toHaveFocus();
    expect(screen.getAllByRole("option")).toHaveLength(2);
  });

  it("filters as you type and runs the match on Enter", async () => {
    const { user, darkRun, onClose } = setup();
    await user.type(screen.getByRole("combobox"), "dark");
    expect(screen.getAllByRole("option")).toHaveLength(1);
    await user.keyboard("{Enter}");
    expect(onClose).toHaveBeenCalled();
    expect(darkRun).toHaveBeenCalled();
  });

  it("moves the selection with the arrow keys", async () => {
    const { user, usersRun, darkRun } = setup();
    await user.keyboard("{ArrowDown}{Enter}");
    expect(darkRun).toHaveBeenCalled();
    expect(usersRun).not.toHaveBeenCalled();
  });

  it("shows an empty message when nothing matches", async () => {
    const { user } = setup();
    await user.type(screen.getByRole("combobox"), "zzz");
    expect(screen.getByText("No matching commands.")).toBeInTheDocument();
  });

  it("closes on Escape", async () => {
    const { user, onClose } = setup();
    await user.keyboard("{Escape}");
    expect(onClose).toHaveBeenCalled();
  });
});
