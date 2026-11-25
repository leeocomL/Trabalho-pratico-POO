"""Classe abstrata base Entidade e utilitário de colisão."""

from abc import ABC, abstractmethod

class Entidade(ABC):
  """Define o estado e os métodos comuns aos objetos do jogo."""

  def __init__(self, x: float, y: float, largura: int, altura: int, velocidade: float = 0.0,) -> None:
    """Cria uma entidade ativa com largura e altura maiores que zero."""
    
    if largura <= 0 or altura <= 0:
      raise ValueError("A largura e a altura da entidade devem ser positivas.")

    self.x = float(x)
    self.y = float(y)
    self.largura = largura
    self.altura = altura
    self.velocidade = velocidade  
    self.ativo = True