
document.addEventListener('DOMContentLoaded', function () {


    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });


    const toggleSwitch = document.getElementById("toggleTheme");
    const themeIcon = document.getElementById("themeIcon");
    const body = document.body;

    // Verifica se o tema escuro já está salvo
    const darkModeAtivado = localStorage.getItem("modo-escuro");

    if (darkModeAtivado === "true") {
        body.classList.add("dark-mode");
        toggleSwitch.checked = true;
        themeIcon.classList.replace("fa-sun", "fa-moon"); // Ícone de sol no modo escuro
    }

    toggleSwitch.addEventListener("change", function () {
        body.classList.toggle("dark-mode");

        const modoAtual = body.classList.contains("dark-mode");
        localStorage.setItem("modo-escuro", modoAtual);

        // Troca o ícone
        if (modoAtual) {
        themeIcon.classList.replace("fa-sun", "fa-moon");
        } else {
        themeIcon.classList.replace("fa-moon", "fa-sun");
        }

        // Esconde o tooltip depois de clicar
        const tooltipInstance = bootstrap.Tooltip.getInstance(toggleSwitch.parentElement);
        if (tooltipInstance) {
            tooltipInstance.hide();
        }

    });
});
  
