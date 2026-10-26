// project pop-up section
const projectContainer = document.querySelector('#popupWindow');

const projectsData = [
  {
    id: 'project-one',
    name: 'Fomi Studio: AI Image Workspace',
    client: 'FOMI',
    role: 'Frontend Developer',
    year: '2026',
    image: 'fomi-studio.jpg',
    page: 'projects/fomi-studio/',
    technologies: ['Next.js', 'React', 'CSS Modules'],
    moreTechnologies: ['JavaScript', 'Vercel', 'GitHub'],
    projectDetail: 'A responsive AI image-generation workspace built from a design mockup for FOMI\'s frontend assessment, with a mocked API, loading states and phone/tablet layouts.',
    descriptionShort: 'A responsive AI image-generation workspace built with Next.js from a design mockup. It has a working generator panel, a gallery with loading and empty states, an image viewer and layouts made separately for phone, tablet and desktop.',
    descriptionLong: 'I built this for FOMI\'s frontend assessment: their Image Generator mockup turned into a real, working Next.js app. It includes a model picker, reference uploads, a prompt box with keyboard shortcuts, a mocked API that "generates" images and videos, loading placeholders in the right shape, a masonry gallery, a full-size viewer with keyboard navigation, and a guided tutorial that highlights the real controls. Each screen size has its own layout (on phones the generator becomes a bottom sheet), and the app uses next/image, lazy loading and accessible components throughout.',
    liveLink: 'https://fomi-studio-weld.vercel.app',
    sourceLink: 'https://github.com/Afsheen96/fomi-studio',
  },
  {
    id: 'project-two',
    name: 'Fomi Flow: Version-based Workspace',
    client: 'FOMI',
    role: 'Product & UI',
    year: '2026',
    image: 'fomi-flow.jpg',
    page: 'projects/fomi-flow/',
    technologies: ['Next.js', 'React', 'UX Design'],
    moreTechnologies: ['JavaScript', 'CSS Modules', 'Vercel'],
    projectDetail: 'My own redesign of an AI image workspace: every image is a version you can compare, branch and restore, with an automatic "what changed" summary.',
    descriptionShort: 'My redesign of an AI image workspace for professional creators. Every image is saved as a version, so you can compare it with the one it came from, see what changed and keep editing from any version.',
    descriptionLong: 'Most AI image tools show results as an endless feed, so good results get lost. In Fomi Flow every generation is a version inside a project. A version strip shows the history (with branches like "from v2"), a compare slider puts two versions side by side, and a "What changed" panel lists the prompt words added or removed and any settings change. The prompt bar starts filled with the selected version, so editing means changing a few words, not starting over. It works on phone, tablet and desktop, with keyboard shortcuts for moving between versions.',
    liveLink: 'https://fomi-studio-weld.vercel.app/flow',
    sourceLink: 'https://github.com/Afsheen96/fomi-studio',
  },
  {
    id: 'project-three',
    name: 'HighTechZone',
    client: 'Personal',
    role: 'Web Designer & Developer',
    year: '2026',
    image: 'hightechzone.jpg',
    page: 'projects/hightechzone/',
    technologies: ['HTML', 'CSS', 'JavaScript'],
    moreTechnologies: ['Responsive', 'GitHub Pages', 'Git'],
    projectDetail: 'My own website about AI tools, tech guides and digital skills, designed and built from scratch and published on GitHub Pages.',
    descriptionShort: 'My own website about AI tools, tech tips and digital-skills guides, with a modern dark design, animated hero and responsive layout.',
    descriptionLong: 'HighTechZone is my personal website where I share AI tools, practical tech guides and digital-skills content. I designed and built it myself: a bold dark theme, an animated hero section, clear navigation (AI Tools, Guides, Projects, Services) and a layout that works on phones, tablets and desktops. It is published for free on GitHub Pages.',
    liveLink: 'https://afsheen96.github.io/HighTechZone/',
    sourceLink: 'https://github.com/Afsheen96',
  },
];

const listItems = (items) => items.map((item) => `<li>${item}</li>`).join('');

const icons = {
  arrow: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
  external: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
  github: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/></svg>',
  eye: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
  close: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
};

// ------------popup modal------------------

function popUpWindow(project) {
  const projectcontent = `
  <div class="popup-container" data-close="true">
  <div class="popup" role="dialog" aria-modal="true" aria-labelledby="popupTitle">
  <div class="popup-top">
  <div>
  <h3 id="popupTitle">${project.name}</h3>
  <ul class="proj">
  <li><a href="${project.page}">${project.client}</a></li>
  <li><div class="dot"></div></li>
  <li>${project.role}</li>
  <li><div class="dot"></div></li>
  <li>${project.year}</li>
  </ul>
  </div>
  <button type="button" class="popup-close" id="popupClose" aria-label="Close">${icons.close}</button>
  </div>
  <div class="browser-frame">
  <div class="browser-bar"><span></span><span></span><span></span></div>
  <img src="./resources/${project.image}" alt="Screenshot of ${project.name}" class="popupImage" width="1088" height="896"/>
  </div>
  <div class="popup-body">
  <div class="left-popup">
  <p class="pro mobile-popup-info">
  ${project.descriptionShort}
  </p>
  <p class="pro desktop-popup-info">
  ${project.descriptionLong}
  </p>
  </div>
  <div class="right-popup">
  <ul class="language">
  ${listItems(project.technologies)}
  </ul>
  <ul class="language lagu-desktop">
  ${listItems(project.moreTechnologies)}
  </ul>
  <div class="thin-line"></div>
  <div class="popup-actions">
  <a href="${project.liveLink}" class="btn btn-primary popupLink" target="_blank" rel="noopener">Live Link ${icons.external}</a>
  <a href="${project.sourceLink}" class="btn btn-ghost popupLink" target="_blank" rel="noopener">Source Link ${icons.github}</a>
  </div>
  <a href="${project.page}" class="text-link">Read the full case study ${icons.arrow}</a>
  </div>
  </div>
  </div>
  </div>`;

  return projectcontent;
}

// ----------------------work samples--------------------

function projectWorkCards(projectsData = []) {
  let projectContent = '';

  projectsData.forEach((project, index) => {
    projectContent += `
    <article class="works reveal">
    <a class="work-media tilt" href="${project.page}" aria-label="Open the ${project.name} case study">
    <div class="browser-frame">
    <div class="browser-bar"><span></span><span></span><span></span></div>
    <div class="media-clip">
    <img src="./resources/${project.image}" alt="Screenshot of ${project.name}" class="img-transition" loading="lazy" width="1088" height="896"/>
    </div>
    </div>
    <span class="media-overlay"><span>View case study ${icons.arrow}</span></span>
    </a>
    <div class="card-work work">
    <span class="work-number">0${index + 1}</span>
    <h3><a href="${project.page}">${project.name}</a></h3>
    <ul class="proj">
    <li><a href="${project.page}">${project.client}</a></li>
    <li><div class="dot"></div></li>
    <li>${project.role}</li>
    <li><div class="dot"></div></li>
    <li>${project.year}</li>
    </ul>
    <p class="pro">
    ${project.projectDetail}
    </p>
    <ul class="language">
    ${listItems(project.technologies)}
    </ul>
    <div class="work-actions">
    <a class="btn btn-primary magnetic" href="${project.page}">See Project ${icons.arrow}</a>
    <button type="button" class="btn btn-ghost see-project-button" project-id="${project.id}">${icons.eye} Quick view</button>
    <a class="icon-link" href="${project.liveLink}" target="_blank" rel="noopener" aria-label="Open ${project.name} live website">${icons.external}</a>
    </div>
    </div>
    </article>
    `;
  });

  return projectContent;
}

// -----------------------open and close popup-----------------------

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
  const windowTemplate = popUpWindow(project);
  projectContainer.innerHTML = windowTemplate;
  projectContainer.style.display = 'block';
  document.body.classList.add('no-scroll');
  requestAnimationFrame(() => projectContainer.classList.add('is-open'));

  const popUpCloseButton = document.querySelector('#popupClose');

  popUpCloseButton.addEventListener('click', closeWindow);
  popUpCloseButton.focus();
  projectContainer.querySelector('.popup-container').addEventListener('click', (event) => {
    if (event.target.dataset.close) closeWindow();
  });
}

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && projectContainer.classList.contains('is-open')) closeWindow();
});

function renderProjects() {
  const portfolioSection = document.querySelector('#projects');
  projectContainer.style.display = 'none';

  portfolioSection.innerHTML = projectWorkCards(projectsData);

  const proButtons = document.querySelectorAll('.see-project-button');

  Array.from(proButtons).forEach((element) => {
    element.addEventListener('click', () => {
      const projectID = element.getAttribute('project-id');
      const projectObj = projectsData.find((project) => project.id === projectID);

      openWindow(projectObj);
    });
  });

  if (window.site) window.site.refresh();
}

renderProjects();

// form validation section
function validateEmail() {
  const emailInput = document.getElementById('email').value;
  const lowerCaseEmail = emailInput.toLowerCase();

  if (emailInput !== lowerCaseEmail) {
    document.getElementById('errormsg').innerHTML = '*Email must be in lowercase!';
    return false;
  }
  document.getElementById('errormsg').innerHTML = '';
  return true;
}

const contactForm = document.getElementById('contactform');
contactForm.addEventListener('submit', (event) => {
  if (!validateEmail()) event.preventDefault();
});

const submitform = document.getElementById('submit');
submitform.addEventListener('click', () => {
  validateEmail();
});

// local storage section
const storageData = document.querySelectorAll('.form-input');
const localStoreValue = {
  name: '',
  email: '',
  message: '',
};
storageData.forEach((input) => {
  input.addEventListener('input', () => {
    localStoreValue[input.name] = input.value;
    localStorage.setItem('information', JSON.stringify(localStoreValue));
  });
});
const informationStored = JSON.parse(localStorage.getItem('information'));
if (informationStored) {
  Object.assign(localStoreValue, informationStored);
  storageData.forEach((element) => {
    element.value = informationStored[element.name] || '';
  });
}
