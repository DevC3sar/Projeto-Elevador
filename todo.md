# Lista de Tarefas do Projeto Elevador AFD

## Fase 1: Planejamento e Estruturação

- [X] **1.1. Análise Detalhada dos Requisitos:** Revisar o documento "Case 2- Elevador.pdf" para garantir a compreensão completa de todos os requisitos funcionais e não funcionais. (Em progresso, requisitos básicos entendidos e sendo implementados)
- [ - [X] **1.2. Definição do Autômato Finito Determinístico (AFD):** (Revisando e detalhando para visualização)
    - [X] 1.2.1. Definir os estados do AFD (ex: ParadoPortaAberta_Terreo, Movendo_Subindo_Entre_T_e_1, ParadoPortaFechada_1Andar, etc.).
    - [X] 1.2.2. Definir o alfabeto (entradas) do AFD (ex: Botao_Andar_X, Sensor_Chegada_Andar_Y, Temporizador_Porta_Fechada).
    - [X] 1.2.3. Definir as transições de estado.
    - [X] 1.2.4. Definir o estado inicial (ParadoPortaAberta_Terreo, conforme PDF).
    - [X] 1.2.5. Definir os estados finais (se aplicável, ou estados de aceitação para certas operações).
    - [X] 1.2.6. Criar um diagrama visual do AFD (para apresentação e possivelmente na interface).
    - [X] **1.2.7. Implementar visualização dinâmica do AFD na interface da simulação.** (NOVA TAREFA - CONCLUÍDA)
- [X] **1.3. Planejamento da Interface e Animação:**
    - [X] 1.3.1. Esboçar a interface do usuário (HTML/CSS), incluindo o menu de seleção (Case 1 vs Case 2) e a visualização do elevador.
    - [X] 1.3.2. Definir os elementos da animação (elevador, portas, indicadores de andar, botões).
    - [X] 1.3.3. Planejar a lógica da animação em JavaScript para refletir os estados do AFD.
- [X] **1.4. Estrutura do Projeto:**
    - [X] 1.4.1. Definir a estrutura de pastas e arquivos para o projeto (HTML, CSS, JS, Python, assets).

## Fase 2: Desenvolvimento do Back-end (Lógica do AFD)

- [X] **2.1. Implementação do AFD em Python:** (Revisando e corrigindo funcionalidade)
    - [X] 2.1.1. Criar classes ou estruturas de dados para representar estados, transições e o AFD em si.
    - [X] 2.1.2. Implementar a lógica de transição de estados. (Revisado e corrigido)
    - [X] 2.1.3. Desenvolver uma API (Flask) para que o front-end possa interagir com o AFD.
    - [X] 2.1.4. Implementar a lógica para o elevador atender térreo + 3 andares, movimento linear, e controle de portas. (Revisado e corrigido)
- [X] **2.2. Testes da Lógica do AFD:**
    - [ ] 2.2.1. Criar testes unitários para a lógica do AFD em Python. (Pendente - Foco na funcionalidade e apresentação visual primeiro)
    - [X] **2.2.2. Adicionar logging detalhado para depuração.** (NOVA TAREFA - CONCLUÍDA)

## Fase 3: Desenvolvimento do Front-end (Interface e Animação)

- [X] **3.1. Desenvolvimento da Estrutura HTML:**
    - [X] 3.1.1. Criar o arquivo `index.html`.
    - [X] 3.1.2. Implementar o menu de seleção (Case 1 / Case 2).
    - [X] 3.1.3. Estruturar os elementos visuais do elevador (painel de botões, display de andar, representação do elevador e portas).
- [X] **3.2. Estilização com CSS:**
    - [X] 3.2.1. Criar o arquivo `style.css`.
    - [X] 3.2.2. Estilizar o menu e a interface do elevador para ser visualmente agradável e clara.
    - [X] 3.2.3. Garantir responsividade básica.
- [X] **3.3. Implementação da Animação e Interação com JavaScript:** (Revisando e corrigindo funcionalidade)
    - [X] 3.3.1. Criar o arquivo `script.js`.
    - [X] 3.3.2. Implementar a lógica para exibir o estado atual do elevador (andar, portas). (Revisado e corrigido)
    - [X] 3.3.3. Criar as animações de movimento do elevador entre andares.
    - [X] 3.3.4. Criar as animações de abertura e fechamento das portas.
    - [X] 3.3.5. Implementar a interatividade dos botões do painel do elevador (chamada para andares). (Revisado e corrigido)
    - [X] 3.3.6. Implementar a comunicação com o back-end Python (via API) para enviar comandos e receber atualizações de estado. (Revisado e corrigido)
    - [X] **3.3.7. Implementar a visualização do diagrama/estados do AFD no frontend.** (NOVA TAREFA - CONCLUÍDA)

## Fase 4: Integração e Testes

- [X] **4.1. Integração Front-end e Back-end:** (Revisando e corrigindo)
    - [X] 4.1.1. Garantir que o JavaScript consiga se comunicar com a API Python corretamente.
    - [X] 4.1.2. Assegurar que as ações no front-end disparem as transições corretas no AFD do back-end.
    - [X] 4.1.3. Garantir que as atualizações de estado do AFD no back-end sejam refletidas corretamente na animação do front-end.
- [X] **4.2. Testes Funcionais e de Usabilidade:**
    - [X] 4.2.1. Testar todos os cenários de uso do elevador (chamadas para todos os andares, de todos os andares).
    - [X] 4.2.2. Verificar a corretude da animação em relação ao estado do AFD.
    - [X] 4.2.3. Avaliar a clareza da interface e da demonstração do AFD.
    - [X] 4.2.4. Testar o menu de seleção.
    - [X] **4.2.5. Validar a visualização dinâmica do AFD.** (NOVA TAREFA - CONCLUÍDA)

## Fase 5: Criação da Apresentação

- [ ] **5.1. Roteiro da Apresentação:**
    - [ ] 5.1.1. Definir os tópicos a serem abordados (introdução, descrição do problema, o AFD modelado, a implementação, a demonstração, conclusões).
- [ ] **5.2. Criação dos Slides/Material de Apoio:**
    - [ ] 5.2.1. Desenvolver slides claros e objetivos.
    - [ ] 5.2.2. Incluir o diagrama do AFD.
    - [ ] 5.2.3. Preparar capturas de tela ou um vídeo curto da animação funcionando.
- [ ] **5.3. Preparação da Demonstração ao Vivo:**
    - [ ] 5.3.1. Garantir que o projeto esteja funcional para uma demonstração.
    - [ ] 5.3.2. Praticar a apresentação explicando o funcionamento do AFD e da animação.

## Fase 6: Finalização e Entrega

- [ ] **6.1. Revisão Final do Projeto:**
    - [ ] 6.1.1. Verificar se todos os requisitos do PDF foram atendidos.
    - [ ] 6.1.2. Revisar o código (Python, JS, HTML, CSS) para clareza e boas práticas.
    - [ ] 6.1.3. Verificar a qualidade da animação e a didática da apresentação.
- [ ] **6.2. Preparação dos Arquivos para Entrega:**
    - [ ] 6.2.1. Organizar todos os arquivos do projeto (código fonte, assets, etc.).
    - [ ] 6.2.2. (Opcional, se solicitado) Criar um `README.md` com instruções de execução.
- [ ] **6.3. Entrega do Projeto ao Usuário:**
    - [ ] 6.3.1. Enviar todos os arquivos do projeto.
    - [ ] 6.3.2. Enviar o material da apresentação.


