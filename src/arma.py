"""Classe Arma com encapsulamento de munição e recarga."""

from src.projetil import Projetil


class Arma:
  """Gerencia munição, recarga e disparo de projéteis."""

  def __init__(self, capacidade_maxima: int = 12, dano: int = 1):
    self.capacidade_maxima = capacidade_maxima
    self._municao = capacidade_maxima
    self.dano = dano
    self.cooldown_max = 16
    self.cooldown_atual = 0

  @property
  def municao(self) -> int:
    return self._municao

  @municao.setter
  def municao(self, valor: int):
    self._municao = max(0, min(valor, self.capacidade_maxima))

  def atualizar_recarga(self):
    if self.cooldown_atual > 0:
      self.cooldown_atual -= 1

  def disparar(self, x: float, y: float, direcao: int) -> Projetil | None:
    if self.municao > 0 and self.cooldown_atual == 0:
      self.municao -= 1
      self.cooldown_atual = self.cooldown_max
      return Projetil(x, y, direcao, self.dano, do_jogador=True)
    return None
