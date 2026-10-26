// Project cards: quick-view popup (home and Projects page), the project
// filter on the Projects page, and redirects for old one-page links.
(() => {
  // Old links like /Portfolio/#about now have their own pages.
  const legacy = {
    '#about': 'about/', '#form': 'contact/', '#portfolio': 'projects/', '#projects': 'projects/',
  };
  if (document.body.dataset.page === 'home' && legacy[window.location.hash]) {
    window.location.replace(legacy[window.location.hash]);
    return;
  }

  const projectContainer = document.querySelector('#popupWindow');
  const dataEl = document.getElementById('projects-data');
  const projectsData = dataEl ? JSON.parse(dataEl.textContent) : [];

  const escapeHtml = (text) => String(text).replace(/[&<>"']/g, (ch) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[ch]));
  const listItems = (items) => items.map((item) => `<li>${escapeHtml(item)}</li>`).join('');

  const icons = {
    arrow: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    external: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
    code: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/></svg>',
    close: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  };

  // ------------popup modal------------------
  function popUpWindow(project) {
    return `
    <div class="popup-container" data-close="true">
      <div class="popup" role="dialog" aria-modal="true" aria-labelledby="popupTitle">
        <div class="popup-top">
          <div>
            <h3 id="popupTitle">${escapeHtml(project.name)}</h3>
            <ul class="proj">
              <li><strong>${escapeHtml(project.client)}</strong></li>
              <li><div class="dot"></div></li>
              <li>${escapeHtml(project.role)}</li>
              <li><div class="dot"></div></li>
              <li>${escapeHtml(project.year)}</li>
            </ul>
          </div>
          <button type="button" class="popup-close" id="popupClose" aria-label="Close">${icons.close}</button>
        </div>
        <div class="browser-frame">
          <div class="browser-bar"><span></span><span></span><span></span></div>
          <img src="${project.image}" alt="Screenshot of ${escapeHtml(project.name)}" class="popupImage" width="1440" height="900"/>
        </div>
        <div class="popup-body">
          <div class="left-popup"><p class="pro">${escapeHtml(project.text)}</p></div>
          <div class="right-popup">
            <ul class="language">${listItems(project.tech)}</ul>
            <div class="thin-line"></div>
            <div class="popup-actions">
              <a href="${project.live}" class="btn btn-primary" target="_blank" rel="noopener">Live Link ${icons.external}</a>
              <a href="${project.source}" class="btn btn-ghost" target="_blank" rel="noopener">${icons.code} ${escapeHtml(project.sourceLabel)}</a>
            </div>
            <a href="${project.page}" class="text-link">Read the full case study ${icons.arrow}</a>
          </div>
        </div>
      </div>
    </div>`;
  }

  let lastFocused = null;

  function closeWindow() {
    projectContainer.classList.remove('is-open');
    document.body.classList.remove('no-scroll');
    setTimeout(() => {
      if (!projectContainer.classList.contains('is-open')) {
        projectContainer.style.display = 'none';
        projectContainer.innerHTML = '';
      }
    }, 300);
    if (lastFocused) lastFocused.focus();
  }

  function openWindow(project) {
    lastFocused = document.activeElement;
    projectContainer.innerHTML = popUpWindow(project);
    projectContainer.style.display = 'block';
    document.body.classList.add('no-scroll');
    requestAnimationFrame(() => projectContainer.classList.add('is-open'));
    const closeButton = projectContainer.querySelector('#popupClose');
    closeButton.addEventListener('click', closeWindow);
    closeButton.focus();
    projectContainer.querySelector('.popup-container').addEventListener('click', (event) => {
      if (event.target.dataset.close) closeWindow();
    });
  }

  if (projectContainer) {
    document.querySelectorAll('.quick-view').forEach((button) => {
      button.addEventListener('click', () => {
        const project = projectsData.find((p) => p.slug === button.dataset.project);
        if (project) openWindow(project);
      });
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && projectContainer.classList.contains('is-open')) closeWindow();
    });
  }

  // ----------------------project filter (Projects page)-----------------------
  const filterButtons = document.querySelectorAll('.filter-btn');
  const cards = document.querySelectorAll('.project-card');
  filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const { filter } = button.dataset;
      filterButtons.forEach((b) => {
        b.classList.toggle('active', b === button);
        b.setAttribute('aria-pressed', String(b === button));
      });
      cards.forEach((card) => {
        const show = filter === 'all' || card.dataset.category === filter;
        card.classList.toggle('is-hidden', !show);
        if (show) card.classList.add('visible');
      });
    });
  });
})();
