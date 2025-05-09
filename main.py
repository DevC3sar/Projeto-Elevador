# -*- coding: utf-8 -*-
import os
import sys
import logging # Adicionado para logging
# Adiciona o diretório src ao sys.path para permitir importações absolutas
# Não altere esta configuração!!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify, request
from flask_cors import CORS

# Configuração do Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app) # Habilita CORS para todas as rotas

# --- Lógica do Autômato Finito Determinístico (AFD) do Elevador ---
NUM_FLOORS = 4 # Térreo + 3 andares

elevator_state = {
    "current_floor": 0,
    "door_status": "OPEN",    # "OPEN", "CLOSED"
    "movement_status": "STOPPED", # "STOPPED", "MOVING_UP", "MOVING_DOWN"
    "target_floor": None,
    "queue": []
}

def floor_to_text(floor_number):
    if floor_number == 0:
        return "Térreo"
    return f"{floor_number}º Andar"

def get_state_description():
    current = elevator_state["current_floor"]
    doors = elevator_state["door_status"]
    movement = elevator_state["movement_status"]
    target = elevator_state["target_floor"]
    queue = elevator_state["queue"]
    
    desc = None
    if movement == "STOPPED":
        if doors == "OPEN":
            desc = f"Parado no {floor_to_text(current)}, Portas Abertas"
        else: # doors == "CLOSED"
            if target is not None and target != current: # Se tem um target e portas fechadas, vai começar a mover
                 desc = f"Parado no {floor_to_text(current)}, Portas Fechadas. Próximo destino: {floor_to_text(target)}"
            else:
                desc = f"Parado no {floor_to_text(current)}, Portas Fechadas"
    elif movement == "MOVING_UP":
        if target is not None:
            desc = f"Subindo para o {floor_to_text(target)}. Passando por: {floor_to_text(current)}"
        else: # Deveria ter um target se está movendo
            desc = f"Subindo, passando por: {floor_to_text(current)}"
    elif movement == "MOVING_DOWN":
        if target is not None:
            desc = f"Descendo para o {floor_to_text(target)}. Passando por: {floor_to_text(current)}"
        else:
            desc = f"Descendo, passando por: {floor_to_text(current)}"
    
    if desc is None:
        logging.warning(f"Descrição não definida para o estado: C:{current}, D:{doors}, M:{movement}, T:{target}, Q:{queue}")
        desc = f"Processando... Andar: {floor_to_text(current)}, Portas: {doors}, Fila: {queue}"

    logging.debug(f"Estado Atual: Andar={current}, Portas={doors}, Movimento={movement}, Destino={target}, Fila={queue}. Descrição: {desc}")
    return desc

@app.route("/api/elevator/status", methods=["GET"])
def get_status_api():
    logging.info("API: /api/elevator/status (GET) chamada")
    current_status = {
        "current_floor": elevator_state["current_floor"],
        "door_status": elevator_state["door_status"],
        "movement_status": elevator_state["movement_status"],
        "target_floor": elevator_state["target_floor"],
        "queue": elevator_state["queue"],
        "description": get_state_description()
    }
    logging.debug(f"Retornando status: {current_status}")
    return jsonify(current_status)

@app.route("/api/elevator/call", methods=["POST"])
def call_elevator():
    data = request.get_json()
    logging.info(f"API: /api/elevator/call (POST) chamada com dados: {data}")
    if data is None or "floor" not in data:
        logging.error("Erro na chamada: Andar não especificado")
        return jsonify({"error": "Andar não especificado"}), 400
    try:
        requested_floor = int(data["floor"])
    except ValueError:
        logging.error(f"Erro na chamada: Andar inválido - {data['floor']}")
        return jsonify({"error": "Andar inválido"}), 400

    if not (0 <= requested_floor < NUM_FLOORS):
        logging.error(f"Erro na chamada: Andar fora do intervalo - {requested_floor}")
        return jsonify({"error": "Andar fora do intervalo permitido"}), 400

    # Adiciona à fila se não for o destino atual e não estiver na fila
    # E se não for o andar atual com portas abertas
    if requested_floor != elevator_state["target_floor"] and requested_floor not in elevator_state["queue"]:
        if not (elevator_state["current_floor"] == requested_floor and elevator_state["door_status"] == "OPEN" and elevator_state["movement_status"] == "STOPPED"):
            elevator_state["queue"].append(requested_floor)
            logging.info(f"Andar {requested_floor} adicionado à fila. Fila atual: {elevator_state['queue']}")
        else:
            logging.info(f"Chamada para o andar atual ({requested_floor}) com portas abertas ignorada (já no local).")
    else:
        logging.info(f"Chamada para o andar {requested_floor} já está na fila ou é o destino atual.")

    # Se o elevador estiver parado e sem destino, processa a fila
    if elevator_state["movement_status"] == "STOPPED" and elevator_state["target_floor"] is None:
        process_next_in_queue()
    # Se chamado para o andar atual e portas fechadas, abre as portas
    elif elevator_state["current_floor"] == requested_floor and elevator_state["door_status"] == "CLOSED" and elevator_state["movement_status"] == "STOPPED":
        logging.info(f"Chamada para o andar atual ({requested_floor}) com portas fechadas. Abrindo portas.")
        elevator_state["door_status"] = "OPEN"
        if requested_floor in elevator_state["queue"]: # Remove da fila se estava lá
            elevator_state["queue"].remove(requested_floor)
        elevator_state["target_floor"] = None # Garante que não há target se abriu no andar
            
    return jsonify(get_status_api().get_json())

@app.route("/api/elevator/step", methods=["POST"])
def step_simulation():
    logging.info("API: /api/elevator/step (POST) chamada")
    
    # 1. Se parado, sem destino e com fila, define novo destino
    if elevator_state["movement_status"] == "STOPPED" and elevator_state["target_floor"] is None and elevator_state["queue"]:
        logging.debug("Step: Elevador parado, sem destino, com fila. Processando fila.")
        process_next_in_queue()

    # 2. Lógica de Portas e Movimento
    if elevator_state["target_floor"] is not None: # Só faz algo se tiver um destino
        if elevator_state["current_floor"] == elevator_state["target_floor"]:
            # Chegou ao destino
            logging.debug(f"Step: Chegou ao destino {elevator_state['target_floor']}.")
            elevator_state["movement_status"] = "STOPPED"
            if elevator_state["door_status"] == "CLOSED":
                elevator_state["door_status"] = "OPEN"
                logging.info(f"Portas abrindo no andar {elevator_state['current_floor']}")
            elevator_state["target_floor"] = None # Limpa o destino pois chegou
            # Não processa a fila aqui, deixa para o próximo ciclo de step se necessário
        else:
            # Ainda não chegou ao destino, precisa mover ou fechar portas para mover
            if elevator_state["door_status"] == "OPEN":
                elevator_state["door_status"] = "CLOSED"
                logging.info(f"Portas fechando no andar {elevator_state['current_floor']} para mover para {elevator_state['target_floor']}")
            else: # Portas fechadas, pode mover
                if elevator_state["current_floor"] < elevator_state["target_floor"]:
                    elevator_state["movement_status"] = "MOVING_UP"
                    elevator_state["current_floor"] += 1
                    logging.info(f"Movendo para CIMA. Andar atual: {elevator_state['current_floor']}")
                elif elevator_state["current_floor"] > elevator_state["target_floor"]:
                    elevator_state["movement_status"] = "MOVING_DOWN"
                    elevator_state["current_floor"] -= 1
                    logging.info(f"Movendo para BAIXO. Andar atual: {elevator_state['current_floor']}")
    else: # Sem destino (target_floor is None)
        if elevator_state["movement_status"] != "STOPPED":
             # Estava se movendo mas perdeu o target? Para por segurança.
            logging.warning("Step: Movendo sem destino! Parando o elevador.")
            elevator_state["movement_status"] = "STOPPED"
        # Se portas abertas e sem fila, permanece assim. Se tiver fila, o primeiro if deste step tratará.
        # Se portas fechadas, parado e sem fila, permanece assim.

    return jsonify(get_status_api().get_json())

def process_next_in_queue():
    if not elevator_state["queue"]:
        elevator_state["target_floor"] = None
        logging.debug("ProcessQueue: Fila vazia, sem novo destino.")
        return

    # Lógica simples FIFO por enquanto
    next_target = elevator_state["queue"].pop(0)
    elevator_state["target_floor"] = next_target
    logging.info(f"ProcessQueue: Novo destino da fila: {next_target}. Fila restante: {elevator_state['queue']}")

    if elevator_state["current_floor"] == elevator_state["target_floor"]:
        # Chamado para o andar atual, e o elevador está parado
        if elevator_state["door_status"] == "CLOSED":
            elevator_state["door_status"] = "OPEN"
            logging.info(f"ProcessQueue: Já no andar de destino {elevator_state['target_floor']}, abrindo portas.")
        elevator_state["movement_status"] = "STOPPED"
        # elevator_state["target_floor"] = None # Limpa target pois já está no andar e vai abrir/já abriu
    elif elevator_state["current_floor"] < elevator_state["target_floor"]:
        elevator_state["movement_status"] = "MOVING_UP"
    else: # current_floor > target_floor
        elevator_state["movement_status"] = "MOVING_DOWN"
    # A lógica de fechar portas antes de mover está no `step_simulation`.

@app.route("/api/elevator/reset", methods=["POST"])
def reset_simulation_api():
    global elevator_state
    logging.info("API: /api/elevator/reset (POST) chamada")
    elevator_state = {
        "current_floor": 0,
        "door_status": "OPEN",
        "movement_status": "STOPPED",
        "target_floor": None,
        "queue": []
    }
    logging.info("Simulação reiniciada para o estado padrão.")
    return jsonify(get_status_api().get_json())

if __name__ == "__main__":
    logging.info("Iniciando servidor Flask para o simulador de elevador...")
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False) # use_reloader=False para evitar problemas com logging duplicado no modo debug

