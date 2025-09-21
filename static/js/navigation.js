/**
 * Professional Navigation (click-only indicator)
 * - Indicator moves for: initial load, click, resize (desktop only)
 * - No movement on hover
 * - /viewmore* path maps to /candidates
 */

document.addEventListener('DOMContentLoaded', initNav);

function initNav() {
  const links = Array.from(document.querySelectorAll('.nav-a'));
  const indicator = document.getElementById('nav-indicator');
  if (!links.length || !indicator) return;

  // Set active from current URL
  const active = findLinkForPath(window.location.pathname, links) || links[0];
  setActiveLink(active, links);
  if (isDesktop()) moveIndicatorTo(active);

  // Click: set active + move pill, then navigate
  links.forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('#')) return;

      e.preventDefault();            // set state first for a crisp UX
      setActiveLink(link, links);
      if (isDesktop()) moveIndicatorTo(link);

      // Navigate
      window.location.href = href;
    });

    // IMPORTANT: no hover movement — removed mouseenter/leave handlers
  });

  // On resize, keep pill under the active link (desktop only)
  window.addEventListener('resize', () => {
    const current = document.querySelector('.nav-a.is-active');
    if (current && isDesktop()) moveIndicatorTo(current);
  });
}

function isDesktop() {
  return window.innerWidth >= 768;
}

function normalizePath(p) {
  if (!p) return '/';
  const noHash = p.split('#')[0];
  const noQuery = noHash.split('?')[0];
  let clean = noQuery;
  if (clean !== '/' && clean.endsWith('/')) clean = clean.slice(0, -1);
  return clean || '/';
}

// Map detail pages to a nav item (e.g., /viewmore -> /candidates)
function aliasPath(p) {
  const n = normalizePath(p);
  if (n.startsWith('/viewmore')) return '/candidates';
  return n;
}

function findLinkForPath(pathname, links) {
  const target = aliasPath(pathname);
  return links.find(a => normalizePath(new URL(a.getAttribute('href'), location.origin).pathname) === target);
}

function setActiveLink(activeLink, links) {
  links.forEach(a => {
    a.classList.remove('is-active', 'text-black');
    a.classList.add('text-gray-700');
  });
  activeLink.classList.add('is-active', 'text-black');
  activeLink.classList.remove('text-gray-700');
}

function moveIndicatorTo(el) {
  const indicator = document.getElementById('nav-indicator');
  const wrapper = el.closest('.relative');
  if (!indicator || !wrapper) return;

  const wr = wrapper.getBoundingClientRect();
  const r  = el.getBoundingClientRect();
  const padX = 12, padY = 4;

  indicator.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
  indicator.style.width  = `${r.width + padX * 2}px`;
  indicator.style.height = `${r.height + padY * 2}px`;
  indicator.style.transform = `translate(${r.left - wr.left - padX}px, ${r.top - wr.top - padY}px)`;
  indicator.style.opacity = '1';
}
