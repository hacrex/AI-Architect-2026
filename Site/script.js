// AI ARCHITECT 2026 — Minimal Brutalist JS
// No frameworks. No build tools. Just logic.

const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/hacrex/AI-Architect-2026/main/';

let currentModule = null;
let currentTab = 'notes';

document.addEventListener('DOMContentLoaded', () => {
  initFilters();
  initNavHighlight();
  initSmoothScroll();
  initModuleExpand();
  initModal();
});

// MODULE FILTER
function initFilters() {
  const buttons = document.querySelectorAll('.filter-btn');
  const cards = document.querySelectorAll('.module-card');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
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
        const offset = 80;
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
      const isExpanded = card.style.gridColumn === 'span 3';
      cards.forEach(c => {
        c.style.gridColumn = '';
        c.style.zIndex = '';
      });
      if (!isExpanded && window.innerWidth > 900) {
        card.style.gridColumn = 'span 3';
        card.style.zIndex = '10';
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth <= 900) {
      cards.forEach(c => {
        c.style.gridColumn = '';
        c.style.zIndex = '';
      });
    }
  });
}

// MODAL
function initModal() {
  const overlay = document.getElementById('modalOverlay');
  const closeBtn = document.getElementById('modalClose');
  const tabs = document.querySelectorAll('.modal-tab');
  const cards = document.querySelectorAll('.module-card');

  // Open modal on card click
  cards.forEach(card => {
    card.addEventListener('click', (e) => {
      // Don't open if clicking on expand
      if (card.style.gridColumn === 'span 3') return;

      currentModule = card;
      currentTab = 'notes';
      openModal(card);
    });
  });

  // Close modal
  closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeModal();
  });

  // Tab switching
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      currentTab = tab.dataset.tab;
      if (currentModule) {
        loadContent(currentModule, currentTab);
      }
    });
  });

  // ESC key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });
}

function openModal(card) {
  const overlay = document.getElementById('modalOverlay');
  const title = document.getElementById('modalTitle');

  // Get module title
  const moduleName = card.querySelector('h3').textContent;
  const dayNum = card.querySelector('.module-num').textContent;
  title.textContent = `DAY ${dayNum} — ${moduleName}`;

  // Reset tabs
  document.querySelectorAll('.modal-tab').forEach(t => t.classList.remove('active'));
  document.querySelector('.modal-tab[data-tab="notes"]').classList.add('active');
  currentTab = 'notes';

  overlay.classList.add('active');
  document.body.style.overflow = 'hidden';

  loadContent(card, 'notes');
}

function closeModal() {
  const overlay = document.getElementById('modalOverlay');
  overlay.classList.remove('active');
  document.body.style.overflow = '';
  currentModule = null;
}

async function loadContent(card, tab) {
  const content = document.getElementById('modalContent');
  content.innerHTML = '<div class="modal-loading">LOADING...</div>';

  const filePath = tab === 'notes' ? card.dataset.notes : card.dataset.exercise;

  if (!filePath) {
    content.innerHTML = '<div class="modal-loading">FILE NOT AVAILABLE</div>';
    return;
  }

  const url = GITHUB_RAW_BASE + filePath;

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to fetch');
    const markdown = await response.text();
    content.innerHTML = renderMarkdown(markdown);
  } catch (err) {
    content.innerHTML = `
      <div class="modal-loading">
        FAILED TO LOAD CONTENT<br><br>
        <a href="${url}" target="_blank" style="color: var(--red);">VIEW ON GITHUB →</a>
      </div>
    `;
  }
}

// SIMPLE MARKDOWN RENDERER
function renderMarkdown(md) {
  let html = md;

  // Code blocks (must be first)
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');

  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Headers
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

  // Bold and italic
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Blockquotes
  html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');

  // Unordered lists
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

  // Ordered lists
  html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

  // Horizontal rules
  html = html.replace(/^---$/gm, '<hr>');

  // Tables (simple)
  html = html.replace(/\|(.+)\|\n\|[-| ]+\|\n((?:\|.+\|\n?)+)/g, (match, header, body) => {
    const headers = header.split('|').filter(h => h.trim()).map(h => `<th>${h.trim()}</th>`).join('');
    const rows = body.trim().split('\n').map(row => {
      const cells = row.split('|').filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`).join('');
      return `<tr>${cells}</tr>`;
    }).join('');
    return `<table><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table>`;
  });

  // Paragraphs (wrap loose text)
  html = html.replace(/^(?!<[a-z]|$)(.+)$/gm, '<p>$1</p>');

  // Clean up empty paragraphs
  html = html.replace(/<p>\s*<\/p>/g, '');

  return html;
}

// KEYBOARD NAVIGATION
document.addEventListener('keydown', (e) => {
  if (document.getElementById('modalOverlay').classList.contains('active')) return;

  if (e.key >= '1' && e.key <= '9') {
    const day = e.key.padStart(2, '0');
    const target = document.getElementById(`day${day}`);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

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
