const popup = document.getElementById('mobile-menu');
function openmenu() {
    popup.style.display = 'block';

}

function closemenu() {
    popup.style.display = 'none';


}
popup.addEventListener('click', openmenu);
popup.addEventListener('click', closemenu);