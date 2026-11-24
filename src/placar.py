"""Classe Placar com encapsulamento e métodos especiais."""


class Placar:
  """Armazena pontuação e células do jogador, permitindo comparação."""

  def __init__(self, nome_jogador: str):
    self.nome_jogador = nome_jogador
    self._pontuacao = 0
    self.celulas = 0

  @property
  def pontuacao(self) -> int:
    return self._pontuacao

  @pontuacao.setter
  def pontuacao(self, valor: int):
    self._pontuacao = max(0, valor)

  def __str__(self) -> str:
    return (
        f"{self.nome_jogador} | Pontos: {self._pontuacao} | Células:"
        f" {self.celulas}"
    )

  def __eq__(self, outro) -> bool:
    return isinstance(outro, Placar) and self._pontuacao == outro._pontuacao

  def __lt__(self, outro) -> bool:
    return isinstance(outro, Placar) and self._pontuacao < outro._pontuacao
