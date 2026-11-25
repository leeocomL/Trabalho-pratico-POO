"""Classe Plataforma para o cenário do jogo."""

from src.entidade import Entidade

from src.config import COR_BORDA_CHAO, COR_CHAO

import pygame as py

class Plataforma(Entidade):
  """Entidade estática que serve de apoio para o jogador."""

  def __init__(self, x: float, y: float, largura: int, altura: int = 18):
    """Cria uma plataforma parada, com altura padrão de 18 pixels."""
    super().__init__(x = x ,y = y , largura = largura, altura = altura ,velocidade = 0)


  def atualizar(self):
    pass


  def desenhar(self, tela: py.Surface):
    py.draw.rect(tela, COR_CHAO, self.rect, border_radius = 4)
    py.draw.rect(tela, COR_BORDA_CHAO, (self.x, self.y, self.largura, 4), border_radius = 2)
