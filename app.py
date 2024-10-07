import requests
import json
from flask import Flask, render_template
import os
from dotenv import load_dotenv
from config import client
from consultas import calcular_porcentagem_vitorias_derrotas, listar_decks_com_vitorias, calcular_derrotas_combo, calcular_vitorias_carta, listar_combos_vitoriosos


# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar a aplicação Flask
app = Flask(__name__)

# Carregar a chave de API Clash Royale do arquivo .env
API_KEY = os.getenv('TOKEN')

# Configurar os cabeçalhos para a requisição à API
headers = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}



db = client['clash_royale_project']
collection_players = db['cr_players']
collection_battles = db['cr_battles']

PLAYERs_TAG = [
    '%232RPRP0RG', '%232QYVJ0GC', '%232QL0YCJR', '%232GGR2GPQ0', '%23GJV9GPUJJ', '%232YGQVGQ9', '%2322Y9CGYGQ',
    '%232CLPLVGVP', '%23R09228V', '%23PP0VL8LC', '%23220L9GC2', '%232YJRUQ2Q', '%232Q8L8YQG', '%23QVPJRV', 
    '%23P00809CUQ', '%2320R90LLPU', '%232PUJ2URC', '%238P2YR9', '%232JC0JRL2', '%232UQC9VP', '%23280UYY9R8'
]



# Rota principal para a página inicial
@app.route('/')
def index():
    items_obj = []  # Inicializar uma lista para armazenar os dados das batalhas

    player_count = collection_players.count_documents({})  # se já existir coleção com dados, não precisa inserir novamente
    if player_count < 5:
        try:
            # POPULAR DATABASE
            for PLAYER_TAG in PLAYERs_TAG:
                try:
                    # Fazer a requisição para a API de batalhas do jogador
                    response = requests.get(url=f'https://api.clashroyale.com/v1/players/{PLAYER_TAG}/battlelog', headers=headers)
                    response.raise_for_status()  # Lançar erro se o status_code não for 200
                    battle_log = response.json()  # Parsear o JSON de resposta
                    
                    for battle in battle_log:
                        # Extrair informações dos jogadores
                        for player in battle["team"]:
                            jogador = {
                                "nickname": player["name"],
                                "tempo_de_jogo": battle["battleTime"],  # ou algum cálculo que você fizer
                                "trofeus": player["startingTrophies"],
                                "nivel": player["globalRank"]  # ou outro nível que você defina
                            }

                            # Inserir ou atualizar jogador no MongoDB
                            collection_players.update_one(
                                {"nickname": jogador["nickname"]},
                                {"$set": jogador},
                                upsert=True
                            )

                        # Extrair informações da batalha
                        batalha = {
                            "tempo_da_batalha": battle["battleTime"],
                            "torres_derrubadas": {
                                "jogador1": battle["team"][0]["crowns"],
                                "jogador2": battle["opponent"][0]["crowns"]
                            },
                            "vencedor": battle["team"][0]["name"] if battle["team"][0]["crowns"] > battle["opponent"][0]["crowns"] else battle["opponent"][0]["name"],
                            "deck_jogador1": [card["name"] for card in battle["team"][0]["cards"]],
                            "deck_jogador2": [card["name"] for card in battle["opponent"][0]["cards"]],
                            "trofeus_jogador1": battle["team"][0]["startingTrophies"],
                            "trofeus_jogador2": battle["opponent"][0]["startingTrophies"]
                        }
                        
                        # Inserir batalha no MongoDB
                        collection_battles.insert_one(batalha)

                except Exception as err:
                    print(f"Ocorreu um erro no LOOP: {err}")
                    continue
        
        except requests.exceptions.HTTPError as err:
            print(f"Erro HTTP: {err}")
            items_obj = []

        except Exception as err:
            print(f"Ocorreu um erro GENÉRICO: {err}")
            items_obj = []

    # CONSULTA 1
    try:
        items_obj.append(calcular_porcentagem_vitorias_derrotas('Wizard', 1633046400, 1635638400)) # parâmmetros FIXOS
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(items_obj)
    except Exception as err:
        print("ERRO na CONSULTA 1: ", err)

    # CONSULTA 2
    try:
        items_obj.append(listar_decks_com_vitorias(3, 1633046400, 1635638400)) # parâmmetros FIXOS
    except Exception as err:
        print("ERRO na CONSULTA 2: ", err)

    # CONSULTA 3
    try:    
        items_obj.append(calcular_derrotas_combo(["Knight", "Wizard", "Barbarians"], 1633046400, 1635638400)) # parâmmetros FIXOS
    except Exception as err:
        print("ERRO na CONSULTA 3: ", err)

    # CONSULTA 4
    try:
        items_obj.append(calcular_vitorias_carta("Arqueira", 15)) # parâmmetros FIXOS
    except Exception as err:
        print("ERRO na CONSULTA 4: ", err)

    # CONSULTA 5
    try:
        items_obj.append(listar_combos_vitoriosos(2, 50, 1633046400, 1635638400)) # parâmmetros FIXOS
    except Exception as err:
        print("ERRO na CONSULTA 5: ", err)

    '''
    # CONSULTA 6
    try:
        items_obj[5] = calcular_porcentagem_vitorias_derrotas(carta, start_timestamp, end_timestamp) # parâmmetros FIXOS
    except Exception as err:
        print("ERRO: ", err)

    # CONSULTA 7
    try:
        items_obj[6] = calcular_porcentagem_vitorias_derrotas(carta, start_timestamp, end_timestamp) # parâmmetros FIXOS
    except Exception as err:
        print("ERRO: ", err)

    # CONSULTA 8
    try:
        items_obj[7] = calcular_porcentagem_vitorias_derrotas(carta, start_timestamp, end_timestamp) # parâmmetros FIXOS
    except Exception as err:
        print("ERRO: ", err)
    '''




    # Renderizar o template HTML com os dados das cartas
    return render_template('index.html', resultados=items_obj)

# Inicializar o servidor
if __name__ == '__main__':
    app.run(debug=True)

