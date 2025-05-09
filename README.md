# Projeto Simulador de Elevador com AFD

Este projeto simula o comportamento de um elevador utilizando um Autômato Finito Determinístico (AFD). A interface web permite a interação com o elevador e visualiza o estado atual do AFD em tempo real.

## Estrutura do Projeto

- `elevator_sim/` (Pasta principal do projeto)
    - `index.html`: Arquivo principal da interface do usuário (frontend).
    - `style.css`: Folha de estilos para a interface.
    - `script.js`: Lógica do frontend em JavaScript, incluindo a comunicação com o backend, o controle das animações e a visualização do AFD.
    - `apresentacao_elevador_afd.md`: Documento Markdown com a apresentação detalhada do projeto, incluindo a modelagem do AFD e a explicação da implementação.
    - `README.md`: Este arquivo, com instruções de execução e visão geral.
    - `backend/`:
        - `src/`:
            - `main.py`: Implementação do AFD em Python com Flask, expondo a API para o frontend.
            - `models/` (vazio, estrutura para futura expansão)
            - `routes/` (vazio, estrutura para futura expansão)
        - `requirements.txt`: Dependências Python para o backend.
        - `venv/` (Ambiente virtual Python - não incluído no zip, deve ser recriado).
- `todo.md`: (Fora da pasta `elevator_sim` no ambiente de desenvolvimento, mas incluído no zip para referência do processo) Lista de tarefas e acompanhamento do desenvolvimento.
- `Case 2- Elevador.pdf`: (Documento original de requisitos, incluído no zip para referência).

## Como Executar

### Pré-requisitos

- Python 3.9 ou superior
- Navegador web moderno (Chrome, Firefox, Edge, etc.)

### 1. Backend (Servidor Flask)

   a. Navegue até a pasta `elevator_sim/backend`:
      ```bash
      cd /caminho/para/o/projeto/elevator_sim/backend
      ```

   b. Crie e ative um ambiente virtual (recomendado):
      ```bash
      python3 -m venv venv
      source venv/bin/activate  # No Linux/macOS
      # .\venv\Scripts\activate    # No Windows (PowerShell)
      # venv\Scripts\activate     # No Windows (CMD)
      ```

   c. Instale as dependências:
      ```bash
      pip install -r requirements.txt
      ```

   d. Execute o servidor Flask (a partir da pasta `elevator_sim/backend`):
      ```bash
      python src/main.py
      ```
      O servidor estará rodando em `http://localhost:5001`. Você verá logs no terminal indicando que o servidor iniciou e as requisições recebidas.

### 2. Frontend (Interface Web)

   a. Abra o arquivo `index.html` (localizado na pasta `elevator_sim`) em um navegador web.
      - Exemplo: `file:///caminho/para/o/projeto/elevator_sim/index.html`

   b. Interaja com a simulação:
      - Clique em "Case 2: Elevador" no menu inicial.
      - Use os botões no painel do elevador (T, 1, 2, 3) para chamar o elevador para os andares desejados.
      - Observe a animação do elevador, o indicador de andar, a descrição do estado atual do AFD e a lista de estados do AFD com o estado atual destacado.

## Apresentação

O arquivo `apresentacao_elevador_afd.md` contém os slides e o roteiro para a apresentação do projeto, detalhando a modelagem do AFD, a implementação e o funcionamento da simulação.

## Funcionalidades Implementadas

- Simulação de um elevador com Térreo + 3 andares.
- Painel de botões para chamar o elevador.
- Animação do movimento do elevador e abertura/fechamento de portas.
- Exibição do andar atual e do estado descritivo do elevador.
- Lógica de AFD no backend (Python/Flask) para controlar o comportamento do elevador.
- Comunicação Frontend-Backend via API RESTful.
- Visualização dinâmica e simplificada dos estados do AFD na interface, destacando o estado atual.
- Loop de simulação automático que avança o estado do elevador periodicamente.
- Botão de reset para reiniciar a simulação (via seleção do "Case 2").

