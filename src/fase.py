"""Classe Fase responsável pelas ondas de inimigos e entidades ativas."""

from src.entidade import Entidade
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