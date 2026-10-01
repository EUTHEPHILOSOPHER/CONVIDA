/**
 * =====================================================
 * CONVIDA
 * CADASTRO
 * =====================================================
 */


document.addEventListener("DOMContentLoaded", () => {


    /* =================================================
       MOSTRAR / OCULTAR PASSWORD
    ================================================= */

    const passwordButtons =
        document.querySelectorAll(".toggle-password");


    passwordButtons.forEach((button) => {

        button.addEventListener("click", () => {

            const targetId =
                button.dataset.target;

            const input =
                document.getElementById(targetId);


            if (!input) {
                return;
            }


            if (input.type === "password") {

                input.type = "text";

                button.textContent = "Ocultar";

            } else {

                input.type = "password";

                button.textContent = "Mostrar";

            }

        });

    });


    /* =================================================
       SUBMIT
    ================================================= */

    const form =
        document.getElementById("cadastro-form");

    const submitButton =
        document.getElementById("submit-button");

    const buttonText =
        submitButton?.querySelector(".button-text");

    const buttonLoading =
        submitButton?.querySelector(".button-loading");


    if (form && submitButton) {

        form.addEventListener("submit", () => {

            submitButton.disabled = true;

            submitButton.classList.add("loading");


            if (buttonText) {

                buttonText.hidden = true;

            }


            if (buttonLoading) {

                buttonLoading.hidden = false;

            }

        });

    }


    /* =================================================
       REMOVER ESTADO DE ERRO AO DIGITAR
    ================================================= */

    const inputs =
        form?.querySelectorAll("input");


    inputs?.forEach((input) => {

        input.addEventListener("input", () => {

            input.classList.remove("input-error");

        });

    });


});