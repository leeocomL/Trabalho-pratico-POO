"""Classe Jogador com movimento, pulo, esquiva e ataque de espada."""
from src.arma import Arma
from src.config import (
    CHAO_Y,
    COR_AMARELO,
    COR_CACHECOL,
    COR_JOGADOR,
    GRAVIDADE,
    LARGURA,
)
from src.entidade import Entidade
from src.plataforma import Plataforma


class Jogador(Entidade):
  """Entidade controlada pelo usuário, contendo uma Arma por composição."""

  def __init__(self, x: float, y: float, arma: Arma, plataformas: list[Plataforma]):
    super().__init__(x, y, largura=34, altura=50, velocidade=5.2)
    self.arma = arma
    self.plataformas = plataformas
    self.vida_maxima = 6
    self._vida = 6
    self.vel_y = 0.0
    self.no_chao = False
    self.direcao = 1  # 1 = Direita, -1 = Esquerda
    self.invencivel_timer = 0
    self.dash_timer = 0
    self.ataque_corpo_timer = 0


  @property
  def vida(self) -> int:
    return self._vida

  @vida.setter
  def vida(self, valor: int):
    if valor < self._vida:
        self.invencivel_timer = 40

    self._vida = max(0, min(valor, self.vida_maxima))

  def pular(self):
    if self.no_chao:
        self.vel_y = -13.2
        self.no_chao = False

  def esquivar(self):
    if self.dash_timer == 0:
        self.dash_timer = 12
        self.invencivel_timer = 15