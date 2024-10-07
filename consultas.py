
import requests
from itertools import combinations
from config import client
import calendar
from datetime import datetime


db = client['clash_royale_project']
collection_players = db['cr_players']
collection_battles = db['cr_battles']




# CONSULTA 1
def calcular_porcentagem_vitorias_derrotas(carta, ano):
    primeiro_dia = f"{ano}0101T000000.000Z"  # 1º de janeiro
    ultimo_dia = f"{ano}1231T235959.999Z"   # 31 de dezembro

    # Filtrar batalhas no intervalo e que incluem a carta especificada
    battles = collection_battles.find({
        "tempo_da_batalha": {
            "$gte": primeiro_dia,
            "$lte": ultimo_dia
        },
        "$or": [
            {"deck_jogador1": {"$in": [carta]}},
            {"deck_jogador2": {"$in": [carta]}}
        ]
    })
    
    total_battles = 0
    total_victories = 0

    # Contar vitórias e derrotas
    for battle in battles:
        total_battles += 1
        
        # Verificar se a carta é parte do time vencedor
        if carta in battle["deck_jogador1"] and battle["vencedor"] == "deck_jogador1":
            total_victories += 1
        elif carta in battle["deck_jogador2"] and battle["vencedor"] == "deck_jogador2":
            total_victories += 1

    # Calcular porcentagens
    if total_battles > 0:
        win_percentage = (total_victories / total_battles) * 100
        loss_percentage = 100 - win_percentage
    else:
        win_percentage = 0
        loss_percentage = 0

    return {
        "carta": carta,
        "Período": ano,
        "total_battles": total_battles,
        "total_victories": total_victories,
        "win_percentage": round(win_percentage, 2),
        "loss_percentage": round(loss_percentage, 2)
    }





# CONSULTA 2
def listar_decks_com_vitorias(min_victory_percentage, start_timestamp, end_timestamp):
    # Filtrar batalhas no intervalo de timestamps
    battles = collection_battles.find({
        "tempo_da_batalha": {
            "$gte": start_timestamp,
            "$lte": end_timestamp
        }
    })

    deck_stats = {}

    # Contar vitórias e batalhas para cada deck
    for battle in battles:
        # Verifica o deck do jogador 1
        deck1 = tuple(battle["deck_jogador1"])  # Use tuple para chave imutável
        if deck1 not in deck_stats:
            deck_stats[deck1] = {"total": 0, "victories": 0}
        deck_stats[deck1]["total"] += 1

        # Verifica o deck do jogador 2
        deck2 = tuple(battle["deck_jogador2"])
        if deck2 not in deck_stats:
            deck_stats[deck2] = {"total": 0, "victories": 0}
        deck_stats[deck2]["total"] += 1

        # Verifica se há vencedor e atualiza as vitórias
        if battle["vencedor"] == "deck_jogador1":
            deck_stats[deck1]["victories"] += 1
        elif battle["vencedor"] == "deck_jogador2":
            deck_stats[deck2]["victories"] += 1

    # Filtrar decks com base na porcentagem de vitórias
    winning_decks = []
    for deck, stats in deck_stats.items():
        if stats["total"] > 0:
            victory_percentage = (stats["victories"] / stats["total"]) * 100
            if victory_percentage > min_victory_percentage:
                winning_decks.append({
                    "deck": deck,
                    "victories": stats["victories"],
                    "total": stats["total"],
                    "percentage": round(victory_percentage, 2)
                })

    return winning_decks





# CONSULTA 3
def calcular_derrotas_combo(combo, start_timestamp, end_timestamp):
    # Filtrar batalhas no intervalo de timestamps
    battles = collection_battles.find({
        "tempo_da_batalha": {
            "$gte": start_timestamp,
            "$lte": end_timestamp
        }
    })

    total_derrotas = 0

    # Contar derrotas para o combo especificado
    for battle in battles:
        deck1 = battle["deck_jogador1"]
        deck2 = battle["deck_jogador2"]
        
        # Verifica se o combo está no deck do jogador 1
        if set(combo).issubset(set(deck1)) and battle["vencedor"] in deck2:
            total_derrotas += 1
            
        # Verifica se o combo está no deck do jogador 2
        elif set(combo).issubset(set(deck2)) and battle["vencedor"] in deck1:
            total_derrotas += 1

    return total_derrotas

'''
def derrotas_combo():
    combo = request.form.getlist('combo')  # Lista de cartas recebida do formulário
    start_timestamp = int(request.form['start_timestamp'])  # Timestamp inicial
    end_timestamp = int(request.form['end_timestamp'])      # Timestamp final

    resultado = calcular_derrotas_combo(combo, start_timestamp, end_timestamp)

    return render_template('resultado_derrotas.html', combo=combo, total_derrotas=resultado)
'''





# CONSULTA 4
def calcular_vitorias_carta(carta, percentual):
    # Filtrar todas as batalhas que incluem a carta
    battles = collection_battles.find({
        "$or": [
            {"deck_jogador1": carta},
            {"deck_jogador2": carta}
        ]
    })

    total_vitorias = 0

    for battle in battles:
        # Dados do vencedor e perdedor
        if battle["vencedor"] in battle["deck_jogador1"]:
            vencedor_trofeus = battle["trofeus_jogador1"]
            perdedor_trofeus = battle["trofeus_jogador2"]
            torres_derrubadas = battle["torres_derrubadas"]["jogador2"]
        else:
            vencedor_trofeus = battle["trofeus_jogador2"]
            perdedor_trofeus = battle["trofeus_jogador1"]
            torres_derrubadas = battle["torres_derrubadas"]["jogador1"]

        # Cálculo das condições
        duracao_partida = battle["tempo_da_batalha"]
        trofeus_diferenca = perdedor_trofeus * (1 - percentual / 100)

        if (vencedor_trofeus < trofeus_diferenca and 
                duracao_partida < 120 and  # Menos de 2 minutos
                torres_derrubadas >= 2):   # Pelo menos 2 torres derrubadas
            total_vitorias += 1

    return total_vitorias





# CONSULTA 5
def listar_combos_vitoriosos(tamanho_combo, percentual, start_timestamp, end_timestamp):
    # Filtrar batalhas no intervalo de timestamps
    battles = collection_battles.find({
        "tempo_da_batalha": {
            "$gte": start_timestamp,
            "$lte": end_timestamp
        }
    })

    deck_stats = {}

    # Contar vitórias e batalhas para cada combo de tamanho N
    for battle in battles:
        # Decks dos jogadores
        deck1 = battle["deck_jogador1"]
        deck2 = battle["deck_jogador2"]
        
        # Identificar vencedor
        if battle["vencedor"] in deck1:
            winner_deck = tuple(deck1)
            loser_deck = tuple(deck2)
            winner = True
        else:
            winner_deck = tuple(deck2)
            loser_deck = tuple(deck1)
            winner = False

        # Gerar combos de tamanho N
        for combo in combinations(winner_deck, tamanho_combo):
            combo = tuple(sorted(combo))  # Sorteia o combo para padronização
            if combo not in deck_stats:
                deck_stats[combo] = {"total": 0, "victories": 0}
            deck_stats[combo]["total"] += 1
            if winner:
                deck_stats[combo]["victories"] += 1

        for combo in combinations(loser_deck, tamanho_combo):
            combo = tuple(sorted(combo))
            if combo not in deck_stats:
                deck_stats[combo] = {"total": 0, "victories": 0}
            deck_stats[combo]["total"] += 1
            if not winner:
                deck_stats[combo]["victories"] += 1

    # Filtrar combos com base na porcentagem de vitórias
    winning_combos = []
    for combo, stats in deck_stats.items():
        if stats["total"] > 0:
            win_percentage = (stats["victories"] / stats["total"]) * 100
            if win_percentage > percentual:
                winning_combos.append({
                    "combo": combo,
                    "victories": stats["victories"],
                    "total": stats["total"],
                    "percentage": round(win_percentage, 2)
                })

    return winning_combos



# CONSULTA 6



# CONSULTA 7



# CONSULTA 8




