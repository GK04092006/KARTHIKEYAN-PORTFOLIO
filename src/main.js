// ============================================================================
// KARTHIKEYAN S — Interactive Portfolio Controller
// Includes Live Terminal, Spotlight Cards, Skill/Project Filters & Certificate Viewer
// ============================================================================

const TERMINAL_RESPONSES = {
  profile: `$ karthikeyan --status
> Name       : KARTHIKEYAN S
> Degree     : B.E. Computer Science & Engineering (NEC, 2026)
> CGPA       : 7.34 / 10
> Target Role: Software Engineer | Full-Stack | AI Software Engineer
> GitHub     : https://github.com/GK04092006`,

  skills: `$ karthikeyan --skills --top
> Languages  : Java (92%), Python (92%), C++/C (88%), JS ES6+ (90%), SQL (90%)
> Backend/Web: Spring Boot, Flask, React.js, Node.js, Express, REST APIs, JWT
> Databases  : MySQL, PostgreSQL, MongoDB, Normalization, Joins, Indexing
> AI / Algo  : Scikit-learn, Pandas, NumPy, A* Pathfinding, Trees, Graphs`,

  flagship: `$ karthikeyan --project --flagship
> [01] AI-Powered Industrial Digital Twin & Risk Intelligence Platform
> Stack : React, Java, Spring Boot, Python ML, PostgreSQL, REST API, Docker
> Highlights: Real-time pipeline telemetry, ML anomaly & flood risk prediction,
              and A* risk-aware emergency evacuation pathfinding.`,

  github: `$ git remote -v
> origin  https://github.com/GK04092006 (fetch/push)
> Repositories:
  • Smart-Crop-Advisory-System   • careloop          • SMART-FIT
  • course-outcome-Analyzer      • weatherapp        • PORTFOLIO`
};

function initNavbar() {
  const navbar = document.getElementById('navbar');
  const burger = document.getElementById('burgerBtn');
  const mobileNav = document.getElementById('mobileNav');
  const navLinks = document.querySelectorAll('[data-nav]');

  function setMobileMenu(open) {
    if (!burger || !mobileNav) return;
    burger.setAttribute('aria-expanded', String(open));
    mobileNav.hidden = !open;
  }

  burger?.addEventListener('click', () => {
    const isOpen = burger.getAttribute('aria-expanded') === 'true';
    setMobileMenu(!isOpen);
  });

  mobileNav?.addEventListener('click', (e) => {
    if (e.target.closest('a')) setMobileMenu(false);
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setMobileMenu(false);
  });

  const sections = ['home', 'education', 'skills', 'projects', 'certifications', 'contact']
    .map((id) => ({ id, el: document.getElementById(id) }))
    .filter((s) => s.el);

  function onScroll() {
    if (navbar) {
      navbar.classList.toggle('is-scrolled', window.scrollY > 20);
    }

    const scrollPos = window.scrollY + 170;
    let activeId = 'home';

    for (const section of sections) {
      const top = section.el.offsetTop;
      const height = section.el.offsetHeight;
      if (scrollPos >= top && scrollPos < top + height) {
        activeId = section.id;
        break;
      } else if (scrollPos >= top) {
        activeId = section.id;
      }
    }

    navLinks.forEach((link) => {
      const href = link.getAttribute('href');
      link.classList.toggle('is-active', href === `#${activeId}`);
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

function initTerminal() {
  const buttons = document.querySelectorAll('[data-term-cmd]');
  const screen = document.getElementById('terminalScreen');
  if (!buttons.length || !screen) return;

  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      buttons.forEach((b) => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      const key = btn.dataset.termCmd;
      screen.textContent = TERMINAL_RESPONSES[key] || TERMINAL_RESPONSES.profile;
    });
  });
}

function initSpotlightCards() {
  const cards = document.querySelectorAll('.spotlight-card, .tech-card, .project-card, .cert-card, .info-card');
  cards.forEach((card) => {
    card.classList.add('spotlight-card');
    card.addEventListener('pointermove', (e) => {
      const rect = card.getBoundingClientRect();
      card.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
      card.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
    });
  });
}

function initSkillFilter() {
  const buttons = document.querySelectorAll('[data-skill-filter]');
  const cards = document.querySelectorAll('.tech-card');
  if (!buttons.length || !cards.length) return;

  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      buttons.forEach((b) => b.classList.remove('is-active'));
      btn.classList.add('is-active');

      const filter = btn.dataset.skillFilter;
      cards.forEach((card) => {
        const cats = (card.dataset.category || '').split(/\s+/);
        const show = filter === 'all' || cats.includes(filter);
        card.style.display = show ? '' : 'none';
      });
    });
  });
}

function initProjectFilter() {
  const buttons = document.querySelectorAll('[data-proj-filter]');
  const cards = document.querySelectorAll('.project-card');
  if (!buttons.length || !cards.length) return;

  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      buttons.forEach((b) => b.classList.remove('is-active'));
      btn.classList.add('is-active');

      const filter = btn.dataset.projFilter;
      cards.forEach((card) => {
        const cats = (card.dataset.category || '').split(/\s+/);
        const show = filter === 'all' || cats.includes(filter);
        card.style.display = show ? '' : 'none';
      });
    });
  });
}

function initCertificateViewer() {
  const lightbox = document.getElementById('certLightbox');
  const lbImg = document.getElementById('certLightboxImg');
  const lbTitle = document.getElementById('certLightboxTitle');
  const lbDownload = document.getElementById('certLightboxDownload');
  const prevBtn = document.getElementById('certPrevBtn');
  const nextBtn = document.getElementById('certNextBtn');
  if (!lightbox || !lbImg) return;

  const triggers = Array.from(document.querySelectorAll('[data-view-cert]'));
  const items = [];
  const seen = new Set();

  triggers.forEach((el) => {
    const src = el.dataset.viewCert;
    const title = el.dataset.certTitle || 'Certificate Preview';
    if (src && !seen.has(src)) {
      seen.add(src);
      items.push({ src, title });
    }
  });

  let currentIndex = 0;

  function showAtIndex(idx) {
    if (!items.length) return;
    currentIndex = (idx + items.length) % items.length;
    const item = items[currentIndex];
    lbImg.src = item.src;
    lbImg.alt = item.title;
    if (lbTitle) lbTitle.textContent = item.title;
    if (lbDownload) {
      lbDownload.href = item.src;
      lbDownload.setAttribute('download', item.src.split('/').pop() || 'certificate.png');
    }
    lightbox.hidden = false;
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightbox.hidden = true;
    document.body.style.overflow = '';
  }

  triggers.forEach((el) => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      const src = el.dataset.viewCert;
      const idx = items.findIndex((i) => i.src === src);
      showAtIndex(idx >= 0 ? idx : 0);
    });
  });

  prevBtn?.addEventListener('click', () => showAtIndex(currentIndex - 1));
  nextBtn?.addEventListener('click', () => showAtIndex(currentIndex + 1));

  lightbox.querySelectorAll('[data-close-lightbox]').forEach((closer) => {
    closer.addEventListener('click', closeLightbox);
  });

  window.addEventListener('keydown', (e) => {
    if (lightbox.hidden) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') showAtIndex(currentIndex - 1);
    if (e.key === 'ArrowRight') showAtIndex(currentIndex + 1);
  });
}

let toastTimer;
function showToast(msg) {
  const toast = document.getElementById('copyToast');
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add('is-shown');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.classList.remove('is-shown');
  }, 2600);
}

function initClipboard() {
  document.querySelectorAll('[data-copy]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const text = btn.dataset.copy;
      if (!text) return;
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(text);
        } else {
          const ta = document.createElement('textarea');
          ta.value = text;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          ta.remove();
        }
        showToast(`Copied to clipboard: ${text}`);
      } catch {
        showToast(`Copied: ${text}`);
      }
    });
  });
}

function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const name = data.get('name') || '';
    const email = data.get('email') || '';
    const subject = data.get('subject') || 'Software Engineering Inquiry';
    const message = data.get('message') || '';

    const body = `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`;
    const mailto = `mailto:24104011@nec.edu.in?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

    showToast('Opening email client...');
    setTimeout(() => {
      window.location.href = mailto;
    }, 350);
    form.reset();
  });
}

function boot() {
  initNavbar();
  initTerminal();
  initSpotlightCards();
  initSkillFilter();
  initProjectFilter();
  initCertificateViewer();
  initClipboard();
  initContactForm();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}
