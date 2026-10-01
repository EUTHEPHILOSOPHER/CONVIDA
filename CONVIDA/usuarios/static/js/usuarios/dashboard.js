document.addEventListener("DOMContentLoaded", () => {


    const sidebar =
        document.getElementById("sidebar");

    const overlay =
        document.getElementById("sidebar-overlay");

    const menuButton =
        document.getElementById("menu-button");

    const closeButton =
        document.getElementById("close-sidebar");


    function openSidebar() {

        sidebar?.classList.add("open");

        overlay?.classList.add("active");

        document.body.style.overflow = "hidden";
    }


    function closeSidebar() {

        sidebar?.classList.remove("open");

        overlay?.classList.remove("active");

        document.body.style.overflow = "";
    }


    menuButton?.addEventListener(
        "click",
        openSidebar
    );


    closeButton?.addEventListener(
        "click",
        closeSidebar
    );


    overlay?.addEventListener(
        "click",
        closeSidebar
    );


    /*
     * Fechar menu depois de clicar
     * em uma opção no mobile.
     */

    const navItems =
        document.querySelectorAll(".nav-item");


    navItems.forEach((item) => {

        item.addEventListener("click", () => {

            if (window.innerWidth <= 900) {

                closeSidebar();

            }

        });

    });


    /*
     * Quando a janela voltar para desktop,
     * removemos o estado mobile.
     */

    window.addEventListener("resize", () => {

        if (window.innerWidth > 900) {

            closeSidebar();

        }

    });

});