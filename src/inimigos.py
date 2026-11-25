"""Classe abstrata Inimigo e suas 4 subclasses."""

from abc import ABC
import random
import pygame
from src.config import (
    CHAO_Y,
    COR_ARQUEIRO,
    COR_BOSS,
    COR_BRANCO,
    COR_CAVALEIRO,
    COR_FURIA,
    COR_VERMELHO,
    COR_ZUMBI,
    GRAVIDADE,
    LARGURA,
)
from src.entidade import Entidade
from src.jogador import Jogador
from src.projetil import Projetil


class Inimigo(Entidade, ABC):
  """Classe base abstrata para todos os inimigos do jogo."""

  def __init__(
      self,
      x: float,
      y: float,
      largura: int,
      altura: int,
      velocidade: float,
      vida_max: int,
      dano: int,
      pontos: int,
      cor: tuple,
      alvo: Jogador,
      lista_entidades: list[Entidade],
  ):
    super().__init__(x, y, largura, altura, velocidade)
    self.vida_maxima = vida_max
    self._vida = vida_max
    self.dano = dano
    self.pontos = pontos
    self.cor = cor
    self.alvo = alvo
    self.lista_entidades = lista_entidades
    self.vel_y = 0.0
    self.no_chao = False
    self.piscar_dano = 0

  @property
  def vida(self) -> int:
    return self._vida

  @vida.setter
  def vida(self, valor: int):
    if valor < self._vida:
      self.piscar_dano = 8
    self._vida = max(0, min(valor, self.vida_maxima))
    if self._vida == 0:
      self.ativo = False

  def aplicar_gravidade_basica(self):
    self.vel_y += GRAVIDADE
    self.y += self.vel_y
    if self.y + self.altura >= CHAO_Y:
      self.y = float(CHAO_Y - self.altura)
      self.vel_y = 0.0
      self.no_chao = True

  def desenhar_barra_vida(self, tela: pygame.Surface):
    proporcao = self.vida / self.vida_maxima
    pygame.draw.rect(
        tela, (50, 20, 20), (int(self.x), int(self.y - 10), self.largura, 5)
    )
    pygame.draw.rect(
        tela,
        COR_VERMELHO,
        (int(self.x), int(self.y - 10), int(self.largura * proporcao), 5),
    )

  def desenhar(self, tela: pygame.Surface):
    cor_desenho = COR_BRANCO if self.piscar_dano > 0 else self.cor
    if self.piscar_dano > 0:
      self.piscar_dano -= 1
    pygame.draw.rect(tela, (30, 28, 38), self.rect, border_radius=6)
    pygame.draw.rect(tela, cor_desenho, self.rect, 3, border_radius=6)
    self.desenhar_barra_vida(tela)


class ZumbiSaltador(Inimigo):
  """Inimigo ágil que persegue o jogador dando saltos periódicos."""

  def __init__(
      self, x: float, y: float, alvo: Jogador, lista_entidades: list[Entidade]
  ):
    super().__init__(
        x,
        y,
        32,
        46,
        2.6,
        vida_max=2,
        dano=1,
        pontos=50,
        cor=COR_ZUMBI,
        alvo=alvo,
        lista_entidades=lista_entidades,
    )
    self.timer_pulo = random.randint(45, 90)

  def atualizar(self):
    direcao = 1 if self.alvo.x > self.x else -1
    self.x += self.velocidade * direcao
    self.timer_pulo -= 1
    if self.timer_pulo <= 0 and self.no_chao:
      self.vel_y = -11.0
      self.no_chao = False
      self.timer_pulo = random.randint(60, 110)
    self.aplicar_gravidade_basica()


class ArqueiroMaldito(Inimigo):
  """Inimigo à distância que mantém afastamento e dispara flechas."""

  def __init__(
      self, x: float, y: float, alvo: Jogador, lista_entidades: list[Entidade]
  ):
    super().__init__(
        x,
        y,
        30,
        48,
        1.5,
        vida_max=2,
        dano=1,
        pontos=80,
        cor=COR_ARQUEIRO,
        alvo=alvo,
        lista_entidades=lista_entidades,
    )
    self.cooldown_tiro = random.randint(60, 120)

  def atualizar(self):
    distancia_x = self.alvo.x - self.x
    direcao = 1 if distancia_x >= 0 else -1
    if abs(distancia_x) < 220:
      self.x -= self.velocidade * direcao
    elif abs(distancia_x) > 380:
      self.x += self.velocidade * direcao
    self.x = max(20.0, min(self.x, float(LARGURA - self.largura - 20)))
    self.aplicar_gravidade_basica()

    self.cooldown_tiro -= 1
    if self.cooldown_tiro <= 0:
      flecha = Projetil(
          self.x + 10, self.y + 18, direcao, dano=1, do_jogador=False
      )
      self.lista_entidades.append(flecha)
      self.cooldown_tiro = 110


class CavaleiroEscudeiro(Inimigo):
  """Inimigo pesado com alta resistência e dano elevado."""

  def __init__(
      self, x: float, y: float, alvo: Jogador, lista_entidades: list[Entidade]
  ):
    super().__init__(
        x,
        y,
        44,
        56,
        1.1,
        vida_max=5,
        dano=2,
        pontos=150,
        cor=COR_CAVALEIRO,
        alvo=alvo,
        lista_entidades=lista_entidades,
    )

  def atualizar(self):
    direcao = 1 if self.alvo.x > self.x else -1
    self.x += self.velocidade * direcao
    self.aplicar_gravidade_basica()
      
  def desenhar(self, tela: pygame.Surface):
    super().desenhar(tela)
    lado = self.x + self.largura if self.alvo.x > self.x else self.x - 8
    pygame.draw.rect(tela, COR_BRANCO, (lado, self.y + 10, 8, 36))

class ChefeGuardiao(Inimigo):
  """Chefe da masmorra com fase de fúria e ataques variados."""

  def __init__(
      self, x: float, y: float, alvo: Jogador, lista_entidades: list[Entidade]
  ):
    super().__init__(
        x,
        y,
        72,
        88,
        2.0,
        vida_max=20,
        dano=2,
        pontos=1000,
        cor=COR_BOSS,
        alvo=alvo,
        lista_entidades=lista_entidades,
    )
    self.fase_furia = False
    self.timer_acao = 90
    self._fonte_titulo = None

  def atualizar(self):
    if self.vida <= self.vida_maxima // 2 and not self.fase_furia:
      self.fase_furia = True
      self.cor = COR_FURIA
      self.velocidade = 3.4

    direcao = 1 if self.alvo.x > self.x else -1
    self.x += self.velocidade * direcao
    self.aplicar_gravidade_basica()

    self.timer_acao -= 1
    if self.timer_acao <= 0:
      padrao = random.choice(["SALTO_ESMAGADOR", "RAJADA", "INVOCAR"])
      if padrao == "SALTO_ESMAGADOR" and self.no_chao:
        self.vel_y = -14.5
        self.no_chao = False
      elif padrao == "RAJADA":
        self.lista_entidades.append(
            Projetil(self.x, self.y + 30, -1, 1, do_jogador=False)
        )
        self.lista_entidades.append(
            Projetil(
                self.x + self.largura, self.y + 30, 1, 1, do_jogador=False
            )
        )
      elif padrao == "INVOCAR" and self.fase_furia:
        from src.fabrica import FabricaInimigos

        servos = [
            e for e in self.lista_entidades
            if isinstance(e, ZumbiSaltador) and e.ativo
        ]
        if len(servos) < 3:
          servo = FabricaInimigos.criar_inimigo(
              "zumbi", self.x, self.y - 20, self.alvo, self.lista_entidades
          )
          self.lista_entidades.append(servo)
      self.timer_acao = 55 if self.fase_furia else 90

  def desenhar(self, tela: pygame.Surface):
    super().desenhar(tela)
    if self._fonte_titulo is None:
      self._fonte_titulo = pygame.font.SysFont("consolas", 14, bold=True)

    largura_total = 460
    x_barra = LARGURA // 2 - largura_total // 2
    proporcao = self.vida / self.vida_maxima
    pygame.draw.rect(
        tela, (40, 15, 20), (x_barra, 48, largura_total, 18), border_radius=4
    )
    pygame.draw.rect(
        tela,
        self.cor,
        (x_barra, 48, int(largura_total * proporcao), 18),
        border_radius=4,
    )
    pygame.draw.rect(
        tela, COR_BRANCO, (x_barra, 48, largura_total, 18), 2, border_radius=4
    )
    titulo_boss = (
        "CHEFE GUARDIÃO (EM FÚRIA!)"
        if self.fase_furia
        else "CHEFE: O GUARDIÃO DA MASMORRA"
    )
    txt = self._fonte_titulo.render(titulo_boss, True, COR_BRANCO)
    tela.blit(txt, (LARGURA // 2 - txt.get_width() // 2, 28))

