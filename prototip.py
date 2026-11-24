from abc import ABC, abstractmethod
import random
import sys
import pygame

# =====================================================================
# CONFIGURAÇÕES GERAIS E INICIALIZAÇÃO
# =====================================================================
pygame.init()
LARGURA, ALTURA = 960, 540
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("gamezin de poo")

FONTE_TITULO = pygame.font.SysFont("consolas", 28, bold=True)
FONTE_HUD = pygame.font.SysFont("consolas", 18, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("consolas", 14, bold=True)

# Paleta de Cores (Estilo Dark Fantasy / Dead Cells)
COR_FUNDO = (18, 16, 26)
COR_CHAO = (38, 33, 50)
COR_BORDA_CHAO = (75, 65, 95)
COR_JOGADOR = (0, 210, 255)
COR_CACHECOL = (230, 45, 75)
COR_ZUMBI = (80, 190, 90)
COR_ARQUEIRO = (170, 95, 230)
COR_CAVALEIRO = (220, 140, 40)
COR_BOSS = (210, 30, 60)
COR_FURIA = (255, 80, 0)
COR_FLECHA_JOGADOR = (120, 240, 255)
COR_FLECHA_INIMIGA = (255, 90, 90)
COR_BRANCO = (240, 240, 240)
COR_AMARELO = (250, 210, 60)
COR_VERMELHO = (220, 50, 50)
COR_VERDE = (50, 210, 100)

GRAVIDADE = 0.65
CHAO_Y = 460


# =====================================================================
# 1. CLASSE ABSTRATA (Requisito Obrigatório)
# =====================================================================
class Entidade(ABC):

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


# =====================================================================
# 2. UTILITÁRIO DE COLISÃO (@staticmethod Obrigatório)
# =====================================================================
class UtilitarioColisao:

  @staticmethod
  def verificar_colisao(entidade_a: Entidade, entidade_b: Entidade) -> bool:
    """Verifica intersecção de retângulos entre duas entidades."""
    return entidade_a.rect.colliderect(entidade_b.rect)


# =====================================================================
# 3. PROJÉTIL E ARMA (Composição e Encapsulamento com @property)
# =====================================================================
class Projetil(Entidade):

  def __init__(
      self,
      x: float,
      y: float,
      direcao_x: int,
      dano: int,
      do_jogador: bool = True,
  ):
    super().__init__(x, y, largura=18, altura=6, velocidade=11.0)
    self.direcao_x = direcao_x
    self.dano = dano
    self.do_jogador = do_jogador

  def atualizar(self):
    self.x += self.velocidade * self.direcao_x
    if self.x < -50 or self.x > LARGURA + 50:
      self.ativo = False

  def desenhar(self, tela: pygame.Surface):
    cor = COR_FLECHA_JOGADOR if self.do_jogador else COR_FLECHA_INIMIGA
    pygame.draw.rect(tela, cor, self.rect, border_radius=3)


class Arma:

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
    # Validação obrigatória no setter
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


# =====================================================================
# 4. PLACAR (Encapsulamento e Métodos Especiais: __str__, __eq__, __lt__)
# =====================================================================
class Placar:

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


# =====================================================================
# 5. PLATAFORMA (Entidade de Cenário)
# =====================================================================
class Plataforma(Entidade):

  def __init__(self, x: float, y: float, largura: int, altura: int = 18):
    super().__init__(x, y, largura, altura, velocidade=0)

  def atualizar(self):
    pass

  def desenhar(self, tela: pygame.Surface):
    pygame.draw.rect(tela, COR_CHAO, self.rect, border_radius=4)
    pygame.draw.rect(
        tela, COR_BORDA_CHAO, (self.x, self.y, self.largura, 4), border_radius=2
    )


# =====================================================================
# 6. JOGADOR (Herda de Entidade e Contém Arma)
# =====================================================================
class Jogador(Entidade):

  def __init__(
      self, x: float, y: float, arma: Arma, plataformas: list[Plataforma]
  ):
    super().__init__(x, y, largura=34, altura=50, velocidade=5.2)
    self.arma = arma  # Composição: Jogador contém Arma
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
      self.invencivel_timer = 40  # Frames de invencibilidade ao sofrer dano
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

    # Limites laterais da tela
    self.x = max(10.0, min(self.x, float(LARGURA - self.largura - 10)))

    # Física vertical e gravidade
    y_anterior = self.y + self.altura
    self.vel_y += GRAVIDADE
    self.y += self.vel_y
    self.no_chao = False

    # Colisão com o chão principal
    if self.y + self.altura >= CHAO_Y:
      self.y = float(CHAO_Y - self.altura)
      self.vel_y = 0.0
      self.no_chao = True

    # Colisão com plataformas suspensas (apenas caindo)
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

    # Cachecol vermelho e corpo estilo Dead Cells
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


# =====================================================================
# 7. HERANÇA: CLASSE ABSTRATA INIMIGO + 3 SUBCLASSES + BOSS
# =====================================================================
class Inimigo(Entidade, ABC):

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


class ChefeGuardiao(Inimigo):

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
        servo = FabricaInimigos.criar_inimigo(
            "zumbi", self.x, self.y - 20, self.alvo, self.lista_entidades
        )
        self.lista_entidades.append(servo)

      self.timer_acao = 55 if self.fase_furia else 90

  def desenhar(self, tela: pygame.Surface):
    super().desenhar(tela)
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
    txt = FONTE_PEQUENA.render(titulo_boss, True, COR_BRANCO)
    tela.blit(txt, (LARGURA // 2 - txt.get_width() // 2, 28))


# =====================================================================
# 8. FÁBRICA DE INIMIGOS (@classmethod Obrigatório)
# =====================================================================
class FabricaInimigos:
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


# =====================================================================
# 9. FASE E JOGO (Composição: Jogo contém Jogador, Fase e Placar)
# =====================================================================
class Fase:

  def __init__(
      self, numero_onda: int, jogador: Jogador, plataformas: list[Plataforma]
  ):
    self.numero_onda = numero_onda
    self.jogador = jogador
    self.entidades: list[Entidade] = list(plataformas) + [jogador]
    self.gerar_onda()

  def gerar_onda(self):
    if self.numero_onda < 3:
      tipos_disponiveis = ["zumbi", "arqueiro", "cavaleiro"]
      for _ in range(2 + self.numero_onda):
        tipo = random.choice(tipos_disponiveis)
        pos_x = random.choice(
            [random.randint(40, 220), random.randint(700, 900)]
        )
        inimigo = FabricaInimigos.criar_inimigo(
            tipo, pos_x, 120, self.jogador, self.entidades
        )
        self.entidades.append(inimigo)
    else:
      boss = FabricaInimigos.criar_inimigo(
          "boss", LARGURA - 180, 100, self.jogador, self.entidades
      )
      self.entidades.append(boss)


class Jogo:

  def __init__(self):
    self.plataformas = [
        Plataforma(140, 340, 210),
        Plataforma(610, 340, 210),
        Plataforma(370, 230, 220),
    ]
    self.arma = Arma(capacidade_maxima=12, dano=1)
    self.jogador = Jogador(
        x=450, y=380, arma=self.arma, plataformas=self.plataformas
    )
    self.placar = Placar("leozin")
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
            self.__init__()
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

      TELA.fill(COR_FUNDO)
      pygame.draw.rect(TELA, COR_CHAO, (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y))
      pygame.draw.line(TELA, COR_BORDA_CHAO, (0, CHAO_Y), (LARGURA, CHAO_Y), 4)

      for e in self.fase.entidades:
        e.desenhar(TELA)

      txt_vida = FONTE_HUD.render(
          f"VIDA: {'♥' * self.jogador.vida}", True, COR_VERMELHO
      )
      txt_municao = FONTE_HUD.render(
          f"FLECHAS (J): {self.arma.municao}/{self.arma.capacidade_maxima}",
          True,
          COR_FLECHA_JOGADOR,
      )
      txt_placar = FONTE_HUD.render(str(self.placar), True, COR_VERDE)
      txt_onda = FONTE_HUD.render(
          f"ONDA: {self.fase.numero_onda}", True, COR_AMARELO
      )

      TELA.blit(txt_vida, (20, 15))
      TELA.blit(txt_municao, (20, 42))
      TELA.blit(txt_placar, (LARGURA - txt_placar.get_width() - 20, 15))
      TELA.blit(txt_onda, (LARGURA - txt_onda.get_width() - 20, 42))

      txt_comandos = FONTE_PEQUENA.render(
          "[A/D] Mover | [W/Espaço] Pular | [J] Atirar Arco | [K] Espada"
          " (Recupera Flecha) | [L] Dash",
          True,
          (170, 170, 190),
      )
      TELA.blit(
          txt_comandos,
          (LARGURA // 2 - txt_comandos.get_width() // 2, ALTURA - 30),
      )

      if self.fim_de_jogo:
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        TELA.blit(overlay, (0, 0))
        txt_fim = FONTE_TITULO.render(
            "VOCÊ MORREU NA MASMORRA!", True, COR_VERMELHO
        )
        txt_reiniciar = FONTE_HUD.render(
            f"Pontuação Final -> {self.placar} | Pressione [R] para Reiniciar",
            True,
            COR_BRANCO,
        )
        TELA.blit(
            txt_fim,
            (LARGURA // 2 - txt_fim.get_width() // 2, ALTURA // 2 - 30),
        )
        TELA.blit(
            txt_reiniciar,
            (LARGURA // 2 - txt_reiniciar.get_width() // 2, ALTURA // 2 + 15),
        )

      pygame.display.flip()
      relogio.tick(60)


if __name__ == "__main__":
  Jogo().executar()