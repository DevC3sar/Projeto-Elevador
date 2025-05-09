# Apresentação do Projeto: Simulador de Elevador com AFD

## 1. Introdução

Este projeto apresenta a concepção e implementação de um simulador de elevador baseado em um Autômato Finito Determinístico (AFD). O objetivo principal é demonstrar de forma clara e didática o funcionamento de um AFD aplicado a um sistema do mundo real, como um elevador, utilizando tecnologias web modernas para a interface e animação (HTML, CSS, JavaScript) e Python com Flask para a lógica do backend.

A simulação permite ao usuário interagir com o elevador, chamando-o para diferentes andares, e observar não apenas o movimento físico do elevador e o estado de suas portas, mas também a transição entre os estados do AFD que governam seu comportamento. Uma visualização dinâmica do AFD é integrada à interface para facilitar a compreensão.

## 2. Descrição do Problema (Baseado no "Case 2: Elevador.pdf")

O desafio proposto consiste em modelar e simular o comportamento de um elevador que atende a um edifício com térreo e mais três andares (totalizando 4 níveis: T, 1, 2, 3).

As principais funcionalidades e restrições incluem:

*   **Movimentação:** O elevador deve ser capaz de se mover para cima e para baixo entre os andares.
*   **Chamadas:** Usuários podem chamar o elevador para qualquer andar através de um painel de botões.
*   **Portas:** O elevador possui portas que abrem ao chegar a um andar de destino e fecham antes de iniciar um novo movimento.
*   **Estado Inicial:** A simulação deve iniciar com o elevador no térreo, com as portas abertas.
*   **Lógica de Atendimento:** O elevador deve processar as chamadas de forma lógica (neste projeto, foi implementada uma fila FIFO simples para chamadas pendentes).

## 3. Modelagem do Autômato Finito Determinístico (AFD)

O comportamento do elevador é modelado por um Autômato Finito Determinístico. Um AFD é definido por uma 5-tupla (Q, Σ, δ, q0, F):

*   **Q (Conjunto de Estados):** Representa as diferentes situações em que o elevador pode se encontrar. Para esta simulação, os estados principais podem ser categorizados como:
    *   `PARADO_PORTA_ABERTA_ANDAR_X`: Elevador parado no andar X com portas abertas.
    *   `PARADO_PORTA_FECHADA_ANDAR_X`: Elevador parado no andar X com portas fechadas.
    *   `MOVENDO_PARA_CIMA_ENTRE_X_Y`: Elevador se movendo para cima, entre o andar X e o andar Y (ou em direção a um andar superior).
    *   `MOVENDO_PARA_BAIXO_ENTRE_X_Y`: Elevador se movendo para baixo, entre o andar X e o andar Y (ou em direção a um andar inferior).

    Na implementação do backend, o estado é uma combinação de `current_floor`, `door_status` ("OPEN"/"CLOSED"), e `movement_status` ("STOPPED", "MOVING_UP", "MOVING_DOWN"). A visualização no frontend simplifica isso em nomes mais descritivos.

*   **Σ (Alfabeto de Entrada):** Representa os eventos que podem causar uma mudança de estado. Na prática da simulação, as entradas são:
    *   `CHAMADA_ANDAR_N`: Um botão é pressionado para chamar o elevador para o andar N.
    *   `TIMER_STEP_SIMULACAO`: Um evento periódico que faz o elevador avançar em sua lógica (mover um andar, abrir/fechar porta se necessário).

*   **δ (Função de Transição):** Define para qual próximo estado o autômato transita, dado o estado atual e um símbolo de entrada. Exemplos de transições (simplificado):
    *   Se (Estado = `PARADO_PORTA_ABERTA_ANDAR_X`, Entrada = `CHAMADA_ANDAR_Y` onde Y != X):
        *   Primeiro, a porta fecha: Transita para `PARADO_PORTA_FECHADA_ANDAR_X`.
        *   Depois, inicia o movimento: Transita para `MOVENDO_PARA_CIMA_ENTRE_X_Y` (se Y > X) ou `MOVENDO_PARA_BAIXO_ENTRE_X_Y` (se Y < X).
    *   Se (Estado = `MOVENDO_PARA_CIMA_ENTRE_A_B`, Entrada = `TIMER_STEP_SIMULACAO`, Destino = Y):
        *   Se o próximo andar é Y: Transita para `PARADO_PORTA_ABERTA_ANDAR_Y` (após parar e abrir a porta).
        *   Se o próximo andar não é Y: Continua em `MOVENDO_PARA_CIMA_ENTRE_B_C` (atualiza o andar atual).
    *   A lógica detalhada está implementada na função `step_simulation` e `call_elevator` no backend.

*   **q0 (Estado Inicial):** `PARADO_PORTA_ABERTA_ANDAR_0` (Térreo, portas abertas).

*   **F (Conjunto de Estados Finais):** Para um elevador, não há um "estado final" no sentido tradicional de aceitação de uma linguagem. Todos os estados operacionais são válidos. Poderíamos considerar estados de "tarefa concluída" aqueles onde o elevador está parado em um andar solicitado com a porta aberta.

### Visualização do AFD na Simulação

A interface do simulador inclui uma seção que lista os principais estados do AFD e destaca o estado ativo no momento, fornecendo uma descrição textual. Isso ajuda a correlacionar a animação visual do elevador com o estado lógico do autômato.

*(Captura de tela da interface mostrando o elevador e a visualização do AFD seria inserida aqui em uma apresentação real)*

## 4. Implementação

O projeto é dividido em duas partes principais: o frontend (interface do usuário e animação) e o backend (lógica do AFD e API).

### 4.1. Frontend (HTML, CSS, JavaScript)

*   **HTML (`index.html`):** Estrutura a página, incluindo a área do edifício com os andares, o poço do elevador, o carro do elevador, o painel de controle com botões de chamada, e a área de exibição de status e visualização do AFD.
*   **CSS (`style.css`):** Estiliza todos os elementos visuais, define as animações básicas de movimento do elevador e abertura/fechamento das portas (usando transições CSS).
*   **JavaScript (`script.js`):
    *   Manipula os eventos de clique nos botões de chamada.
    *   Comunica-se com a API do backend para enviar chamadas e solicitar atualizações de estado.
    *   Atualiza a interface do usuário (posição do elevador, indicador de andar, estado das portas, descrição do estado do AFD) com base nos dados recebidos do backend.
    *   Controla um loop de simulação que periodicamente chama a API do backend para avançar a lógica do elevador (função `stepSimulationAPI`).
    *   Renderiza a visualização simplificada do AFD, destacando o estado atual.

### 4.2. Backend (Python com Flask)

*   **`main.py`:**
    *   Utiliza o microframework Flask para criar uma API RESTful.
    *   Implementa a lógica do AFD do elevador.
        *   `elevator_state`: Um dicionário Python que armazena o estado atual do elevador (andar, status da porta, status de movimento, andar de destino, fila de chamadas).
        *   Funções para manipular o estado: `call_elevator()`, `step_simulation()`, `process_next_in_queue()`, `reset_simulation_api()`.
    *   **Endpoints da API:**
        *   `GET /api/elevator/status`: Retorna o estado atual completo do elevador.
        *   `POST /api/elevator/call`: Recebe uma chamada para um andar específico, adiciona à fila e atualiza o estado.
        *   `POST /api/elevator/step`: Avança a simulação em um passo lógico (movimento, operação de porta).
        *   `POST /api/elevator/reset`: Reinicia a simulação para o estado inicial.
    *   Utiliza `flask_cors` para permitir requisições do frontend.
    *   Inclui logging detalhado para facilitar a depuração e o acompanhamento do comportamento do AFD.

### Diagrama de Interação Simplificado

```
Usuário (Browser)         Frontend (JS)           Backend (Python/Flask)
-----------------         ---------------           ----------------------
Clica Botão Andar X  -->  callElevator(X)
                             | 
                             V
                         POST /api/elevator/call {floor: X}
                                                       |
                                                       V
                                                   Lógica AFD (atualiza estado, fila)
                                                       |
                                                       V
                                                   Retorna Novo Estado
                             |
                             V
                         updateUI(NovoEstado)
                             |
                             V
                         (Loop de Simulação chama stepSimulationAPI() periodicamente)
                             |
                             V
                         POST /api/elevator/step
                                                       |
                                                       V
                                                   Lógica AFD (move, abre/fecha porta)
                                                       |
                                                       V
                                                   Retorna Novo Estado
                             |
                             V
                         updateUI(NovoEstado)
```

## 5. Demonstração

Para demonstrar o funcionamento:

1.  **Iniciar o Backend:** Execute o servidor Flask (`python src/main.py` dentro da pasta `backend` após ativar o ambiente virtual e instalar dependências).
2.  **Abrir o Frontend:** Abra o arquivo `index.html` em um navegador web.
3.  **Selecionar o Case:** Clique em "Case 2: Elevador".
4.  **Interagir:**
    *   O elevador inicia no térreo com portas abertas.
    *   A visualização do AFD mostrará "Térreo, Portas Abertas" como estado ativo.
    *   Clique em um botão de andar (ex: "3").
        *   O frontend envia a chamada para o backend.
        *   O backend processa: define o andar 3 como destino, fecha as portas (estado muda para "Térreo, Portas Fechadas", depois para "Movendo para Cima").
        *   A cada passo da simulação (controlado pelo `setInterval` no JS e `step` no backend):
            *   O elevador se move um andar para cima.
            *   A interface é atualizada: posição do carro, indicador de andar, descrição do estado e visualização do AFD.
            *   Ao chegar no 3º andar, o estado muda para "3º Andar, Portas Abertas".
    *   Experimente chamar o elevador para outros andares enquanto ele está em movimento ou parado.

*(Em uma apresentação real, seriam mostradas capturas de tela ou um vídeo da simulação em diferentes cenários)*

**Exemplo de Cenário:**

1.  Elevador no Térreo, Portas Abertas.
2.  Usuário chama para o 2º Andar.
    *   Backend: Fila = [2], Destino = 2. Portas fecham. Estado = "Térreo, Portas Fechadas".
    *   Backend: Movimento = "MOVING_UP". Estado = "Movendo para Cima".
    *   Frontend: Animação do elevador subindo, portas fechadas. Visualização do AFD em "Movendo para Cima".
3.  Elevador chega ao 1º Andar.
    *   Backend: Andar Atual = 1. Estado continua "Movendo para Cima".
    *   Frontend: Indicador de andar mostra "1".
4.  Elevador chega ao 2º Andar.
    *   Backend: Andar Atual = 2. Movimento = "STOPPED". Portas abrem. Estado = "2º Andar, Portas Abertas".
    *   Frontend: Animação do elevador parado no 2º andar, portas abrindo. Visualização do AFD em "2º Andar, Portas Abertas".

## 6. Conclusões

Este projeto demonstrou com sucesso a aplicação de um Autômato Finito Determinístico para modelar e simular o comportamento de um elevador. A combinação de uma interface web interativa com um backend que implementa a lógica do AFD permitiu uma visualização clara e didática das transições de estado e do funcionamento geral do sistema.

A visualização do AFD em tempo real na interface do usuário é uma ferramenta valiosa para entender como as ações do usuário e os eventos internos do sistema (como o temporizador de passo da simulação) afetam o estado do elevador.

**Possíveis Melhorias Futuras:**

*   Implementação de uma lógica de atendimento de chamadas mais sofisticada (ex: SCAN/LOOK).
*   Adição de botões de chamada nos próprios andares (painel externo).
*   Visualização gráfica mais elaborada do diagrama do AFD, mostrando as transições explicitamente.
*   Testes unitários mais abrangentes para o backend.

Obrigado!

