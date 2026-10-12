
document.addEventListener("DOMContentLoaded", () => {
    const title = document.getElementById("id_titulo");
    const date = document.getElementById("id_data_evento");
    const time = document.getElementById("id_hora_evento");
    const location = document.getElementById("id_local_evento");
    const description = document.getElementById("id_descricao");

    const previewTitle = document.getElementById("previewTitle");
    const previewDate = document.getElementById("previewDate");
    const previewTime = document.getElementById("previewTime");
    const previewLocation = document.getElementById("previewLocation");
    const previewDescription = document.getElementById("previewDescription");

    const update = (field, target, fallback, formatter = value => value) => {
        if (!field || !target) return;

        const refresh = () => {
            target.textContent = field.value
                ? formatter(field.value)
                : fallback;
        };

        field.addEventListener("input", refresh);
        field.addEventListener("change", refresh);
        refresh();
    };

    update(title, previewTitle, "Título do evento");
    update(date, previewDate, "Data a definir", value => {
        const parts = value.split("-");
        return parts.length === 3
            ? `${parts[2]}/${parts[1]}/${parts[0]}`
            : value;
    });
    update(time, previewTime, "Hora a definir");
    update(location, previewLocation, "Local a definir");
    update(description, previewDescription, "");
});
