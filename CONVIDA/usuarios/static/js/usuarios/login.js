document.addEventListener("DOMContentLoaded", () => {


    /* =========================================
       PASSWORD
    ========================================= */

    const buttons =
        document.querySelectorAll(".toggle-password");


    buttons.forEach((button) => {

        button.addEventListener("click", () => {

            const target =
                document.getElementById(
                    button.dataset.target
                );


            if (!target) {
                return;
            }


            if (target.type === "password") {

                target.type = "text";

                button.textContent = "Ocultar";

            } else {

                target.type = "password";

                button.textContent = "Mostrar";

            }

        });

    });


    /* =========================================
       LOADING
    ========================================= */

    const form =
        document.getElementById("login-form");

    const submit =
        document.getElementById("submit-button");


    if (form && submit) {

        form.addEventListener("submit", () => {

            submit.disabled = true;

            const text =
                submit.querySelector(".button-text");

            const loading =
                submit.querySelector(".button-loading");


            if (text) {
                text.hidden = true;
            }


            if (loading) {

                loading.hidden = false;

            }

        });

    }

});