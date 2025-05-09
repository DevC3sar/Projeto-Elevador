document.addEventListener("DOMContentLoaded", () => {
    const case1Btn = document.getElementById("case1-btn");
    const case2Btn = document.getElementById("case2-btn");
    const menuContainer = document.querySelector(".menu-container");
    const elevatorSimulationContainer = document.querySelector(".elevator-simulation-container");

    const elevatorCar = document.getElementById("elevator-car");
    const elevatorFloorIndicator = document.getElementById("elevator-floor-indicator");
    const afdStateDisplay = document.getElementById("afd-state");
    const currentFloorDisplay = document.getElementById("current-floor-display");
    const floorButtons = document.querySelectorAll(".floor-btn");
    const afdVisualizer = document.getElementById("afd-visualizer");

    let simulationInterval = null;
    const SIMULATION_STEP_INTERVAL = 1500;

    const afdStates = {
        "S0_OPEN": { name: "Térreo, Portas Abertas", description: "Elevador no térreo, portas abertas, aguardando chamada." },
        "S0_CLOSED": { name: "Térreo, Portas Fechadas", description: "Elevador no térreo, portas fechadas, pronto para mover ou aguardando." },
        "S1_OPEN": { name: "1º Andar, Portas Abertas", description: "Elevador no 1º andar, portas abertas." },
        "S1_CLOSED": { name: "1º Andar, Portas Fechadas", description: "Elevador no 1º andar, portas fechadas." },
        "S2_OPEN": { name: "2º Andar, Portas Abertas", description: "Elevador no 2º andar, portas abertas." },
        "S2_CLOSED": { name: "2º Andar, Portas Fechadas", description: "Elevador no 2º andar, portas fechadas." },
        "S3_OPEN": { name: "3º Andar, Portas Abertas", description: "Elevador no 3º andar, portas abertas." },
        "S3_CLOSED": { name: "3º Andar, Portas Fechadas", description: "Elevador no 3º andar, portas fechadas." },
        "MOVING_UP": { name: "Movendo para Cima", description: "Elevador subindo entre andares." },
        "MOVING_DOWN": { name: "Movendo para Baixo", description: "Elevador descendo entre andares." }
    };

    function mapBackendStateToVisualAfdKey(state) {
        if (!state || typeof state.movement_status === "undefined") return null;
        if (state.movement_status === "MOVING_UP") return "MOVING_UP";
        if (state.movement_status === "MOVING_DOWN") return "MOVING_DOWN";
        return `S${state.current_floor}_${state.door_status}`;
    }

    function renderAfdVisualizer(currentStateKey) {
        if (!afdVisualizer) return;
        let html = "<h4>Visualização do AFD (Estados Simplificados):</h4><ul>";
        for (const key in afdStates) {
            const stateInfo = afdStates[key];
            const isActive = key === currentStateKey;
            html += `<li class="afd-state-item ${isActive ? "active" : ""}" title="${stateInfo.description}">${stateInfo.name}</li>`;
        }
        html += "</ul>";
        afdVisualizer.innerHTML = html;
    }

    case2Btn.addEventListener("click", () => {
        menuContainer.style.display = "none";
        elevatorSimulationContainer.style.display = "flex";
        resetSimulation();
    });

    floorButtons.forEach(button => {
        button.addEventListener("click", () => {
            const targetFloor = parseInt(button.dataset.target);
            console.log(`Botão do andar ${targetFloor} clicado.`);
            callElevator(targetFloor);
        });
    });

    // === MOCK SIMULADO SEM BACKEND ===

    let mockState = {
        current_floor: 0,
        door_status: "OPEN",
        movement_status: "STOPPED",
        description: "Parado no Térreo, Portas Abertas"
    };

    let mockTargetFloor = 0;

    async function fetchAPI(endpoint, method = "GET", body = null) {
        console.log(`[MOCK] Chamando: ${endpoint}`, method, body);
        await new Promise(resolve => setTimeout(resolve, 500)); // Simula atraso

        if (endpoint === "/status") {
            return { ...mockState };
        }

        if (endpoint === "/reset") {
            mockState = {
                current_floor: 0,
                door_status: "OPEN",
                movement_status: "STOPPED",
                description: "Parado no Térreo, Portas Abertas"
            };
            mockTargetFloor = 0;
            return { ...mockState };
        }

        if (endpoint === "/call" && method === "POST") {
            mockTargetFloor = body.floor;
            console.log(`[MOCK] Elevador chamado para andar ${mockTargetFloor}`);
            return { ...mockState };
        }

        if (endpoint === "/step" && method === "POST") {
            if (mockState.current_floor !== mockTargetFloor) {
                mockState.door_status = "CLOSED";
                mockState.movement_status = (mockTargetFloor > mockState.current_floor) ? "MOVING_UP" : "MOVING_DOWN";
                mockState.description = "Movendo para " + (mockState.movement_status === "MOVING_UP" ? "cima" : "baixo");

                mockState.current_floor += (mockState.movement_status === "MOVING_UP") ? 1 : -1;
            } else {
                mockState.movement_status = "STOPPED";
                mockState.door_status = "OPEN";
                mockState.description = `Parado no ${mockState.current_floor === 0 ? "Térreo" : mockState.current_floor + "º Andar"}, Portas Abertas`;
            }

            return { ...mockState };
        }

        return null;
    }

    async function getStatus() {
        console.log("Solicitando status do elevador...");
        const data = await fetchAPI("/status");
        if (data) {
            updateUI(data);
        }
    }

    async function callElevator(floor) {
        console.log(`Frontend: Chamando elevador para o andar: ${floor}`);
        const data = await fetchAPI("/call", "POST", { floor });
        if (data) {
            updateUI(data);
        }
    }

    async function stepSimulationAPI() {
        const data = await fetchAPI("/step", "POST");
        if (data) {
            updateUI(data);
        }
    }

    async function resetSimulation() {
        console.log("Resetando simulação...");
        const data = await fetchAPI("/reset", "POST");
        if (data) {
            updateUI(data);
        }
        startSimulationLoop();
    }

    function updateUI(state) {
        if (!state || typeof state.current_floor === "undefined") {
            console.error("Estado inválido recebido para updateUI:", state);
            afdStateDisplay.textContent = "Erro ao carregar estado!";
            return;
        }

        console.log("Atualizando UI com estado:", state);

        const bottomPosition = state.current_floor * 100;
        elevatorCar.style.bottom = `${bottomPosition}px`;
        elevatorFloorIndicator.textContent = floorToIndicatorText(state.current_floor);

        if (state.door_status === "OPEN") {
            elevatorCar.classList.add("doors-open");
        } else {
            elevatorCar.classList.remove("doors-open");
        }

        afdStateDisplay.textContent = state.description || "Carregando descrição...";
        currentFloorDisplay.textContent = floorToDisplayText(state.current_floor);

        const visualAfdKey = mapBackendStateToVisualAfdKey(state);
        renderAfdVisualizer(visualAfdKey);
    }

    function floorToIndicatorText(floor) {
        return floor === 0 ? "T" : floor.toString();
    }

    function floorToDisplayText(floor) {
        return floor === 0 ? "Térreo" : `${floor}º Andar`;
    }

    function startSimulationLoop() {
        if (simulationInterval) {
            clearInterval(simulationInterval);
            console.log("Loop de simulação anterior interrompido.");
        }
        simulationInterval = setInterval(() => {
            stepSimulationAPI();
        }, SIMULATION_STEP_INTERVAL);
        console.log("Loop de simulação iniciado.");
        getStatus();
    }

    renderAfdVisualizer(null);
});
