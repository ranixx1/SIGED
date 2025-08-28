### 1. Autenticação e Gestão de Usuários
* **Cadastro de Usuários:** Permite que novos usuários se registrem no sistema.
* **Login e Logout:** Gerenciamento de sessão de usuário.
* **Segurança Básica:** Validação de senha no backend e autenticação de usuários.

### 2. Mural Interativo
* **Visualização de Cards:** Exibe cards com avisos e informações.
* **Adicionar Card (Admin-only):** Formulário dedicado para administradores criarem novos cards.
    * Página de criação (`/home/cards/novo/`) com visual consistente e centralizado.
    * Link "Adicionar Card" na sidebar, visível apenas para admins.
* **Editar Card (Admin-only):** Permite a edição de cards existentes.
    * Link de edição em cada card no mural (visível apenas para admins).
    * Página de edição (`/home/cards/editar/<id>/`) com visual consistente e centralizado.
* **Remover Card:** Funcionalidade de exclusão de cards diretamente do mural.
* **Arrastar e Soltar:** Cards no mural podem ser reorganizados via drag-and-drop.

### 3. Central de Serviços (Chamados)
* **Abertura de Chamados:** Usuários podem abrir chamados selecionando um setor e preenchendo detalhes.
* **Visualização de Meus Chamados:** Usuários podem ver o status e detalhes dos seus próprios chamados.
* **Detalhamento de Chamados:** Visualização detalhada de um chamado específico.
* **Gerenciamento de Chamados (Admin):** Administradores podem visualizar e atualizar chamados no painel Django Admin.

### 4. Dashboard Administrativo
* **Página Exclusiva para Admins:** Um dashboard (`/home/dashboard-admin/`) que exibe métricas e informações importantes do sistema, acessível apenas por usuários com permissões de equipe (`is_staff`).
* **Métricas Iniciais:** Exibe total de chamados, chamados abertos e resolvidos, e últimas mensagens do chat.
* **Link na Sidebar:** Acesso direto via sidebar, visível apenas para usuários administradores.

### 5. Design e Layout
* **Sidebar Responsiva:** Sidebar com funcionalidade de expandir/colapsar.
* **Consistência Visual:** Layout padronizado através de um `base.html` com estilos Tailwind CSS, aplicado a diversas páginas (login, cadastro, criar/editar/deletar card, dashboard).

---

## Como Rodar o Projeto (Ambiente de Desenvolvimento)

1.  **Clone o repositório:**
    ```bash
    git clone https://GitHub.com/ranixx1/siged
    cd siged
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv .venv
    # No Linux/macOS:
    source .venv/bin/activate
    # No Windows (CMD):
    .venv\Scripts\activate.bat
    # No Windows (PowerShell):
    .\.venv\Scripts\Activate.ps1
    ```
3.  **Instale as dependências:**
    ```bash
    pip install django daphne
    ```
4.  **Configure o arquivo `.env`:**
    Crie um arquivo `.env` na raiz do projeto (`suap-clone/.env`) e adicione suas chaves de API (se for usar IA no futuro):
    ```
    GEMINI_API_KEY=SUA_CHAVE_DE_API_AQUI # Exemplo, se for integrar IA
    ```
5.  **Aplique as migrações do banco de dados:**
    ```bash
    python manage.py makemigrations App usuarios
    python manage.py migrate
    ```
6.  **Crie um superusuário (para acesso ao admin e dashboard):**
    ```bash
    python manage.py createsuperuser
    ```

    ```
7.  **Inicie o servidor Django:**
    Abra outro terminal e execute:
    ```bash
    python manage.py runserver
    ```
    O sistema estará acessível em `http://127.0.0.1:8000/`.

---
