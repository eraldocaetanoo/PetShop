
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
  
document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.getElementById('menuToggle');
    const dropdownMenu = document.getElementById('menuItems');
    let hideTimeout;
  
    // Função para mostrar o menu
    function showMenu() {
      clearTimeout(hideTimeout); // cancela o atraso de esconder
      dropdownMenu.classList.add('show');
    }
  
    // Função para esconder o menu com atraso
    function hideMenu() {
      hideTimeout = setTimeout(() => {
        dropdownMenu.classList.remove('show');
      }, 500); // atraso para a transição suave
    }
  
    // Detecta toque (mobile)
    if (window.matchMedia("(hover: none) and (pointer: coarse)").matches) {
      menuToggle.addEventListener('click', function (e) {
        e.preventDefault();
        if (dropdownMenu.classList.contains('show')) {
          hideMenu();
        } else {
          showMenu();
        }
      });
  
      // Fecha o menu ao tocar fora (mobile)
      document.addEventListener('click', function (e) {
        if (!menuToggle.contains(e.target) && !dropdownMenu.contains(e.target)) {
          hideMenu();
        }
      });
    }
  
    // Eventos para desktop (hover com atraso ao sair)
    menuToggle.addEventListener('mouseenter', showMenu);
    dropdownMenu.addEventListener('mouseenter', showMenu);
  
    menuToggle.addEventListener('mouseleave', hideMenu);
    dropdownMenu.addEventListener('mouseleave', hideMenu);
  });
  

