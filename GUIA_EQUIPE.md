# Guia de Orientação da Equipe — Trabalho Prático de POO

Este guia reúne tudo o que cada integrante do grupo (6 pessoas) precisa saber para trabalhar em conjunto, manter o histórico no Git organizado e mandar bem na apresentação final.

---

## 1. Datas e Avaliação (Fique atento!)

### Prazos
- **Etapa 3 (26/11):** Hierarquia de classes completa e polimorfismo funcionando.
- **Mostra final em sala (03/12):** A turma testa os jogos e vota ("mais criativo" e "melhor arquitetura").
- **Etapa 4 (10/12 ou 14/12):** Versão final, **Defesa Oral** e **Requisito Surpresa**.

### Como a nota é composta
| Critério | Peso | O que importa para você |
| :--- | :---: | :--- |
| **Qualidade do design POO** | 30% | Cumprir os requisitos obrigatórios (abstração, herança, polimorfismo, encapsulamento, composição, métodos especiais, `@classmethod`/`@staticmethod`). |
| **Processo** | 25% | Entregas no prazo (10%), **commits distribuídos entre todos os 6 membros (10%)** e **registro de uso de IA (5%)**. |
| **Jogo funcionando e criativo** | 20% | O jogo roda sem travar, é jogável e tem identidade própria. |
| **Defesa oral (sorteio)** | 15% | 1 integrante é sorteado para explicar o código; **a nota dele vai para TODOS**. |
| **Requisito surpresa (sorteio)** | 10% | 1 integrante é sorteado para implementar algo novo na hora (ex.: novo inimigo em 10 min); **a nota dele vai para TODOS**. |

> **Resumo:** Não basta só uma pessoa programar. Todo mundo precisa **commitar com a própria conta** e **entender a estrutura geral do código**.

---

## 2. Divisão dos 6 Pacotes de Trabalho

Cada integrante assume **1 pacote** (preencher os nomes abaixo antes de começar):

| Pacote | Integrante | O que faz | Dificuldade |
| :--- | :--- | :--- | :---: |
| **Pacote 1** | *(Antonio)* | `Entidade` (classe abstrata), `Plataforma` e `UtilitarioColisao` (`@staticmethod`) 
| **Pacote 2** | *(Leo)* | `Arma` (`municao` com `@property`, disparo e recarga) + `Projetil` 
| **Pacote 3** | *(Nome)* | `Inimigo` (classe abstrata) + `ZumbiSaltador` + `ArqueiroMaldito` 
| **Pacote 4** | *(Nome)* | `CavaleiroEscudeiro` + `ChefeGuardiao` + `FabricaInimigos` (`@classmethod`/`@staticmethod`) 
| **Pacote 5** | *(Nome)* | `Placar` (`pontuacao` com `@property`, `__str__`, `__eq__`, `__lt__`) + `Fase` + integração no `Jogo` 
| **Pacote 6** | *(Nome)* | `Jogador` (`vida` com `@property`, movimento, pulo, esquiva, ataque de espada) 

---

## 3. Requisitos Obrigatórios de POO (Checklist)

Todo o grupo precisa garantir que o código final tenha:

- [ ] **Classe abstrata:** `Entidade` (e `Inimigo`) herdando de `ABC` com `@abstractmethod` em `atualizar()` e `desenhar(tela)`.
- [ ] **Herança:** Pelo menos 3 tipos de inimigos herdando de `Inimigo` (temos 4: `ZumbiSaltador`, `ArqueiroMaldito`, `CavaleiroEscudeiro`, `ChefeGuardiao`).
- [ ] **Polimorfismo:** Um único laço `for e in entidades: e.atualizar()` (e `e.desenhar(tela)`), **sem `if isinstance(...)` ou `if tipo == ...`**.
- [ ] **Encapsulamento:** `vida`, `pontuacao` e `municao` usando `@property` e `@<nome>.setter` com validação (ex.: não deixar vida/munição/pontuação ficarem negativos).
- [ ] **Composição:** `Jogo` contém `Jogador`, `Fase` e `Placar`; `Jogador` contém `Arma`.
- [ ] **Métodos especiais:** `__str__`, `__eq__` e `__lt__` implementados em `Placar`.
- [ ] **`@classmethod` / `@staticmethod`:** `FabricaInimigos.criar_inimigo(...)` e `UtilitarioColisao.verificar_colisao(...)`.

---

## 4. Contrato Básico entre as Classes (Para tudo encaixar)

Antes de mexer no seu arquivo, siga este padrão para que o código de uma pessoa funcione com o da outra:

1. **Toda entidade herda de `Entidade`** e possui `x`, `y`, `largura`, `altura`, `velocidade`, `ativo` (`bool`) e a propriedade `rect` retornando um `pygame.Rect`.
2. **Assinatura padrão dos métodos:**
   - `atualizar(self)` — atualiza posição, física, estado ou cooldowns.
   - `desenhar(self, tela: pygame.Surface)` — desenha o objeto na tela do Pygame.
3. **Sem `if` por tipo no loop principal:** cada classe resolve seu próprio comportamento dentro do seu `atualizar()` e `desenhar(tela)`.

---

## 5. Passo a Passo do Git e GitHub (Como trabalhar sem conflito)

Repositório oficial: `https://github.com/leeocomL/Trabalho-pratico-POO.git`

### Primeira vez no seu computador
```bash
git clone https://github.com/leeocomL/Trabalho-pratico-POO.git
cd Trabalho-pratico-POO
pip install pygame
```

Configure seu nome e e-mail (use o **mesmo e-mail da sua conta do GitHub** para os commits contarem para você):
```bash
git config user.name "Seu Nome"
git config user.email "seu_email@exemplo.com"
```

### Fluxo diário para trabalhar na sua parte
1. **Sempre atualize a `main` antes de começar:**
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Crie (ou entre na) sua branch:**
   *(Nunca trabalhe direto na `main` para não quebrar o código dos colegas.)*
   ```bash
   git checkout -b feat/nome-da-sua-parte
   ```
   Exemplos: `feat/jogador`, `feat/arma-projetil`, `feat/inimigos`, `feat/placar-fase`.

3. **Faça suas alterações, salve e teste o jogo.**

4. **Salve e envie seus commits:**
   ```bash
   git status
   git add .
   git commit -m "feat: descreva o que voce fez aqui"
   git push -u origin feat/nome-da-sua-parte
   ```
5. **Abra um Pull Request (PR) no GitHub:**
   - Entre no repositório no GitHub, clique em **Compare & pull request** e crie o PR para `main`.
   - Outro integrante revisa/testa se o jogo continua rodando e faz o merge.

---

## 6. Registro de Uso de IA (Obrigatório — 5% da nota)

A professora permite usar IA, mas exige transparência. Sempre que usar IA para gerar, revisar ou entender algum trecho da sua parte, anote na tabela abaixo (ou no arquivo de registro da etapa):

| Etapa | Onde usamos IA | O que precisamos corrigir ou entender |
| :--- | :--- | :--- |
| Etapa 3 | *Ex.: Estruturação da classe `Arma` com `@property`* | *Ex.: Entendemos como o setter impede munição negativa e ajustamos o cooldown.* |
| | | |

---

## 7. Preparação para Defesa Oral e Requisito Surpresa

Como qualquer um dos 6 pode ser sorteado na apresentação final, revise estes pontos antes da entrega:

- **Por que `Entidade` e `Inimigo` são abstratas?**
  Para impedir que alguém instancie uma "entidade genérica" ou um "inimigo genérico" e para obrigar toda subclasse a implementar `atualizar()` e `desenhar()`.
- **Onde está o polimorfismo?**
  No loop do `Jogo` (`for e in entidades: e.atualizar()` e `e.desenhar(tela)`). Cada objeto responde de forma diferente ao mesmo método, sem precisar de `if` checando o tipo.
- **Como funciona o encapsulamento?**
  Atributos protegidos (`_vida`, `_municao`, `_pontuacao`) acessados via `@property` e validados no `@...setter`.
- **Como adicionar um novo inimigo em 10 minutos (Requisito Surpresa)?**
  1. Criar uma nova classe herdando de `Inimigo` e implementar `atualizar()` e `desenhar(tela)`.
  2. Registrar o novo tipo na `FabricaInimigos`.
  3. Não precisa alterar `Jogador`, `Jogo` ou o loop de polimorfismo!
