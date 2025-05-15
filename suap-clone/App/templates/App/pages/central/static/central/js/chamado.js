document.addEventListener('DOMContentLoaded', function() {
    // Setores disponíveis
    const setores = [
        { id: 'ti', nome: 'Tecnologia da Informação', cor: '#4e73df' },
        { id: 'rh', nome: 'Recursos Humanos', cor: '#1cc88a' },
        { id: 'financeiro', nome: 'Financeiro', cor: '#36b9cc' },
        { id: 'manutencao', nome: 'Manutenção', cor: '#f6c23e' },
        { id: 'limpeza', nome: 'Limpeza', cor: '#e74a3b' },
        { id: 'outros', nome: 'Outros', cor: '#858796' }
    ];

    const setoresGrid = document.getElementById('setores-grid');
    const formContainer = document.getElementById('form-container');
    const setoresContainer = document.getElementById('setores-container');
    const setorSelecionadoText = document.getElementById('setor-selecionado-text');
    const voltarBtn = document.getElementById('voltar-btn');
    const chamadoForm = document.getElementById('chamado-form');

    // Criar os quadrados dos setores
    setores.forEach(setor => {
        const setorElement = document.createElement('div');
        setorElement.className = 'col-md-4 mb-4';
        setorElement.innerHTML = `
            <div class="card setor-card" data-setor-id="${setor.id}" 
                 style="background-color: ${setor.cor}; cursor: pointer;">
                <div class="card-body text-center text-white">
                    <h5 class="card-title">${setor.nome}</h5>
                </div>
            </div>
        `;
        setoresGrid.appendChild(setorElement);
    });

    // Adicionar evento de clique nos cards
    document.querySelectorAll('.setor-card').forEach(card => {
        card.addEventListener('click', function() {
            const setId = this.getAttribute('data-setor-id');
            const setor = setores.find(s => s.id === setId);
            
            // Mostrar formulário
            setorSelecionadoText.textContent = `Setor: ${setor.nome}`;
            setoresContainer.style.display = 'none';
            formContainer.style.display = 'block';
        });
    });

    // Botão voltar
    voltarBtn.addEventListener('click', function(e) {
        e.preventDefault();
        formContainer.style.display = 'none';
        setoresContainer.style.display = 'block';
    });

    // Envio do formulário
    chamadoForm.addEventListener('submit', function(e) {
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