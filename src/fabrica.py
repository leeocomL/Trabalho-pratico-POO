"""Fábrica de inimigos com @classmethod."""

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

  @classmethod
  def criar_inimigo(
      cls,
      tipo: str,
      x: float,
      y: float,
      alvo: Jogador,
      lista_entidades: list[Entidade],
  ) -> Inimigo:
    classe = cls._catalogo.get(tipo, ZumbiSaltador)
    return classe(x, y, alvo, lista_entidades)
