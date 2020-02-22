
//Menu Responsive
const enlaces = document.getElementsByClassName("enlaces")[0];
const hmbrgMenu = document.getElementsByClassName("hmbgr-menu")[0];
const menuHmbrg = document.getElementById("hmbrg-menu");
let abierto = false;

const toggleMenu = () => {
    enlaces.classList.toggle("enlaces2")
    enlaces.style.transition = "transform 0.5s ease-in-out"
}

hmbrgMenu.addEventListener("click", function () {
    toggleMenu()
    if (document.querySelector(".enlaces.enlaces2")) {
        abierto = true;
    } else {
        abierto = false;
    }
})

window.addEventListener("click", function (e) {
    if (abierto) {
        if (e.target !== menuHmbrg) {
            toggleMenu();
            abierto = false;
        }
    }
})