import csv
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

# Inicialização do Flask e do MongoDB
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para mensagens flash
client = MongoClient("mongodb://localhost:27017/")
db = client["clash"]
jogadores = db["jogadores"]

# Função para carregar cartas do arquivo CSV
def carregar_cartas():
    caminho_arquivo = r"C:\Users\naeld\OneDrive\Área de Trabalho\Porjeto Mongo\clash_wiki_dataset.csv"
    
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'Card' in row:  # Verifica se a coluna 'Card' existe
                    carta = {
                        "Card": row['Card'],
                        "Cost": int(row['Cost']) if row['Cost'].isdigit() else 0,
                        "Damage": int(row['Damage']) if row['Damage'].isdigit() else 0,
                    }
                    # Insere ou atualiza a carta na coleção 'cartas'
                    db.cartas.update_one({"Card": carta["Card"]}, {"$set": carta}, upsert=True)
        print("Cartas carregadas com sucesso.")
    except FileNotFoundError:
        print("Arquivo não encontrado. Verifique o caminho.")
    except Exception as e:
        print(f"Ocorreu um erro ao carregar as cartas: {e}")

@app.route('/')
def index():
    todos_jogadores = list(jogadores.find())  # Converte o cursor para uma lista
    return render_template('index.html', jogadores=todos_jogadores)

@app.route('/editar/<string:nickname>', methods=['GET', 'POST'])
def editar(nickname):
    jogador = jogadores.find_one({"nickname": nickname})
    if request.method == 'POST':
        # Atualiza informações do jogador
        jogadores.update_one(
            {"nickname": nickname},
            {"$set": {
                "tempo_jogo": int(request.form['tempo_jogo']),
                "trofeus": int(request.form['trofeus']),
                "nivel": int(request.form['nivel'])
            }}
        )
        flash('Jogador atualizado com sucesso!', 'success')
        return redirect(url_for('index'))

    # Renderiza o template de edição
    return render_template('editar.html', jogador=jogador)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nickname = request.form['nickname']
    tempo_jogo = int(request.form['tempo_jogo'])
    trofeus = int(request.form['trofeus'])
    nivel = int(request.form['nivel'])

    novo_jogador = {
        "nickname": nickname,
        "tempo_jogo": tempo_jogo,
        "trofeus": trofeus,
        "nivel": nivel,
        "deck": []  # Inicializa o deck vazio
    }
    jogadores.insert_one(novo_jogador)
    flash('Jogador adicionado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/cartas')
def listar_cartas():
    cartas = db.cartas.find()  # Certifica-se de que a coleção 'cartas' existe
    return render_template('listar_cartas.html', cartas=cartas)

@app.route('/adicionar_carta/<nickname>', methods=['POST'])
def adicionar_carta(nickname):
    carta = request.form['carta']
    jogador = jogadores.find_one({"nickname": nickname})

    if jogador:
        jogadores.update_one(
            {"nickname": nickname},
            {"$addToSet": {"deck": carta}}  # Adiciona a carta ao deck
        )
        flash('Carta adicionada ao deck com sucesso!', 'success')
    else:
        flash('Jogador não encontrado!', 'danger')
    return redirect(url_for('index'))

@app.route('/deletar/<string:nickname>', methods=['POST'])
def deletar(nickname):
    jogadores.delete_one({"nickname": nickname})
    flash('Jogador excluído com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/jogadores_por_forca')
def jogadores_por_forca():
    todos_jogadores = list(jogadores.find())

    # Calcula a força dos decks
    for jogador in todos_jogadores:
        jogador['forca_deck'] = 0  # Inicializa a força do deck
        if isinstance(jogador.get('deck'), list):
            for carta in jogador['deck']:
                carta_info = db.cartas.find_one({"Card": carta})
                if carta_info:
                    # Adiciona a força da carta à força total do deck
                    jogador['forca_deck'] += carta_info.get('Cost', 0) + carta_info.get('Damage', 0)

    # Ordena jogadores pela força do deck
    jogadores_ordenados = sorted(todos_jogadores, key=lambda x: x.get('forca_deck', 0))

    return render_template('jogadores_por_forca.html', jogadores=jogadores_ordenados)

@app.route('/calcular_porcentagem/<nickname>', methods=['GET', 'POST'])
def calcular_porcentagem(nickname):
    # Lógica para calcular a porcentagem do jogador
    return render_template('resultado_porcentagem.html', nickname=nickname)

@app.route('/selecionar_carta/<nickname>')
def selecionar_carta(nickname):
    carregar_cartas()  # Carrega as cartas antes de selecionar
    cartas = db.cartas.find()  # Obtém todas as cartas carregadas
    return render_template('selecionar_carta.html', nickname=nickname, cartas=cartas)

if __name__ == '__main__':
    app.run(debug=True)