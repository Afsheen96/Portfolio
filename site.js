// Shared interactions for every page: header, mobile menu, page transitions,
// scroll reveal, typing effect, accordions, tilt, magnetic buttons, ripples
// and the social links from config.js.
(() => {
  const root = document.documentElement;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  root.classList.add('js');

  // ---------- social links (config.js) ----------
  const config = window.SITE_CONFIG || {};
  document.querySelectorAll('[data-social]').forEach((link) => {
    const key = link.dataset.social;
    const value = (config[key] || '').trim();
    const valueEl = link.querySelector('[data-social-value]');
    if (!value) {
      link.removeAttribute('href');
      link.classList.add('is-pending');
      link.setAttribute('aria-disabled', 'true');
      link.setAttribute('title', `${link.dataset.label || 'This link'}: coming soon`);
      if (valueEl) valueEl.textContent = 'Coming soon';
      return;
    }
    if (key === 'email') {
      link.href = `mailto:${value}`;
      if (valueEl) valueEl.textContent = value;
    } else {
      link.href = value;
      link.target = '_blank';
      link.rel = 'noopener';
    }
  });

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
    if (open && closeBtn) closeBtn.focus();
  }
  if (openBtn) openBtn.addEventListener('click', () => setMenu(true));
  if (closeBtn) closeBtn.addEventListener('click', () => setMenu(false));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileMenu && mobileMenu.classList.contains('open')) setMenu(false);
  });

  // ---------- page transitions ----------
  // Fade out before going to another page of this site; the next page fades in.
  const supportsViewTransitions = 'onpagereveal' in window;
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a[href]');
    if (!link || reduceMotion || supportsViewTransitions) return;
    if (e.defaultPrevented || e.button !== 0) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (link.target === '_blank' || link.hasAttribute('download')) return;
    const url = new URL(link.href, window.location.href);
    if (url.origin !== window.location.origin || url.protocol.indexOf('http') !== 0) return;
    if (url.pathname === window.location.pathname && url.hash) return;
    e.preventDefault();
    if (mobileMenu) mobileMenu.classList.remove('open');
    root.classList.add('is-leaving');
    setTimeout(() => { window.location.href = url.href; }, 220);
  });
  window.addEventListener('pageshow', () => root.classList.remove('is-leaving'));

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
    document.querySelectorAll('.pc-media:not([data-tilt]), .tilt:not([data-tilt])').forEach((card) => {
      card.setAttribute('data-tilt', '');
      card.addEventListener('mousemove', (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(1000px) rotateX(${(-y * 5).toFixed(2)}deg) rotateY(${(x * 7).toFixed(2)}deg)`;
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

  // ---------- click ripple ----------
  if (!reduceMotion) {
    document.addEventListener('pointerdown', (e) => {
      const btn = e.target.closest('.btn, .form-button, .nav-cta, .filter-btn');
      if (!btn) return;
      const r = btn.getBoundingClientRect();
      const ripple = document.createElement('span');
      const size = Math.max(r.width, r.height) * 2;
      ripple.className = 'ripple';
      ripple.style.width = `${size}px`;
      ripple.style.height = `${size}px`;
      ripple.style.left = `${e.clientX - r.left - size / 2}px`;
      ripple.style.top = `${e.clientY - r.top - size / 2}px`;
      btn.appendChild(ripple);
      setTimeout(() => ripple.remove(), 650);
    });
  }

  // ---------- typing effect ----------
  const typed = document.getElementById('typed');
  if (typed && !reduceMotion) {
    const words = ['modern websites', 'responsive web apps', 'landing pages that convert', 'engaging user interfaces'];
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
    setTimeout(tick, 2800);
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

  window.site = { refresh, reduceMotion, finePointer };
})();
