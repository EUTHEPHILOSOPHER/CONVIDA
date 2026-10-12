document.addEventListener("DOMContentLoaded", () => {

    const options = document.querySelectorAll(
        '.event-option input[name="tipo_evento"]'
    );

    const continueButton =
        document.getElementById("continueButton");


    options.forEach((option) => {

        option.addEventListener("change", () => {

            continueButton.disabled = false;

        });

    });

});