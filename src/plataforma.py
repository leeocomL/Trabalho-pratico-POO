"""Classe Plataforma para o cenário do jogo."""

import pygame
from src.config import COR_BORDA_CHAO, COR_CHAO
from src.entidade import Entidade


class Plataforma(Entidade):
  """Entidade estática que serve de apoio para o jogador."""

  def __init__(self, x: float, y: float, largura: int, altura: int = 18):
    super().__init__(x, y, largura, altura, velocidade=0)

  def atualizar(self):
    pass

  def desenhar(self, tela: pygame.Surface):
    pygame.draw.rect(tela, COR_CHAO, self.rect, border_radius=4)
    pygame.draw.rect(
        tela, COR_BORDA_CHAO, (self.x, self.y, self.largura, 4), border_radius=2
    )
