"""Classe principal Jogo (loop principal, HUD e verificação de colisões)."""

import sys
import pygame
from src.arma import Arma
from src.config import (
    ALTURA,
    CHAO_Y,
    COR_AMARELO,
    COR_BORDA_CHAO,
    COR_BRANCO,
    COR_CHAO,
    COR_FLECHA_JOGADOR,
    COR_FUNDO,
    COR_VERDE,
    COR_VERMELHO,
    FPS,
    LARGURA,
)
from src.entidade import UtilitarioColisao
from src.fase import Fase
from src.inimigos import Inimigo
from src.jogador import Jogador
from src.placar import Placar
from src.plataforma import Plataforma
from src.projetil import Projetil


class Jogo:
  """Orquestra o jogo contendo Jogador, Fase e Placar por composição."""

  def __init__(self):
    pygame.init()
    self.tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Balada Salada: A dança")

    self.fonte_titulo = pygame.font.SysFont("consolas", 28, bold=True)
    self.fonte_hud = pygame.font.SysFont("consolas", 18, bold=True)
    self.fonte_pequena = pygame.font.SysFont("consolas", 14, bold=True)

    self.reiniciar()

  def reiniciar(self):
    self.plataformas = [
        Plataforma(140, 340, 210),
        Plataforma(610, 340, 210),
        Plataforma(370, 230, 220),
    ]
    self.arma = Arma(capacidade_maxima=12, dano=1)
    self.jogador = Jogador(
        x=450, y=380, arma=self.arma, plataformas=self.plataformas
    )
    self.placar = Placar("Jogador")
    self.fase = Fase(1, self.jogador, self.plataformas)
    self.fim_de_jogo = False
    self.vitoria_onda_timer = 0

  def verificar_colisoes(self):
    projeteis = [
        e for e in self.fase.entidades if isinstance(e, Projetil) and e.ativo
    ]
    inimigos = [
        e for e in self.fase.entidades if isinstance(e, Inimigo) and e.ativo
    ]

    for proj in projeteis:
      if proj.do_jogador:
        for ini in inimigos:
          if UtilitarioColisao.verificar_colisao(proj, ini):
            ini.vida -= proj.dano
            proj.ativo = False
            if not ini.ativo:
              self.placar.pontuacao += ini.pontos
              self.placar.celulas += 1
              self.arma.municao += 2
            break
      else:
        if UtilitarioColisao.verificar_colisao(proj, self.jogador):
          if self.jogador.invencivel_timer == 0:
            self.jogador.vida -= proj.dano
          proj.ativo = False

    for ini in inimigos:
      if UtilitarioColisao.verificar_colisao(ini, self.jogador):
        if self.jogador.invencivel_timer == 0:
          self.jogador.vida -= ini.dano

    if self.jogador.vida <= 0:
      self.fim_de_jogo = True

  def executar(self):
    relogio = pygame.time.Clock()

    while True:
      for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

        if evento.type == pygame.KEYDOWN:
          if self.fim_de_jogo and evento.key == pygame.K_r:
            self.reiniciar()
          elif not self.fim_de_jogo:
            if evento.key in (pygame.K_w, pygame.K_UP, pygame.K_SPACE):
              self.jogador.pular()
            elif evento.key == pygame.K_j:
              tiro = self.arma.disparar(
                  self.jogador.x + 10,
                  self.jogador.y + 20,
                  self.jogador.direcao,

          
              )
              if tiro:
                self.fase.entidades.append(tiro)
            elif evento.key == pygame.K_k:
              hitbox_espada = self.jogador.ataque_espada()
              for e in self.fase.entidades:
                if (
                    isinstance(e, Inimigo)
                    and e.ativo
                    and hitbox_espada.colliderect(e.rect)
                ):
                  e.vida -= 1
                  self.arma.municao += 1
                  if not e.ativo:
                    self.placar.pontuacao += e.pontos
                    self.placar.celulas += 1
            elif evento.key == pygame.K_l:
              self.jogador.esquivar()

      if not self.fim_de_jogo:
        # POLIMORFISMO OBRIGATÓRIO: Único laço sem IF por tipo!
        for e in self.fase.entidades:
          e.atualizar()

        self.verificar_colisoes()
        self.fase.entidades = [e for e in self.fase.entidades if e.ativo]

        inimigos_vivos = [
            e for e in self.fase.entidades if isinstance(e, Inimigo)
        ]
        if len(inimigos_vivos) == 0:
          self.vitoria_onda_timer += 1
          if self.vitoria_onda_timer > 60:
            self.vitoria_onda_timer = 0
            nova_onda = self.fase.numero_onda + 1
            self.jogador.vida += 1
            self.arma.municao = self.arma.capacidade_maxima
            self.fase = Fase(nova_onda, self.jogador, self.plataformas)

      self.tela.fill(COR_FUNDO)
      pygame.draw.rect(
          self.tela, COR_CHAO, (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y)
      )
      pygame.draw.line(
          self.tela, COR_BORDA_CHAO, (0, CHAO_Y), (LARGURA, CHAO_Y), 4
      )

      for e in self.fase.entidades:
        e.desenhar(self.tela)

      txt_vida = self.fonte_hud.render(
          f"VIDA: {'♥' * self.jogador.vida}", True, COR_VERMELHO
      )
      txt_municao = self.fonte_hud.render(
          f"FLECHAS (J): {self.arma.municao}/{self.arma.capacidade_maxima}",
          True,
          COR_FLECHA_JOGADOR,
      )
      txt_placar = self.fonte_hud.render(str(self.placar), True, COR_VERDE)
      txt_onda = self.fonte_hud.render(
          f"ONDA: {self.fase.numero_onda}", True, COR_AMARELO
      )

      self.tela.blit(txt_vida, (20, 15))
      self.tela.blit(txt_municao, (20, 42))
      self.tela.blit(txt_placar, (LARGURA - txt_placar.get_width() - 20, 15))
      self.tela.blit(txt_onda, (LARGURA - txt_onda.get_width() - 20, 42))

      txt_comandos = self.fonte_pequena.render(
          "[A/D] Mover | [W/Espaço] Pular | [J] Atirar Arco | [K] Espada"
          " (Recupera Flecha) | [L] Dash",
          True,
          (170, 170, 190),
      )
      self.tela.blit(
          txt_comandos,
          (LARGURA // 2 - txt_comandos.get_width() // 2, ALTURA - 30),
      )

      if self.fim_de_jogo:
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.tela.blit(overlay, (0, 0))
        txt_fim = self.fonte_titulo.render(
            "VOCÊ MORREU NA MASMORRA!", True, COR_VERMELHO
        )
        txt_reiniciar = self.fonte_hud.render(
            f"Pontuação Final -> {self.placar} | Pressione [R] para Reiniciar",
            True,
            COR_BRANCO,
        )
        self.tela.blit(
            txt_fim,
            (LARGURA // 2 - txt_fim.get_width() // 2, ALTURA // 2 - 30),
        )
        self.tela.blit(
            txt_reiniciar,
            (LARGURA // 2 - txt_reiniciar.get_width() // 2, ALTURA // 2 + 15),
        )

      pygame.display.flip()
      relogio.tick(FPS)
