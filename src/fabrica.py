"""Fábrica de inimigos com @classmethod e @staticmethod."""

from src.entidade import Entidade
from src.inimigos import (
    ArqueiroMaldito,
    CavaleiroEscudeiro,
    ChefeGuardiao,
    Inimigo,
    ZumbiSaltador,
)
from src.jogador import Jogador


class FabricaInimigos:
  """Centraliza a criação dos diferentes tipos de inimigos."""

  _catalogo = {
      "zumbi": ZumbiSaltador,
      "arqueiro": ArqueiroMaldito,
      "cavaleiro": CavaleiroEscudeiro,
      "boss": ChefeGuardiao,
  }

  @staticmethod
  def tipos_disponiveis() -> list[str]:
    return list(FabricaInimigos._catalogo)

  @classmethod
  def criar_inimigo(
      cls,
      tipo: str,
      x: float,
      y: float,
      alvo: Jogador,
      lista_entidades: list[Entidade],
  ) -> Inimigo:
    if tipo not in cls._catalogo:
      raise ValueError(f"Tipo de inimigo desconhecido: {tipo!r}")
    return cls._catalogo[tipo](x, y, alvo, lista_entidades)
