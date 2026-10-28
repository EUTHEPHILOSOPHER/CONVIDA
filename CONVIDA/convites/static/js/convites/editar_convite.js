
document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    // Campos do formulário Django
    const fields = {
        title: document.getElementById("id_titulo"),
        date: document.getElementById("id_data_evento"),
        time: document.getElementById("id_hora_evento"),
        location: document.getElementById("id_local_evento"),
        description: document.getElementById("id_descricao"),
    };

    // Elementos da pré-visualização
    const preview = {
        title: document.getElementById("previewTitle"),
        date: document.getElementById("previewDate"),
        time: document.getElementById("previewTime"),
        location: document.getElementById("previewLocation"),
        description: document.getElementById("previewDescription"),
    };

    // Valores apresentados quando um campo está vazio
    const fallback = {
        title: "Título do evento",
        date: "Data a definir",
        time: "Hora a definir",
        location: "Local a definir",
        description: "",
    };

    /**
     * Atualiza um elemento da pré-visualização
     * sem interpretar o conteúdo como HTML.
     */
    function updateField(field, target, defaultValue, formatter = value => value) {
        if (!field || !target) return;

        const refresh = () => {
            const value = field.value.trim();

            target.textContent = value
                ? formatter(value)
                : defaultValue;
        };

        field.addEventListener("input", refresh);
        field.addEventListener("change", refresh);

        // Atualiza imediatamente ao abrir a página
        refresh();
    }

    // Título
    updateField(
        fields.title,
        preview.title,
        fallback.title
    );

    // Data: YYYY-MM-DD para DD/MM/YYYY
    updateField(
        fields.date,
        preview.date,
        fallback.date,
        value => {
            const match = value.match(/^(\d{4})-(\d{2})-(\d{2})$/);

            if (!match) return value;

            const [, year, month, day] = match;
            return `${day}/${month}/${year}`;
        }
    );

    // Hora
    updateField(
        fields.time,
        preview.time,
        fallback.time,
        value => {
            const match = value.match(/^(\d{2}):(\d{2})(?::\d{2})?$/);

            return match ? `${match[1]}:${match[2]}` : value;
        }
    );

    // Local do evento
    updateField(
        fields.location,
        preview.location,
        fallback.location
    );

    // Mensagem do convite
    updateField(
        fields.description,
        preview.description,
        fallback.description
    );

    // Evita que o formulário seja enviado acidentalmente
    // ao premir Enter em campos que não são áreas de texto.
    // O comportamento normal do formulário é preservado.
});
