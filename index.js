const element = document.getElementById('mobile-menu');
function menu() {
  if (element.style.display === 'block') {
    element.style.display = 'none';
  } else {
    element.style.display = 'block';
  }
}
element.addEventListener('click', menu);

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

// ------------popup modal------------------

function popUpWindow(project) {
  const projectcontent = `
  <div class= "popup-container">
  <div class= "popup">
  <div>
  <i class="fa-solid fa-xmark" id="popupClose"></i>
  <h3>${project.name}</h3>
  <ul class="proj">
  <li><a href="#">${project.client}</a></li>
  <li><div class="dot"></div></li>
  <li>${project.role}</li>
  <li><div class="dot"></div></li>
  <li>${project.year}</li>
  </ul>
  </div>
  <img src="./resources/${project.image}" alt="Screenshot of ${project.name}" class="popupImage"/>
  <div>
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
  <button class="button popup-buttons">
  <div>
  <a href="${project.liveLink}" class="popupLink" target="_blank" rel="noopener">Live Link</a> <i class="fa-solid fa-arrow-up-right-from-square"></i>
  </div>
  </button>
  <button class="button popup-buttons">
  <div>
  <a href="${project.sourceLink}" class="popupLink" target="_blank" rel="noopener">Source Link</a> <i class="fa-brands fa-square-github"></i>
  </div>
  </button>
  </div>
  </div>
  </div>
  </div>
  </div>`;

  return projectcontent;
}

// ----------------------work samples--------------------

function projectWorkCards(projectsData = []) {
  let projectContent = '';

  projectsData.forEach((project) => {
    projectContent += `
    <div class= "works" id= "portfolio">
    <img src="./resources/${project.image}" alt="Screenshot of ${project.name}" class="img-transition"/>
    <div class="card-work work">
    <h3>${project.name}</h3>
    <ul class="proj">
    <li><a href="#">${project.client}</a></li>
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
    <button class="button button-mg" project-id="${project.id}" id="see-project-button">See Project</button>
    </div>
    </div>
    `;
  });

  return projectContent;
}

// -----------------------open and close popup-----------------------

function closeWindow() {
  projectContainer.style.display = 'none';
}

function openWindow(project) {
  const windowTemplate = popUpWindow(project);
  projectContainer.innerHTML = windowTemplate;
  projectContainer.style.display = 'block';

  const popUpCloseButton = document.querySelector('#popupClose');

  popUpCloseButton.addEventListener('click', closeWindow);
}

window.addEventListener('load', () => {
  const portfolioSection = document.querySelector('#projects');
  projectContainer.style.display = 'none';

  portfolioSection.innerHTML = projectWorkCards(projectsData);

  const proButtons = document.querySelectorAll('#see-project-button');

  Array.from(proButtons).forEach((element) => {
    element.addEventListener('click', () => {
      const projectID = element.getAttribute('project-id');
      const projectObj = projectsData.find((project) => project.id === projectID);

      openWindow(projectObj);
    });
  });
});
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

const submitform = document.getElementById('submit');
submitform.addEventListener('click', () => {
  validateEmail();
});
