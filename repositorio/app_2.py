import requests, json
from flask import Flask, render_template


# URL_ATLAS = ''
app = Flask(__name__)



# para ACESSAR a API do clash royale
headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjcxMmU4YTMxLTZiZjgtNGQxYS1iNjI4LTA1OWVlYTgxMTJlOSIsImlhdCI6MTcyODE3NjczMiwic3ViIjoiZGV2ZWxvcGVyL2ZhMjIxNmQ0LTYyMmMtN2M5NC1mMzFlLTYyNGYzN2ZjN2E2YSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxODYuMjE4Ljc0LjY1Il0sInR5cGUiOiJjbGllbnQifV19.VKXPzWcLgvOZndK5kPIwZG5m3ozXU52aFu1OVP0BLZ8KIupp1uhTUPdnXCatKNEmV72G8VgYCHrxRi6sdXf5sg'
}



# LANDPAGE
@app.route('/')
def index():
    '''
        ARMAZENAR:
            * jogadores (apelido, tempo de jogo, troféus, nível);
            * batalhas (tempo, nº torres derrubadas, vencedor, decks, troféus até o momento);
            * decks
        
        RETORNAR:
            * porcentagens utlizando a carta x: vitórias e derrotas, por intervalo de tempo;
                  - parâmetros: carta e tempo
            * listar decks: mais X % de vitórias em um intervalo de tempo;
                - parâmetros: porcentagem e tempo
            * calcular combo de cartas:
                - Xn cartas e tempo
            * vitórias: usando a carta X em que o vencedor porcentagem menor de troféus do que o perdedor,
                partida menor que 2 minutos, perdedor derrubou pelo menos 2 torres;
            * listar combos: quantidade N de cartas para fazer um combo que produziu mais vitórias em um intervalo de tempo.
            * mais uma consultar para auxiliar o balanceamento;
            * mais uma consultar para auxiliar o balanceamento;
            * mais uma consultar para auxiliar o balanceamento;
    '''
    response = requests.get(url='https://developer.clashroyale.com/v1/cards', headers=headers)
    if response.status_code == 200:
        items_obj = json.loads(response.text)
    else:
        print(response.status_code)
        print(response.text)

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)