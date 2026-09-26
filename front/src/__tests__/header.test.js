import { describe, it, expect, beforeEach } from "vitest";
import { initHeader } from "../header.js";

function setScroll(y) {
  Object.defineProperty(window, "scrollY", { value: y, configurable: true, writable: true });
}

describe("initHeader", () => {
  let header, menu, menuBtn;

  beforeEach(() => {
    // Scroll listeners from earlier tests stay on window but point at
    // detached elements, so fresh markup per test keeps tests isolated.
    document.body.innerHTML = `
      <header id="site-header">
        <button id="mobile-menu-btn" aria-expanded="false"></button>
        <div id="mobile-menu" class="max-h-0"></div>
      </header>
    `;
    header = document.getElementById("site-header");
    menu = document.getElementById("mobile-menu");
    menuBtn = document.getElementById("mobile-menu-btn");
    setScroll(0);
  });

  it("keeps the header transparent at the top of the page", () => {
    initHeader();
    expect(header.style.backgroundColor).toBe("transparent");
    expect(header.style.borderBottom).toBe("");
  });

  it("applies a solid background when the page is already scrolled on load", () => {
    setScroll(200);
    initHeader();
    expect(header.style.backgroundColor).not.toBe("transparent");
    expect(header.style.borderBottom).toContain("1px solid");
  });

  it("applies a solid background after scrolling past the threshold", () => {
    initHeader();
    setScroll(51);
    window.dispatchEvent(new Event("scroll"));
    expect(header.style.backgroundColor).not.toBe("transparent");
  });

  it("opens the mobile menu and updates aria-expanded", () => {
    initHeader();
    menuBtn.click();
    expect(menu.classList.contains("max-h-80")).toBe(true);
    expect(menu.classList.contains("max-h-0")).toBe(false);
    expect(menuBtn.getAttribute("aria-expanded")).toBe("true");
  });

  it("applies a solid background when the menu is opened at the top of the page", () => {
    initHeader();
    menuBtn.click();
    expect(header.style.backgroundColor).not.toBe("transparent");
    expect(header.style.borderBottom).toContain("1px solid");
  });

  it("keeps the solid background while the menu is open and scrolled back to top", () => {
    initHeader();
    menuBtn.click();
    setScroll(0);
    window.dispatchEvent(new Event("scroll"));
    expect(header.style.backgroundColor).not.toBe("transparent");
  });

  it("restores transparency when the menu is closed at the top of the page", () => {
    initHeader();
    menuBtn.click();
    menuBtn.click();
    expect(menu.classList.contains("max-h-0")).toBe(true);
    expect(menu.classList.contains("max-h-80")).toBe(false);
    expect(menuBtn.getAttribute("aria-expanded")).toBe("false");
    expect(header.style.backgroundColor).toBe("transparent");
  });

  it("does nothing when the header is missing", () => {
    document.body.innerHTML = "";
    expect(() => initHeader()).not.toThrow();
  });
});
