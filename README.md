
# SIGED – Sistema Integrado de Gestão e Desenvolvimento

## 📑 Visão Geral
Este projeto visa centralizar e otimizar a gestão de diversas atividades, desde a organização de tarefas em um mural interativo até o gerenciamento completo de chamados, tudo isso integrado a um sistema de chat em tempo real.  
O **SIGED** é um ambiente de aprendizado e aprimoramento contínuo, focado em trazer funcionalidades que realmente fazem a diferença.

---

## 🚀 Funcionalidades Atuais

### ✅ Mural Interativo
- Crie e visualize **cards dinâmicos** em um mural intuitivo.
- Ideal para organizar tarefas e acompanhar o progresso visualmente, facilitando a colaboração em equipe ou pessoal.

### ✅ Gestão de Chamados com Dashboard Administrativo
- **Abertura e acompanhamento de chamados** de forma clara e organizada.
- **Dashboard completo**, com filtros inteligentes por status, setor e outras categorias, permitindo uma gestão eficiente dos chamados.

### ✅ Chat em Tempo Real (Inspirado no Zendesk)
- Comunicação em tempo real vinculada a um **ID de ticket específico**.
- Desenvolvido com **WebSockets e Daphne**, garantindo uma comunicação rápida, fluida e eficiente.

---

## 🛠️ Como Clonar e Rodar o SIGED Localmente

Siga este passo a passo para configurar e executar o projeto na sua máquina.

---

### 1️⃣ Pré-requisitos
Certifique-se de ter as seguintes ferramentas instaladas:

- **Python** (versão 3.9 ou superior): [Download Python](https://www.python.org)
- **Git**: [Download Git](https://git-scm.com)

---

### 2️⃣ Clonar o Repositório

Abra o terminal e execute:

```bash
git clone https://github.com/ranixx1/SIGED
```

---

### 3️⃣ Acessar o Diretório do Projeto

```bash
cd SIGED
```

---

### 4️⃣ Criar e Ativar um Ambiente Virtual

**Criar o ambiente virtual:**

```bash
python -m venv venv
```

**Ativar no Windows:**

```bash
.env\Scriptsctivate
```

**Ativar no macOS/Linux:**

```bash
source venv/bin/activate
```

---

### 5️⃣ Instalar as Dependências

Com o ambiente virtual ativado, execute:

```bash
pip install django pillow channels daphne
```

Ou, se houver um arquivo `requirements.txt` no projeto (recomendado):

```bash
pip install -r requirements.txt
```

---

### 6️⃣ Configurar o Banco de Dados

Execute as migrações:

```bash
python manage.py migrate
```

---

### 7️⃣ Criar um Superusuário (Opcional)

Para acessar o painel administrativo do Django:

```bash
python manage.py createsuperuser
```

Siga as instruções para definir nome, e-mail e senha.

---

### 8️⃣ Rodar o Servidor de Desenvolvimento

Execute:

```bash
python manage.py runserver
```

Acesse o projeto no navegador:  
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

