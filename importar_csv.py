import pandas as pd
from pymongo import MongoClient

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["clash"]  # Substitua pelo nome do seu banco

# Ler o CSV
df = pd.read_csv('clash_wiki_dataset.csv')

# Inserir dados na coleção de cartas
for index, row in df.iterrows():
    carta = {
        "card": row['Card'],
        "card_level": row['Card Level (Spawn Level)'],
        "cost": row['Cost'],
        "count": row['Count'],
        "crown_tower_damage": row['Crown Tower Damage'],
        "damage": row['Damage'],
        "damage_per_second": row['Damage per second'],
        "death_damage": row['Death Damage'],
        "health_with_shield": row['Health (+Shield)'],
        "hit_speed": row['Hit Speed'],
        "level": row['Level'],
        "maximum_spawned": row['Maximum Spawned'],
        "radius": row['Radius'],
        "range": row['Range'],
        "spawn_dps": row['Spawn DPS'],
        "spawn_damage": row['Spawn Damage'],
        "spawn_health": row['Spawn Health'],
        "spawn_speed": row['Spawn Speed'],
        "spawner_health": row['Spawner Health'],
        "troop_spawned": row['Troop Spawned'],
        "type": row['Type']
    }
    db.cartas.insert_one(carta)

print("Dados importados com sucesso!")