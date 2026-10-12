document.addEventListener("DOMContentLoaded", () => {

    const options = document.querySelectorAll(
        'input[name="template"]'
    );

    const button =
        document.getElementById("continueButton");

    options.forEach((option) => {

        option.addEventListener("change", () => {

            button.disabled = false;

        });

    });

});