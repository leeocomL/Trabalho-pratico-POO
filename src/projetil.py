"""Classe Projetil para disparos do jogador e de inimigos."""

import pygame
from src.config import COR_FLECHA_INIMIGA, COR_FLECHA_JOGADOR, LARGURA
from src.entidade import Entidade


class Projetil(Entidade):
  """Projétil que se move horizontalmente causando dano ao atingir alvos."""

  def __init__(
      self,
      x: float,
      y: float,
      direcao_x: int,
      dano: int,
      do_jogador: bool = True,
  ):
    super().__init__(x, y, largura=18, altura=6, velocidade=11.0)
    self.direcao_x = direcao_x
    self.dano = dano
    self.do_jogador = do_jogador

  def atualizar(self):
    self.x += self.velocidade * self.direcao_x
    if self.x < -50 or self.x > LARGURA + 50:
      self.ativo = False

  def desenhar(self, tela: pygame.Surface):
    cor = COR_FLECHA_JOGADOR if self.do_jogador else COR_FLECHA_INIMIGA
    pygame.draw.rect(tela, cor, self.rect, border_radius=3)
