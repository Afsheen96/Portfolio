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
 const projects =[
  {
    // id: '1',
    // name: 'Tonic',
    // namedesk: 'Tonic',
    // description: 'A daily selection of privately personalized reads; no accounts or sign-ups required.',
    // Descriptiondesk: 'A daily selection of privately personalized reads; no accounts or sign-ups required.',
    // longDescription: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the
    // industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and
    // scrambled it 1960s with the releaLorem Ipsum is simply dummy text of the printing and typesetting
    // industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown
    // printer took a galley of type and scrambled it 1960s with the relea`,
    // featured: ['CANOPY', 'Back End Dev', 2023],
    // featureddesk: ['CANOPY', 'Back End Dev', 2023],
    // image: './First-image.jpg',
    // imageDesktop: './images/desktop/projectone.svg',
    // technologies: ['html', 'css', 'javaScript'],
    // technologiesdesk: ['html', 'css', 'javaScript', 'Ruby on rails;'],
    // live_version: 'https://afsheen96.github.io/Portfolio',
    // source_link: 'https://github.com/Afsheen96/Portfolio',
  }
 ]