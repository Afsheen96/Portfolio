// Animated hero background: softly drifting particles in the brand colours
// that link up with thin lines and gently react to the mouse, plus a
// spotlight and parallax shapes. Pauses when the hero is off screen or the
// tab is hidden, and draws a single still frame for reduced motion.
(() => {
  const hero = document.querySelector('.hero');
  const canvas = hero && hero.querySelector('.hero-canvas');
  if (!canvas || !canvas.getContext) return;

  const ctx = canvas.getContext('2d');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const colors = ['96,112,255', '127,140,255', '57,109,242'];
  const mouse = { x: -9999, y: -9999, active: false };
  let particles = [];
  let width = 0;
  let height = 0;
  let dpr = 1;
  let running = false;
  let frame = null;

  function resize() {
    const rect = hero.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = rect.width;
    height = rect.height;
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    const target = Math.round(Math.min(90, Math.max(28, (width * height) / 16000)));
    particles = Array.from({ length: target }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      r: Math.random() * 1.8 + 0.8,
      c: colors[Math.floor(Math.random() * colors.length)],
      a: Math.random() * 0.4 + 0.35,
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);
    const linkDist = Math.min(150, width / 7);

    for (let i = 0; i < particles.length; i += 1) {
      const p = particles[i];

      if (mouse.active) {
        const dx = p.x - mouse.x;
        const dy = p.y - mouse.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 140 && dist > 0) {
          const force = (140 - dist) / 140;
          p.vx += (dx / dist) * force * 0.06;
          p.vy += (dy / dist) * force * 0.06;
        }
      }

      p.vx *= 0.985;
      p.vy *= 0.985;
      if (Math.abs(p.vx) < 0.05) p.vx += (Math.random() - 0.5) * 0.04;
      if (Math.abs(p.vy) < 0.05) p.vy += (Math.random() - 0.5) * 0.04;
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < -10) p.x = width + 10;
      if (p.x > width + 10) p.x = -10;
      if (p.y < -10) p.y = height + 10;
      if (p.y > height + 10) p.y = -10;

      for (let j = i + 1; j < particles.length; j += 1) {
        const q = particles[j];
        const dx = p.x - q.x;
        const dy = p.y - q.y;
        const d2 = dx * dx + dy * dy;
        if (d2 < linkDist * linkDist) {
          const alpha = (1 - Math.sqrt(d2) / linkDist) * 0.22;
          ctx.strokeStyle = `rgba(96,112,255,${alpha.toFixed(3)})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(q.x, q.y);
          ctx.stroke();
        }
      }

      if (mouse.active) {
        const dx = p.x - mouse.x;
        const dy = p.y - mouse.y;
        const d = Math.sqrt(dx * dx + dy * dy);
        if (d < 190) {
          ctx.strokeStyle = `rgba(127,140,255,${((1 - d / 190) * 0.35).toFixed(3)})`;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.stroke();
        }
      }

      ctx.fillStyle = `rgba(${p.c},${p.a})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function loop() {
    draw();
    frame = window.requestAnimationFrame(loop);
  }

  function start() {
    if (running || reduceMotion) return;
    running = true;
    loop();
  }

  function stop() {
    running = false;
    if (frame) window.cancelAnimationFrame(frame);
  }

  resize();
  draw();

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      resize();
      draw();
    }, 150);
  });

  if (!reduceMotion) {
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(([entry]) => {
        if (entry.isIntersecting && !document.hidden) start();
        else stop();
      }).observe(hero);
    } else {
      start();
    }
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) stop();
      else if (hero.getBoundingClientRect().bottom > 0) start();
    });
  }

  // mouse: particles, spotlight and parallax shapes
  if (finePointer && !reduceMotion) {
    const shapes = Array.from(hero.querySelectorAll('[data-depth]'));
    hero.addEventListener('mousemove', (e) => {
      const rect = hero.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
      mouse.active = true;
      hero.style.setProperty('--spot-x', `${mouse.x}px`);
      hero.style.setProperty('--spot-y', `${mouse.y}px`);
      const nx = mouse.x / rect.width - 0.5;
      const ny = mouse.y / rect.height - 0.5;
      shapes.forEach((s) => {
        const depth = Number(s.dataset.depth) || 20;
        s.style.transform = `translate(${(-nx * depth).toFixed(1)}px, ${(-ny * depth).toFixed(1)}px)`;
      });
      hero.style.setProperty('--bg-x', `${(-nx * 14).toFixed(1)}px`);
      hero.style.setProperty('--bg-y', `${(-ny * 10).toFixed(1)}px`);
      hero.classList.add('is-hovered');
    });
    hero.addEventListener('mouseleave', () => {
      mouse.active = false;
      mouse.x = -9999;
      mouse.y = -9999;
      hero.classList.remove('is-hovered');
    });
  }
})();
