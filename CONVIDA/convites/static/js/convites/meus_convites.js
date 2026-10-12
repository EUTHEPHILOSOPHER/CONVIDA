document.addEventListener("DOMContentLoaded", () => {
    const mobileMenu = document.getElementById("mobileMenu");

    if (mobileMenu) {
        mobileMenu.addEventListener("click", () => {
            alert("Menu mobile será ativado na próxima etapa.");
        });
    }
});