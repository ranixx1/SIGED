isão Geral
Este projeto visa centralizar e otimizar a gestão de diversas atividades, desde a organização de tarefas em um mural interativo até o gerenciamento completo de chamados, tudo isso integrado a um sistema de chat em tempo real. O SIGED é um ambiente de aprendizado e aprimoramento contínuo, focado em trazer funcionalidades que realmente façam a diferença.

Funcionalidades Atuais
Conheça as principais funcionalidades já implementadas no SIGED:

Mural Interativo
Crie e visualize cards dinâmicos em um mural intuitivo. Essa ferramenta é perfeita para organizar tarefas e acompanhar o progresso visualmente, facilitando a colaboração e a organização pessoal ou em equipe.

Gestão de Chamados com Dashboard Administrativo
Visualização Detalhada: Abra e acompanhe chamados de forma clara e organizada, garantindo que nenhum pedido passe despercebido.
Dashboard Administrativo: Acesse um painel completo com filtros inteligentes por status, setor e outras categorias. Isso simplifica a gestão e o acompanhamento dos chamados, proporcionando uma visão rápida do cenário.
Chat em Tempo Real (Inspirado no Zendesk)
Comunicação Eficiente: Um sistema de chat robusto, desenvolvido com referência no Zendesk, que permite a comunicação em tempo real vinculada a um ID de ticket específico. Isso otimiza o suporte e a resolução de problemas.
Tecnologia de Ponta: Implementado utilizando WebSockets e a biblioteca Daphne, garantindo uma comunicação rápida, fluida e eficiente. Este recurso está em constante aprimoramento para oferecer a melhor experiência.
Como Clonar e Rodar o SIGED Localmente
Siga este passo a passo para configurar e executar o projeto em sua máquina. Para um funcionamento adequado, verifique os pré-requisitos antes de começar.

1. Pré-requisitos
Certifique-se de ter as seguintes ferramentas instaladas em seu ambiente:

Python: Recomenda-se a versão 3.9 ou superior. Você pode baixá-lo diretamente do site oficial: python.org.
Git: Ferramenta essencial para controle de versão. Baixe e instale-o através do site oficial: git-scm.com.
2. Clonar o Repositório
Abra seu terminal ou prompt de comando e execute o seguinte comando para clonar o projeto:

Bash

git clone https://github.com/ranixx1/SIGED
3. Navegar até o Diretório do Projeto
Após a clonagem, acesse a pasta do projeto:

Bash

cd SIGED
4. Criar e Ativar um Ambiente Virtual
É uma boa prática criar um ambiente virtual para isolar as dependências do projeto, evitando conflitos com outras instalações Python.

Bash

python -m venv venv
Para ativar o ambiente virtual:

No Windows:
Bash

.\venv\Scripts\activate
No macOS/Linux:
Bash

source venv/bin/activate
5. Instalar as Dependências
Com o ambiente virtual ativado, instale todas as bibliotecas Python necessárias para o projeto.

Recomendado: Se você já tem um requirements.txt no projeto:


Bash

pip install django
pip install pillow
pip install channels daphne



6. Configurar o Banco de Dados
O Django utiliza um banco de dados para armazenar informações. Para desenvolvimento local, o SQLite (já incluído no Django) é uma excelente opção.

Execute as migrações para criar as tabelas necessárias no banco de dados:

Bash

python manage.py migrate
7. Criar um Superusuário (Opcional)
Para acessar o painel administrativo do Django e gerenciar o conteúdo do projeto, você pode criar um superusuário:

Bash

python manage.py createsuperuser
Siga as instruções no terminal para definir um nome de usuário, endereço de e-mail e senha.

8. Rodar o Servidor de Desenvolvimento
Por fim, inicie o servidor de desenvolvimento do Django para ver o SIGED em ação:

Bash

python manage.py runserver
Após a execução bem-sucedida, o projeto estará acessível no seu navegador, geralmente em http://127.0.0.1:8000/.
