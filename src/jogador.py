"""Classe Jogador com movimento, pulo, esquiva e ataque de espada."""

import pygame
from src.arma import Arma
from src.config import (
    CHAO_Y,
    COR_AMARELO,
    COR_CACHECOL,
    COR_JOGADOR,
    GRAVIDADE,
    LARGURA,
)
from src.entidade import Entidade
from src.plataforma import Plataforma


class Jogador(Entidade):
  """Entidade controlada pelo usuário, contendo uma Arma por composição."""

  def __init__(
      self, x: float, y: float, arma: Arma, plataformas: list[Plataforma]
  ):
    super().__init__(x, y, largura=34, altura=50, velocidade=5.2)
    self.arma = arma
    self.plataformas = plataformas
    self.vida_maxima = 6
    self._vida = 6
    self.vel_y = 0.0
    self.no_chao = False
    self.direcao = 1  # 1 = Direita, -1 = Esquerda
    self.invencivel_timer = 0
    self.dash_timer = 0
    self.ataque_corpo_timer = 0

  @property
  def vida(self) -> int:
    return self._vida

  @vida.setter
  def vida(self, valor: int):
    if valor < self._vida:
      self.invencivel_timer = 40
    self._vida = max(0, min(valor, self.vida_maxima))

  def pular(self):
    if self.no_chao:
      self.vel_y = -13.2
      self.no_chao = False

  def esquivar(self):
    if self.dash_timer == 0:
      self.dash_timer = 12
      self.invencivel_timer = 15

  def ataque_espada(self) -> pygame.Rect:
    self.ataque_corpo_timer = 10
    offset_x = self.x + self.largura if self.direcao == 1 else self.x - 42
    return pygame.Rect(int(offset_x), int(self.y + 6), 42, 38)

  def atualizar(self):
    self.arma.atualizar_recarga()
    if self.invencivel_timer > 0:
      self.invencivel_timer -= 1
    if self.ataque_corpo_timer > 0:
      self.ataque_corpo_timer -= 1

    teclas = pygame.key.get_pressed()
    vel_atual = (
        self.velocidade * 2.4 if self.dash_timer > 0 else self.velocidade
    )
    if self.dash_timer > 0:
      self.dash_timer -= 1

    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
      self.x -= vel_atual
      self.direcao = -1
    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
      self.x += vel_atual
      self.direcao = 1

    self.x = max(10.0, min(self.x, float(LARGURA - self.largura - 10)))

    y_anterior = self.y + self.altura
    self.vel_y += GRAVIDADE
    self.y += self.vel_y
    self.no_chao = False

    if self.y + self.altura >= CHAO_Y:
      self.y = float(CHAO_Y - self.altura)
      self.vel_y = 0.0
      self.no_chao = True

    if self.vel_y >= 0:
      for plat in self.plataformas:
        if (
            self.x + self.largura > plat.x
            and self.x < plat.x + plat.largura
            and y_anterior <= plat.y + 10
            and self.y + self.altura >= plat.y
        ):
          self.y = float(plat.y - self.altura)
          self.vel_y = 0.0
          self.no_chao = True

  def desenhar(self, tela: pygame.Surface):
    if self.invencivel_timer > 0 and (self.invencivel_timer // 3) % 2 == 0:
      return

    cachecol_x = self.x - 10 if self.direcao == 1 else self.x + self.largura - 4
    pygame.draw.rect(
        tela,
        COR_CACHECOL,
        (int(cachecol_x), int(self.y + 8), 14, 8),
        border_radius=3,
    )
    pygame.draw.rect(tela, (40, 50, 75), self.rect, border_radius=6)
    pygame.draw.rect(tela, COR_JOGADOR, self.rect, 2, border_radius=6)
    pygame.draw.circle(
        tela,
        COR_JOGADOR,
        (int(self.x + self.largura // 2), int(self.y + 12)),
        9,
    )

    if self.ataque_corpo_timer > 0:
      espada_x = self.x + self.largura if self.direcao == 1 else self.x - 42
      pygame.draw.arc(
          tela,
          COR_AMARELO,
          (int(espada_x), int(self.y + 4), 42, 40),
          0,
          3.14,
          4,
      )
