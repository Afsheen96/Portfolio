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
    name: 'Tonic',
    image: 'project1.png',
    descriptionShort: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essent",
    descriptionLong: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it 1960s with the releaLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it 1960s with the releorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum han printer took a galley of type and scrambled it 1960s with the releawn printer took a galley of type and scrambled it 1960s with the releaLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it 1960s with the relea",
    projectDetail: 'A daily selection of privately personalized reads; accounts or sign-ups required.',
    liveLink: 'https://afsheen96.github.io/Portfolio',
    sourceLink: 'https://github.com/Afsheen96/Portfolio',
  },
  {
    id: 'project-two',
    name: 'Multi-post stories',
    image: 'project2.png',
    descriptionShort: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essent",
    descriptionLong: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it 1960s with the releaLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it 1960s with the releorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum han printer took a galley of type and scrambled it 1960s with the releawn printer took a galley of type and scrambled it 1960s with the releaLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it 1960s with the relea",
    projectDetail: 'Experimental content creation feature that allows users to add to an existing story over the course of a day without spamming their friends.',
    liveLink: 'https://afsheen96.github.io/Portfolio',
    sourceLink: 'https://github.com/Afsheen96/Portfolio',
  },
  {
    id: 'project-three',
    name: 'Tonic',
    image: 'project3.png',
    descriptionShort: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essent",
    descriptionLong: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it 1960s with the releaLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it 1960s with the releorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum han printer took a galley of type and scrambled it 1960s with the releawn printer took a galley of type and scrambled it 1960s with the releaLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it 1960s with the relea",
    projectDetail: "Exploring the future of media in Facebook's first Virtual Reality app; a place to discover and enjoy 360 photos and videos on Gear VR.",
    liveLink: 'https://afsheen96.github.io/Portfolio',
    sourceLink: 'https://github.com/Afsheen96/Portfolio',
  },
  {
    id: 'project-four',
    name: 'Multi-post stories',
    image: 'project4.png',
    descriptionShort: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essent",
    descriptionLong: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it 1960s with the releaLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it 1960s with the releorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum han printer took a galley of type and scrambled it 1960s with the releawn printer took a galley of type and scrambled it 1960s with the releaLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it 1960s with the relea",
    projectDetail: "Exploring the future of media in Facebook's first Virtual Reality app; a place to discover and enjoy 360 photos and videos on Gear VR.",
    liveLink: 'https://afsheen96.github.io/Portfolio',
    sourceLink: 'https://github.com/Afsheen96/Portfolio',
  },
];

// ------------popup modal------------------

function popUpWindow(project) {
  const projectcontent = `
  <div class= "popup-container">
    <div class= "popup">
      <div>
        <i class="fa-solid fa-xmark" id="popupClose"></i>
        <h3>${project.name}</h3>
        <ul class="proj">
          <li><a href="#">CANOPY</a></li>
          <li><div class="dot"></div></li>
          <li>Back End Dev</li>
          <li><div class="dot"></div></li>
          <li>2015</li>
        </ul>
      </div>
      <img src="./resources/${project.image}" alt="Work-sample" class="popupImage"/>
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
            <li>HTML</li>
            <li>CSS</li>
            <li>JavaScript</li>
          </ul>
          <ul class="language lagu-desktop">
            <li>Github</li>
            <li>Ruby</li>
            <li>BootStrap</li>
          </ul>
          <div class="thin-line"></div>
            <button class="button popup-buttons">
              <div>
                <a href="${project.liveLink}" class="popupLink">Live Link</a> <i class="fa-solid fa-arrow-up-right-from-square"></i>
              </div>
            </button>
            <button class="button popup-buttons">
              <div>
                <a href="${project.sourceLink}" class="popupLink">Source Link</a> <i class="fa-brands fa-square-github"></i></i>
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
    <img src="./resources/${project.image}" alt="Work-sample" class="img-transition"/>
    <div class="card-work work">
      <h3>${project.name}</h3>
      <ul class="proj">
        <li><a href="#">CANOPY</a></li>
        <li><div class="dot"></div></li>
        <li>Back End Dev</li>
        <li><div class="dot"></div></li>
        <li>2015</li>
      </ul>
      <p class="pro">
        ${project.projectDetail}
      </p>
      <ul class="language">
        <li>HTML</li>
        <li>CSS</li>
        <li>JavaScript</li>
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
