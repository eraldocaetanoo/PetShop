
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
    if (menuToggle && dropdownMenu) {
      // Eventos para desktop (hover com atraso ao sair)
      menuToggle.addEventListener('mouseenter', showMenu);
      dropdownMenu.addEventListener('mouseenter', showMenu);
      
      menuToggle.addEventListener('mouseleave', hideMenu);
      dropdownMenu.addEventListener('mouseleave', hideMenu);
    }
});
  

document.addEventListener('DOMContentLoaded', function () {
  const menuDropdown = document.getElementById('menuDropdown');
  const menuItems = document.getElementById('menuItems');

  menuDropdown.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault(); // impede scroll da página com espaço
      menuItems.classList.toggle('show'); // alterna o menu
    }
  });

  menuDropdown.addEventListener('click', function () {
    menuItems.classList.toggle('show');
  });
});


document.addEventListener('DOMContentLoaded', function () {

  let debounceTimeout;

  const ids = ['login', 'masterLogin'];
  ids.forEach(id => {
    const el = document.getElementById(id);
      if (el) {
          el.addEventListener('input', function () {
            
            clearTimeout(debounceTimeout); // Limpa o último timeout

            const login = this.value;
            const feedback = document.getElementById('login-feedback');
        
            if (login.length < 3) {
                feedback.textContent = 'Digite pelo menos 3 caracteres.';
                feedback.style.color = 'gray';
                return;
            }
        
            debounceTimeout = setTimeout(() => {
                fetch('/verificar_login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ login: login })
                })
                .then(response => response.json())
                .then(data => {
                    feedback.textContent = data.mensagem;
                    feedback.style.color = data.disponivel ? 'green' : 'red';
                })
                .catch(error => {
                    feedback.textContent = 'Erro ao verificar login.';
                    feedback.style.color = 'gray';
                });
            }, 500); // Aguarda 500ms antes de enviar a requisição


          });
      }


  });
});



document.addEventListener('DOMContentLoaded', function () {

  // Formatação de telefone
  document.getElementById("telefone").addEventListener("input", function (e) {
    let value = e.target.value.replace(/\D/g, "");

    // Se não tem nenhum número, não mostra nada
    if (value.length === 0) {
      e.target.value = "";
      return;
    }

    // Limita ao máximo de 11 dígitos
    if (value.length > 11) value = value.slice(0, 11);

    // Formata conforme o número de dígitos
    if (value.length >= 11) {
      value = value.replace(/^(\d{2})(\d{5})(\d{4})/, "($1) $2-$3");
    } else if (value.length >= 10) {
      value = value.replace(/^(\d{2})(\d{4})(\d{4})/, "($1) $2-$3");
    } else if (value.length >= 3) {
      value = value.replace(/^(\d{2})(\d{0,5})/, "($1) $2");
    } else {
      value = value.replace(/^(\d{0,2})/, "($1");
    }

    e.target.value = value;
  });

  // Formatação de CEP
  document.getElementById("cep").addEventListener("input", function (e) {
    let value = e.target.value.replace(/\D/g, ""); // Remove qualquer caractere que não seja número

    // Se não tem nenhum número, não mostra nada
    if (value.length === 0) {
      e.target.value = "";
      return;
    }

    // Limita ao máximo de 8 dígitos (CEP no Brasil tem 8 números)
    if (value.length > 8) value = value.slice(0, 8);

    // Formata o CEP como 'xxxxx-xxx'
    if (value.length >= 5) {
      value = value.replace(/^(\d{5})(\d{0,3})/, "$1-$2");
    }

    e.target.value = value;
  });


});

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById("preco").addEventListener("input", function (e) {
    let value = e.target.value.replace(/\D/g, "");
    value = (value / 100).toFixed(2);
    value = value.replace(".", ",");
    value = value.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    e.target.value = "R$ " + value;
  });
});


document.addEventListener('DOMContentLoaded', function () {
  const selects = document.querySelectorAll('.custom-select-cor');

  selects.forEach(function (select) {
    select.addEventListener('change', function () {
      if (this.value) {
        this.classList.add('valid-option');
      } else {
        this.classList.remove('valid-option');
      }
    });
  });

});


document.addEventListener('DOMContentLoaded', function () {
  const racasPorEspecie = {
    "Cachorro": [
      "Vira-lata", "Labrador Retriever", "Poodle", "Bulldog", "Shih Tzu", "Pinscher", "Golden Retriever", "Pastor Alemão", "Beagle", "Yorkshire Terrier"
    ],
    "Gato": [
      "Persa", "Siamês", "Maine Coon", "Sphynx", "Angorá", "Bengal", "Ragdoll", "SRD"
    ],
    "Pássaro": [
      "Calopsita", "Periquito", "Canário", "Papagaio", "Agapornis", "Arara"
    ],
    "Roedor": [
      "Hamster", "Porquinho-da-Índia", "Chinchila", "Rato", "Gerbil"
    ],
    "Réptil": [
      "Jabuti", "Iguana", "Gecko", "Teiú", "Corn Snake", "Python", "Cobra"
    ],
    "Peixe": [
      "Betta", "Kinguios", "Neon", "Oscar", "Platy", "Acará-bandeira", "Disco"
    ],
    "Outro": [
      "Outro"
    ]
  };

  const especieSelect = document.getElementById("especie");
  const racaSelect = document.getElementById("raca");

  especieSelect.addEventListener("change", function () {
    const especieSelecionada = this.value;
    const racas = racasPorEspecie[especieSelecionada] || [];

    // Limpa o select de raças
    racaSelect.innerHTML = '<option value="">Selecione a raça</option>';

    // Adiciona as opções da raça conforme a espécie
    racas.forEach(raca => {
      const option = document.createElement("option");
      option.value = raca;
      option.textContent = raca;
      racaSelect.appendChild(option);
    });
  });

});


document.addEventListener('DOMContentLoaded', function () {
  document.getElementById("animalPeso").addEventListener("input", function (e) {
    // Substitui vírgula por ponto automaticamente
    e.target.value = e.target.value.replace(",", ".");
  });
});


// Campo/resultados de pesquisa

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('pesquisaUsuarios').addEventListener('input', function () {
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll('#tabelaUsuarios tbody tr');

    rows.forEach(row => {
        const rowText = row.innerText.toLowerCase();
        row.style.display = rowText.includes(searchTerm) ? '' : 'none';
    });
  }); 
});