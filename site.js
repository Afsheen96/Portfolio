// Shared interactions for every page: header, mobile menu, scroll reveal,
// typing effect, accordions, tilt and magnetic buttons.
(() => {
  const root = document.documentElement;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  root.classList.add('js');

  // ---------- header + scroll progress ----------
  const headerNav = document.getElementById('header-nav');
  const progress = document.querySelector('.scroll-progress');
  let ticking = false;

  function onScroll() {
    const y = window.scrollY;
    if (headerNav) headerNav.classList.toggle('scrolled', y > 20);
    if (progress) {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
    }
    ticking = false;
  }
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(onScroll);
      ticking = true;
    }
  }, { passive: true });
  onScroll();

  // ---------- mobile menu ----------
  const mobileMenu = document.getElementById('mobile-menu');
  const openBtn = document.getElementById('menu-open');
  const closeBtn = document.getElementById('menu-close');

  function setMenu(open) {
    if (!mobileMenu) return;
    mobileMenu.classList.toggle('open', open);
    document.body.classList.toggle('no-scroll', open);
    if (openBtn) openBtn.setAttribute('aria-expanded', String(open));
  }
  if (openBtn) openBtn.addEventListener('click', () => setMenu(true));
  if (closeBtn) closeBtn.addEventListener('click', () => setMenu(false));
  if (mobileMenu) {
    mobileMenu.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenu(false)));
  }
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileMenu && mobileMenu.classList.contains('open')) setMenu(false);
  });

  // ---------- active nav link ----------
  const navLinks = Array.from(document.querySelectorAll('.nav-link[href^="#"]'));
  const sections = navLinks
    .map((link) => document.querySelector(link.getAttribute('href')))
    .filter(Boolean);
  if ('IntersectionObserver' in window && sections.length) {
    const navObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          navLinks.forEach((link) => link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`));
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach((s) => navObserver.observe(s));
  }

  // ---------- reveal on scroll ----------
  let revealObserver = null;
  if ('IntersectionObserver' in window && !reduceMotion) {
    revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  }

  function observeReveals() {
    document.querySelectorAll('.reveal:not(.visible)').forEach((el) => {
      if (revealObserver) revealObserver.observe(el);
      else el.classList.add('visible');
    });
  }

  // ---------- tilt cards ----------
  function bindTilt() {
    if (!finePointer || reduceMotion) return;
    document.querySelectorAll('.tilt:not([data-tilt])').forEach((card) => {
      card.setAttribute('data-tilt', '');
      card.addEventListener('mousemove', (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(900px) rotateX(${(-y * 6).toFixed(2)}deg) rotateY(${(x * 8).toFixed(2)}deg)`;
        card.style.setProperty('--mx', `${(x + 0.5) * 100}%`);
        card.style.setProperty('--my', `${(y + 0.5) * 100}%`);
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
      });
    });
  }

  // ---------- magnetic buttons ----------
  function bindMagnetic() {
    if (!finePointer || reduceMotion) return;
    document.querySelectorAll('.magnetic:not([data-magnetic])').forEach((btn) => {
      btn.setAttribute('data-magnetic', '');
      btn.addEventListener('mousemove', (e) => {
        const r = btn.getBoundingClientRect();
        const x = e.clientX - r.left - r.width / 2;
        const y = e.clientY - r.top - r.height / 2;
        btn.style.transform = `translate(${x * 0.18}px, ${y * 0.25}px)`;
      });
      btn.addEventListener('mouseleave', () => {
        btn.style.transform = '';
      });
    });
  }

  // ---------- typing effect ----------
  const typed = document.getElementById('typed');
  if (typed && !reduceMotion) {
    const words = ['modern websites', 'responsive web apps', 'landing pages that convert', 'AI-powered interfaces'];
    let w = 0;
    let c = words[0].length;
    let deleting = true;
    const tick = () => {
      const word = words[w];
      c += deleting ? -1 : 1;
      typed.textContent = word.slice(0, c);
      let delay = deleting ? 40 : 75;
      if (!deleting && c === word.length) {
        deleting = true;
        delay = 2200;
      } else if (deleting && c === 0) {
        deleting = false;
        w = (w + 1) % words.length;
        delay = 350;
      }
      setTimeout(tick, delay);
    };
    setTimeout(tick, 2600);
  }

  // ---------- accordions ----------
  document.querySelectorAll('.accordion-toggle').forEach((toggle) => {
    toggle.addEventListener('click', () => {
      const item = toggle.closest('.accordion');
      const open = !item.classList.contains('open');
      item.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', String(open));
    });
  });

  // ---------- footer year ----------
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  function refresh() {
    observeReveals();
    bindTilt();
    bindMagnetic();
  }

  // page entrance
  window.requestAnimationFrame(() => root.classList.add('loaded'));
  refresh();

  window.site = { refresh };
})();
