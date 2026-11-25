"""Classe Plataforma para o cenário do jogo."""

from src.entidade import Entidade


class Plataforma(Entidade):
  """Entidade estática que serve de apoio para o jogador."""

  def __init__(self, x: float, y: float, largura: int, altura: int = 18):
    """Cria uma plataforma parada, com altura padrão de 18 pixels."""
    super().__init__(x = x ,y = y , largura = largura, altura = altura ,velocidade = 0)
