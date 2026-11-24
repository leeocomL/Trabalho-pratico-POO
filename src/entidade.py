"""Classe abstrata base Entidade e utilitário de colisão."""

from abc import ABC, abstractmethod
import pygame


class Entidade(ABC):
  """Classe abstrata base para todas as entidades do jogo."""

  def __init__(
      self,
      x: float,
      y: float,
      largura: int,
      altura: int,
      velocidade: float = 0.0,
  ):
    self.x = float(x)
    self.y = float(y)
    self.largura = largura
    self.altura = altura
    self.velocidade = velocidade
    self.ativo = True

  @property
  def rect(self) -> pygame.Rect:
    return pygame.Rect(int(self.x), int(self.y), self.largura, self.altura)

  @abstractmethod
  def atualizar(self):
    pass

  @abstractmethod
  def desenhar(self, tela: pygame.Surface):
    pass


class UtilitarioColisao:
  """Utilitário com método estático para verificação de colisões."""

  @staticmethod
  def verificar_colisao(entidade_a: Entidade, entidade_b: Entidade) -> bool:
    """Verifica intersecção de retângulos entre duas entidades."""
    return entidade_a.rect.colliderect(entidade_b.rect)
