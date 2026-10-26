// Live preview on project pages: loads the real website in a frame
// only when asked, and lets visitors switch between device sizes.
(() => {
  document.querySelectorAll('.preview').forEach((preview) => {
    const device = preview.querySelector('.preview-device');
    const screen = preview.querySelector('.preview-screen');
    const loadBtn = preview.querySelector('.preview-load');
    const buttons = preview.querySelectorAll('.device-btn');

    function load() {
      if (screen.querySelector('iframe')) return;
      const frame = document.createElement('iframe');
      frame.src = preview.dataset.src;
      frame.title = 'Live preview of the website';
      frame.loading = 'lazy';
      frame.referrerPolicy = 'no-referrer';
      frame.addEventListener('load', () => screen.classList.add('loaded'));
      screen.appendChild(frame);
      screen.classList.add('loading');
    }

    loadBtn.addEventListener('click', load);

    buttons.forEach((btn) => {
      btn.addEventListener('click', () => {
        buttons.forEach((b) => {
          b.classList.toggle('active', b === btn);
          b.setAttribute('aria-pressed', String(b === btn));
        });
        device.style.maxWidth = btn.dataset.width;
        device.classList.toggle('is-mobile', btn.dataset.width !== '100%');
        load();
      });
    });
  });
})();

// Lightbox: click a screenshot to see it large.
(() => {
  const box = document.getElementById('lightbox');
  if (!box) return;
  const img = box.querySelector('img');
  const caption = box.querySelector('figcaption');
  const closeBtn = box.querySelector('.lightbox-close');
  let lastFocused = null;

  function close() {
    box.classList.remove('open');
    document.body.classList.remove('no-scroll');
    setTimeout(() => { box.hidden = true; }, 250);
    if (lastFocused) lastFocused.focus();
  }

  document.querySelectorAll('[data-lightbox]').forEach((trigger) => {
    trigger.addEventListener('click', () => {
      lastFocused = trigger;
      img.src = trigger.dataset.lightbox;
      img.alt = trigger.dataset.caption || '';
      caption.textContent = trigger.dataset.caption || '';
      box.hidden = false;
      document.body.classList.add('no-scroll');
      requestAnimationFrame(() => box.classList.add('open'));
      closeBtn.focus();
    });
  });
  closeBtn.addEventListener('click', close);
  box.addEventListener('click', (e) => { if (e.target === box) close(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !box.hidden) close(); });
})();
