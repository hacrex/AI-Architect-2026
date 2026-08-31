// AI ARCHITECT 2026 — Minimal Brutalist JS
// No frameworks. No build tools. Just logic.

document.addEventListener('DOMContentLoaded', () => {
  initFilters();
  initNavHighlight();
  initSmoothScroll();
  initModuleExpand();
});

// MODULE FILTER
function initFilters() {
  const buttons = document.querySelectorAll('.filter-btn');
  const cards = document.querySelectorAll('.module-card');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      // Update active state
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.dataset.filter;

      cards.forEach(card => {
        if (filter === 'all' || card.dataset.category === filter) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });
}

// NAV HIGHLIGHT ON SCROLL
function initNavHighlight() {
  const sections = document.querySelectorAll('.section, .hero');
  const navLinks = document.querySelectorAll('.nav-links a');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        navLinks.forEach(link => {
          link.style.borderBottom = link.getAttribute('href') === `#${id}`
            ? '2px solid var(--red)'
            : 'none';
        });
      }
    });
  }, { threshold: 0.3 });

  sections.forEach(section => {
    if (section.id) observer.observe(section);
  });
}

// SMOOTH SCROLL
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        const offset = 80; // Nav height
        const position = target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: position, behavior: 'smooth' });
      }
    });
  });
}

// MODULE EXPAND ON CLICK
function initModuleExpand() {
  const cards = document.querySelectorAll('.module-card');

  cards.forEach(card => {
    card.addEventListener('click', () => {
      // Toggle expanded state
      const isExpanded = card.style.gridColumn === 'span 3';

      // Reset all cards
      cards.forEach(c => {
        c.style.gridColumn = '';
        c.style.zIndex = '';
      });

      // Expand clicked card if it wasn't already
      if (!isExpanded && window.innerWidth > 900) {
        card.style.gridColumn = 'span 3';
        card.style.zIndex = '10';
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });

  // Reset on resize
  window.addEventListener('resize', () => {
    if (window.innerWidth <= 900) {
      cards.forEach(c => {
        c.style.gridColumn = '';
        c.style.zIndex = '';
      });
    }
  });
}

// KEYBOARD NAVIGATION
document.addEventListener('keydown', (e) => {
  // Press 1-9 to jump to module
  if (e.key >= '1' && e.key <= '9') {
    const day = e.key.padStart(2, '0');
    const target = document.getElementById(`day${day}`);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  // Press 0 for day 10
  if (e.key === '0') {
    const target = document.getElementById('day10');
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }
});

// CONSOLE EASTER EGG
console.log(`
%c╔══════════════════════════════════════════╗
║                                          ║
║   AI ARCHITECT 2026                      ║
║   Build Production AI Systems            ║
║                                          ║
║   12 Days. 12 Modules. 12 Working Apps.  ║
║                                          ║
╚══════════════════════════════════════════╝
`, 'color: #ff0000; font-family: monospace; font-size: 14px;');
