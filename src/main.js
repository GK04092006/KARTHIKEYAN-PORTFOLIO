// ============================================================================
// KARTHIKEYAN S — Professional Portfolio Interactive Controller
// Clean, zero-dependency controller for navigation, filters, clipboard & form
// ============================================================================

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

  // Scrollspy & sticky header shadow
  const sections = ['home', 'education', 'skills', 'projects', 'certifications', 'contact']
    .map((id) => ({ id, el: document.getElementById(id) }))
    .filter((s) => s.el);

  function onScroll() {
    if (navbar) {
      navbar.classList.toggle('is-scrolled', window.scrollY > 20);
    }

    const scrollPos = window.scrollY + 160;
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

function initSkillFilter() {
  const buttons = document.querySelectorAll('[data-skill-filter]');
  const cards = document.querySelectorAll('.skill-card');
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
  initSkillFilter();
  initProjectFilter();
  initClipboard();
  initContactForm();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}
