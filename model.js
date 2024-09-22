const mongoose = require('mongoose');

// Esquema do Jogador
const jogadorSchema = new mongoose.Schema({
  nickname: { type: String, required: true },
  tempo_jogo: { type: Number, required: true },
  trofeus: { type: Number, required: true },
  nivel: { type: Number, required: true },
  deck: { type: [String], default: [] }  // Array de nomes das cartas
});

// Esquema da Carta
const cartaSchema = new mongoose.Schema({
  card: { type: String, required: true },  // Nome da carta
  cardLevel: { type: Number },              // Nível da carta
  cost: { type: Number, required: true },   // Custo da carta
  crownTowerDamage: { type: Number },       // Dano à torre da coroa
  damage: { type: Number, required: true },  // Dano da carta
  damagePerSecond: { type: Number },        // Dano por segundo
  deathDamage: { type: Number },            // Dano de morte
  health: { type: Number },                  // Saúde da carta
  hitSpeed: { type: Number },                // Velocidade de golpe
  maximumSpawned: { type: Number },         // Máximo gerado
  radius: { type: Number },                  // Raio de ataque
  range: { type: Number },                   // Alcance
  spawnDPS: { type: Number },                // DPS de spawn
  spawnDamage: { type: Number },             // Dano de spawn
  spawnHealth: { type: Number },             // Saúde de spawn
  spawnSpeed: { type: Number },              // Velocidade de spawn
  spawnerHealth: { type: Number },           // Saúde do spawner
  troopSpawned: { type: String },            // Tropas geradas
  type: { type: String, required: true }     // Tipo da carta
});

// Esquema da Batalha
const batalhaSchema = new mongoose.Schema({
  data: { type: Date, default: Date.now },
  tempoBatalha: { type: Number, required: true },  // Tempo da batalha
  torresDerubadas: { type: Object, required: true }, // Detalhes das torres derrubadas
  vencedor: { type: String, required: true },        // Vencedor da batalha
  deckJogador1: { type: [String], required: true },  // Deck do jogador 1
  deckJogador2: { type: [String], required: true },  // Deck do jogador 2
  trofeusJogador1: { type: Number, required: true }, // Troféus do jogador 1
  trofeusJogador2: { type: Number, required: true }  // Troféus do jogador 2
});

// Criação dos modelos
const Jogador = mongoose.model('Jogador', jogadorSchema);
const Carta = mongoose.model('Carta', cartaSchema);
const Batalha = mongoose.model('Batalha', batalhaSchema);

module.exports = { Jogador, Carta, Batalha };