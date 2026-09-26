const SCROLL_THRESHOLD = 50;

// Solid background when scrolled or when the mobile menu is open,
// so the menu never sits directly on top of the page content.
export function initHeader(doc = document, win = window) {
  const header = doc.getElementById("site-header");
  const menu = doc.getElementById("mobile-menu");
  const menuBtn = doc.getElementById("mobile-menu-btn");
  if (!header) return;

  let menuOpen = false;

  function updateHeaderStyle() {
    if (win.scrollY > SCROLL_THRESHOLD || menuOpen) {
      header.style.backgroundColor = "color-mix(in oklch, var(--background), transparent 10%)";
      header.style.backdropFilter = "blur(12px)";
      header.style.borderBottom = "1px solid color-mix(in oklch, var(--border), transparent 50%)";
    } else {
      header.style.backgroundColor = "transparent";
      header.style.backdropFilter = "none";
      header.style.borderBottom = "none";
    }
  }

  if (menu && menuBtn) {
    menuBtn.addEventListener("click", () => {
      menuOpen = !menuOpen;
      menu.classList.toggle("max-h-0", !menuOpen);
      menu.classList.toggle("max-h-80", menuOpen);
      menuBtn.setAttribute("aria-expanded", String(menuOpen));
      updateHeaderStyle();
    });
  }

  win.addEventListener("scroll", updateHeaderStyle);
  updateHeaderStyle();
}
