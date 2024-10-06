# Clash

Este projeto é uma aplicação web desenvolvida em Flask que permite gerenciar jogadores e cartas do jogo Clash Royale. 
Ele utiliza um banco de dados MongoDB para armazenar informações sobre jogadores e suas cartas.


## Tecnologias Utilizadas

- **Flask**: Framework web para Python.
- **Mongo Atlas**: Banco de dados NoSQL para armazenamento de dados.
- **HTML/CSS**: Para a estrutura e estilo da interface.

## Como Começar

### Variáveis
Crie um arquivo .env e preenchar os campos:
**TOKEN=** 'que será a você cria ao registrar uma chave no site https://developer.clashroyale.com/#/';
**CLUSTER=** 'o nome do seu cluster no mongodb Atlas';
**USER_NAME=** 'nome do usuário de acesso';
**PASSWORD=** 'a senha cadastrada do usuário de acesso'

### acessar API do Clash Royale
- crie uma conta no www.developer.clashroyale.com/#/
- crie uma Chave/Key em account => Create New Key => e use o seu IP público

### Instalação
git clone https://github.com/Naeldy/Clash.git
cd clash
pip install -r requirements.txt
python app.py

Acesse a aplicação em seu navegador: http://127.0.0.1:5000/




# OBJETIVOS

ARMAZENAMENTO:
- jogadores: apelido, tempo de jogo, troféus, nível, ...
- batalhas: tempo da batalha, número de torres derrubadas de cada lado, vencedor, deck de cada jogador, quantidade de troféus de cada jogador no momento da partida

CONSULTAS:
- calcule a porcentagem de vitórias e derrotas usando uma carta X, por um intervalo de tempo.
- lista completa do deck mais de X% de vitórias em um intervalo de tempo.
- quantidade de derrotas utilizando o combo de cartas (X1, X2, ...) ocorridas num intervalo de tempo.
- calcule a quantidade de vitórias envolvendo a carta X quando o vencedor possui Z% menos troféus do que o perdedor em que a partida durou menos de 2 minutos e o perdedor derrubou ao menos duas torres do adversário
- listar combo de cartas de tamanho N que produziram Y% de vit´´orias ocorridas em um intervalo de tempo.
- outra consulta a sua escolha.
- outra consulta a sua escolha.
- outra consulta a sua escolha.


