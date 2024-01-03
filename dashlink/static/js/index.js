// Open sidebar for mobile view
var opened = false;
var sidebar = document.getElementById("sidebar");
function openSidebar() {
  if (opened == false) {
    sidebar.style.left = "0%";
    opened = true;
  } else {
    sidebar.style.left = "-100%";
    opened = false;
  }
};


// Alert box modal... My custom modal LOL
const alertBox = document.getElementById('alert');

const deleteLink = () => {
  alertBox.style.display = 'flex';
}

const abort = () => {
  alertBox.style.display = 'none';
}