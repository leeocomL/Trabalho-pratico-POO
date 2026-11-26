"""Classe Fase responsável pelas ondas de inimigos e entidades ativas."""

import random
from src.config import LARGURA
from src.entidade import Entidade
from src.fabrica import FabricaInimigos
from src.jogador import Jogador
from src.plataforma import Plataforma

class Fase:
  """Gerencia uma onda do jogo e a lista polimórfica de entidades."""

  def __init__(
      self, numero_onda: int, jogador: Jogador, plataformas: list[Plataforma]
  ):
    self.numero_onda = numero_onda
    self.jogador = jogador
    self.entidades: list[Entidade] = list(plataformas) + [jogador]
    self.gerar_onda()

  def gerar_onda(self):
    if self.numero_onda < 3:
      tipos_disponiveis = ["zumbi", "arqueiro", "cavaleiro"]
      for _ in range(2 + self.numero_onda):
        tipo = random.choice(tipos_disponiveis)
        pos_x = random.choice(
            [random.randint(40, 220), random.randint(700, 900)]
        )
        inimigo = FabricaInimigos.criar_inimigo(
            tipo, pos_x, 120, self.jogador, self.entidades
        )
        self.entidades.append(inimigo)
    else:
      boss = FabricaInimigos.criar_inimigo(
          "boss", LARGURA - 180, 100, self.jogador, self.entidades
      )
      self.entidades.append(boss)