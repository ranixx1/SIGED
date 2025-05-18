document.addEventListener('DOMContentLoaded', function () {
    // Setores disponíveis com ícones
    const setores = [
        { id: 'ti', nome: 'Tecnologia da Informação', icon: 'bi-laptop' },
        { id: 'rh', nome: 'Recursos Humanos', icon: 'bi-people' },
        { id: 'financeiro', nome: 'Financeiro', icon: 'bi-cash-stack' },
        { id: 'manutencao', nome: 'Manutenção', icon: 'bi-tools' },
        { id: 'limpeza', nome: 'Limpeza', icon: 'bi-trash' },
        { id: 'outro', nome: 'Outro', icon: 'bi-grid' }
    ];

    const setoresGrid = document.getElementById('setores-grid');
    const formContainer = document.getElementById('form-container');
    const setoresContainer = document.getElementById('setores-container');
    const setorSelecionadoText = document.getElementById('setor-selecionado-text');
    const voltarBtn = document.getElementById('voltar-btn');
    const chamadoForm = document.getElementById('chamado-form');

    setores.forEach(setor => {
        const setorElement = document.createElement('div');
        setorElement.className = 'setor-card';
        setorElement.setAttribute('data-setor-id', setor.id);
        setorElement.innerHTML = `
            <div class="card-body d-flex flex-column align-items-center justify-content-center">
                <i class="bi ${setor.icon}"></i>
                <h5 class="card-title mt-2">${setor.nome}</h5>
            </div>
        `;
        setoresGrid.appendChild(setorElement);
    });
    // Adicionar evento de clique nos cards
    document.querySelectorAll('.setor-card').forEach(card => {
        card.addEventListener('click', function () {
            const setId = this.getAttribute('data-setor-id');
            const setor = setores.find(s => s.id === setId);

            // Mostrar formulário
            setorSelecionadoText.textContent = `Setor: ${setor.nome}`;
            setoresContainer.style.display = 'none';
            formContainer.style.display = 'block';
        });
    });

    // Botão voltar
    voltarBtn.addEventListener('click', function (e) {
        e.preventDefault();
        formContainer.style.display = 'none';
        setoresContainer.style.display = 'block';
    });

    // Envio do formulário
    chamadoForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = {
            setor: setorSelecionadoText.textContent.replace('Setor: ', ''),
            assunto: document.getElementById('assunto').value,
            descricao: document.getElementById('descricao').value,
            urgencia: document.getElementById('urgencia').value
        };

        // Aqui você pode enviar os dados para o backend
        console.log('Dados do chamado:', formData);

        // Exemplo de feedback para o usuário
        alert('Chamado enviado com sucesso!');
        chamadoForm.reset();
        formContainer.style.display = 'none';
        setoresContainer.style.display = 'block';
    });
});