import pygame  # importa o pygame
import sys  # importa recursos do sistema
from pygame.locals import *  # importa os modulos do pygame
import random
from Controle import Controle
from Mapa import Mapa
from Personagem import Personagem

global menu, tela1


# Função que controla a captura de enentos
def controlador_eventos_menu(tela):
    if tela == 'menu':
        for evento in pygame.event.get():  # event loop
            if evento.type == QUIT:  # Se o evento for QUIT (sair)
                pygame.quit()  # Finaliza o game e fecha a tela
                sys.exit()  # Fecha o programa

            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if evento.type == MOUSEBUTTONDOWN:
                global menu, tela1
                menu = False
                tela1 = True


# Função que controla a captura de enentos
def controlador_eventos_mapa(person1, person2):
    for evento in pygame.event.get():  # event loop
        if evento.type == QUIT:  # Se o evento for QUIT (sair)
            pygame.quit()  # Finaliza o game e fecha a tela
            sys.exit()  # Fecha o programa

        if evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        # Plyer 1
        if evento.type == KEYDOWN:  # Ao pressionar alguma tecla
            if evento.key == person1.controle.direita:  # Se for direita
                person1.andando_dir = True  # Andar pra direita passa a ser verdadeiro
            if evento.key == person1.controle.esquerda:
                person1.andando_esq = True
            if evento.key == person1.controle.pulo:
                if person1.tempo_no_ar < 6:  # Para um double jump experimente 30
                    person1.personagem_y_momentum = -5
                    person1.pulando = True
                    person1.som_pulo.play()

        if evento.type == KEYUP:  # Ao soltar alguma tecla
            if evento.key == person1.controle.direita:  # Se for seta direita
                person1.andando_dir = False  # Andar direita passa a ser falso
            if evento.key == person1.controle.esquerda:
                person1.andando_esq = False

        # Plyer 2
        if evento.type == KEYDOWN:  # Ao pressionar alguma tecla
            if evento.key == person2.controle.direita:  # Se for direita
                person2.andando_dir = True  # Andar pra direita passa a ser verdadeiro
            if evento.key == person2.controle.esquerda:
                person2.andando_esq = True
            if evento.key == person2.controle.pulo:
                if person1.tempo_no_ar < 6:  # Para um double jump experimente 30
                    person2.personagem_y_momentum = -5
                    person2.pulando = True
                    person2.som_pulo.play()

        if evento.type == KEYUP:  # Ao soltar alguma tecla
            if evento.key == person2.controle.direita:  # Se for seta direita
                person2.andando_dir = False  # Andar direita passa a ser falso
            if evento.key == person2.controle.esquerda:
                person2.andando_esq = False


# Função para prrencher o mapa percorrendo a lista bidimensional na variavel mapa_game (Populada com dados do txt)
def preencher_mapa(mapa):
    y = 0
    mapa.colisao_blocos = []
    for linha in mapa_game:
        x = 0
        for celula in linha:
            if celula == '1':  # Se a celula for 1
                display.blit(bloco_base,
                             (x * tamanho_blocos - mapa1.rolagem_tela[0], y * tamanho_blocos - mapa1.rolagem_tela[1]))
                # Desenha a terra, na posição subtraimos rolagem_tela, isso permite que o bloco se mova para esquerda
                # caso o valor de rolagem_tela aumente, e para esquerda caso diminua, dando o efeito de rolagem de tela
            if celula == '2':
                display.blit(bloco_superficie,
                             (x * tamanho_blocos - mapa1.rolagem_tela[0], y * tamanho_blocos - mapa1.rolagem_tela[1]))
            if celula != '0':  # Se a celula for diferente de 0, ou seja, é um solido
                mapa.colisao_blocos.append(pygame.Rect(x * tamanho_blocos, y * tamanho_blocos,
                                                       tamanho_blocos, tamanho_blocos))
                # Adiciona um bloco solido no array de solidos com a posição atual do mapa e tamanho de bloco padrão
            x += 1
        y += 1


# Controla a rolagem da tela - Movimentação da Camera
def controle_rolagem_tela(person1, person2):
    if person1.personagem_colisao.x >= person2.personagem_colisao.x:
        personagem = person1
    else:
        personagem = person2
    rolagem_verdadeira[0] += (personagem.personagem_colisao.x - rolagem_verdadeira[0] - display.get_width() / 2) / 20
    rolagem_verdadeira[1] += (personagem.personagem_colisao.y - rolagem_verdadeira[1] - display.get_height() / 2) / 20
    rolagem_tela = rolagem_verdadeira.copy()
    rolagem_tela[0] = int(rolagem_tela[0])
    rolagem_tela[1] = int(rolagem_tela[1])
    return rolagem_tela


# Movimenta o personagem passado nos parametros
def movimentar(personagem):
    # Movimentação
    personagem.personagem_movimentacao = [0, 0]
    if personagem.andando_dir:
        personagem.personagem_movimentacao[0] += 2.5
    if personagem.andando_esq:
        personagem.personagem_movimentacao[0] -= 2.5

    personagem.personagem_movimentacao[1] += personagem.personagem_y_momentum  # Simular a gravidade
    personagem.personagem_y_momentum += 0.3  # Poder da gravidade, qnd maior mais pesado, menor mais leve
    if personagem.personagem_y_momentum > 5:  # Se a força da gravidade chegar a 5
        personagem.personagem_y_momentum = 5  # Não aumentará mais, estaciona no 5


# Alterar animação de acordo com o movimento do personagem passado em parametros
def animar_movimento(personagem):
    if not personagem.pulando:
        if personagem.personagem_movimentacao[0] > 0:  # Se estiver se movendo para direita
            personagem.animacao_atual, personagem.frame_aimacao_atual = personagem.alterar_animacao(
                personagem.animacao_atual, personagem.frame_aimacao_atual, 'correndo')
            personagem.personagem_espelhado = False
        if personagem.personagem_movimentacao[0] < 0:  # Se estiver se movendo para esquerda
            personagem.animacao_atual, personagem.frame_aimacao_atual = personagem.alterar_animacao(
                personagem.animacao_atual, personagem.frame_aimacao_atual, 'correndo')
            personagem.personagem_espelhado = True
        if personagem.personagem_movimentacao[0] == 0:  # Se estiver se movendo para direita
            personagem.animacao_atual, personagem.frame_aimacao_atual = personagem.alterar_animacao(
                personagem.animacao_atual, personagem.frame_aimacao_atual, 'parado')
    else:
        personagem.animacao_atual, personagem.frame_aimacao_atual = personagem.alterar_animacao(
            personagem.animacao_atual, personagem.frame_aimacao_atual, 'pulando')
        if personagem.personagem_movimentacao[0] > 0:  # Se estiver se pulando para direita
            personagem.personagem_espelhado = False
        if personagem.personagem_movimentacao[0] < 0:  # Se estiver se pulando para esquerda
            personagem.personagem_espelhado = True


# Função que controla as colisões do personagem, para ele não atravessar os blocos
def controlar_colisoes(personagem):
    personagem.personagem_colisao, personagem.colisoes = personagem.mover(personagem.personagem_colisao,
                                                                          personagem.personagem_movimentacao,
                                                                          mapa1.colisao_blocos)

    if personagem.colisoes['abaixo']:  # Se estiver no chão (Colidindo com algo abaixo)
        personagem.personagem_y_momentum = 0
        personagem.tempo_no_ar = 0
        personagem.pulando = False
    else:  # Se estiver fora do chão
        personagem.tempo_no_ar += 1

    if personagem.colisoes['acima']:
        personagem.personagem_y_momentum = 0


# Função que controla as animações de movimento do personagem e espelha a sprite
def controlar_animacao(personagem):
    personagem.frame_aimacao_atual += 1
    if personagem.frame_aimacao_atual >= len(personagem.database_animacoes[personagem.animacao_atual]):
        personagem.frame_aimacao_atual = 0
    personagem.personagem_sprite_id = personagem.database_animacoes[personagem.animacao_atual][
        personagem.frame_aimacao_atual]
    personagem.personagem_sprite = personagem.frames_animacao[personagem.personagem_sprite_id]
    # Renderiza a imagem do personagem sobre a tela na posição do personagem_colisao
    display.blit(pygame.transform.flip(personagem.personagem_sprite, personagem.personagem_espelhado, False),
                 (personagem.personagem_colisao.x - mapa1.rolagem_tela[0],
                  personagem.personagem_colisao.y - mapa1.rolagem_tela[1]))
    # Transform flip espelha ou não o personagem de acordo com a variavel personagem_espelhado


# Função que cria a base de dados de animação
def povoar_base_animacao(personagem, champ):
    database_animacoes = {
        'correndo': personagem.carregar_animacoes('imagens/personagens/' + champ + '/correndo/',
                                                  [4, 4, 4, 4, 4, 4, 4, 4],
                                                  personagem.personagem_largura, personagem.personagem_altura),
        'parado': personagem.carregar_animacoes('imagens/personagens/' + champ + '/parado/', [14, 14],
                                                personagem.personagem_largura, personagem.personagem_altura),
        'pulando': personagem.carregar_animacoes('imagens/personagens/' + champ + '/pulando/', [14, 21],
                                                 personagem.personagem_largura, personagem.personagem_altura)}
    return database_animacoes


# Inicicializador
pygame.init()  # Inicializando o pygame
clock = pygame.time.Clock()  # Cria uma variavel de controle de clock (Ciclos/tempo)

# Configurações da janela
monitor_size = [pygame.display.Info().current_w,
                pygame.display.Info().current_h - 60]  # tamanho do monitor menos 60 pixels (Pra barra de titulo)
janela_tamanho = monitor_size  # Cria uma variavel com o tamanho da janela em pixels
pygame.display.set_caption("Meu jogo")  # Define o título do game que aparece na janela
janela_game = pygame.display.set_mode(janela_tamanho, 0, 32)  # Exibindo a tela
display = pygame.Surface((1280, 720))  # Cria o Display do game, area visivel do jogo 360 p  1280x720 854x480 640x360

# Importação da imagens
tamanho_blocos = 64  # Define o tamanho dos blocos do jogo para 32 pixels
bloco_superficie = pygame.image.load('imagens/cenario/blocos/BlocoSuperficie.png')  # Importa o bloco com grama
bloco_superficie = pygame.transform.scale(bloco_superficie, (tamanho_blocos, tamanho_blocos))

bloco_base = pygame.image.load('imagens/cenario/blocos/BlocoBase.png')  # Importa o bloco de terra
bloco_base = pygame.transform.scale(bloco_base, (tamanho_blocos, tamanho_blocos))

fundo = pygame.image.load('imagens/cenario/fundo.jpg')
fundo = pygame.transform.scale(fundo, (display.get_width(), display.get_height()))

obj_cenario_perto = pygame.image.load('imagens/cenario/ObjCenarioPerto.png')
obj_cenario_perto = pygame.transform.scale(obj_cenario_perto, (100, 100))

obj_cenario_longe = pygame.image.load('imagens/cenario/ObjCenarioLonge.png')
obj_cenario_longe = pygame.transform.scale(obj_cenario_longe, (120, 120))

info_menu = pygame.image.load('imagens/menu/info_menu.png')
info_menu = pygame.transform.scale(info_menu, (300, 200))

# Importar os sons
som_pulo_p1 = pygame.mixer.Sound('sons/pulo.wav')
musica_fundo = pygame.mixer.Sound('sons/musica.mp3')
# Play na musica. 0 - Toca uma e repete 0. 3 - Toaca uma e repete 3. -1 - Toca uma e repete ate fechar
musica_fundo.play(-1)

# Instanciação do obj de mapa
mapa1 = Mapa(bloco_superficie, bloco_base, fundo, obj_cenario_perto, obj_cenario_longe, musica_fundo, display)
mapa1.objetos_cenario = [[0.25, [200, random.randrange(10, 80), 'ilha_fundo']],  # [% de Paralax, [X, Y, tipo]
                         [0.25, [480, random.randrange(60, 140), 'ilha_fundo']],
                         [0.25, [730, random.randrange(20, 100), 'ilha_fundo']],
                         [0.25, [990, random.randrange(40, 150), 'ilha_fundo']],
                         [0.5, [230, random.randrange(50, 180), 'ilha_perto']],
                         [0.5, [450, random.randrange(80, 220), 'ilha_perto']],
                         [0.5, [810, random.randrange(50, 180), 'ilha_perto']],
                         [0.5, [950, random.randrange(80, 220), 'ilha_perto']],
                         [0.5, [1170, random.randrange(50, 180), 'ilha_perto']],
                         [0.5, [1390, random.randrange(80, 220), 'ilha_perto']]]

controle1 = Controle(K_d, K_a, K_w)
controle2 = Controle(K_RIGHT, K_LEFT, K_UP)

# Instanciação do obj de personagem
personagem1 = Personagem(80, 64, som_pulo_p1, controle1, 320)
personagem2 = Personagem(80, 64, som_pulo_p1, controle2, 300)

# Preenchendo a base de dados de animações
personagem1.database_animacoes = povoar_base_animacao(personagem1, 'avatar1')
personagem2.database_animacoes = povoar_base_animacao(personagem2, 'avatar2')

# Definição da variaveis do jogo
mapa_game = mapa1.carregar_mapa('mapas/mapa1')
rolagem_verdadeira = [0, 0]
menu = True
tela1 = False

while True:  # Lop infinito do game

    if menu:
        display.blit(fundo, (0, 0))  # Preenche o fundo da tela coma a imagem
        display.blit(info_menu, [165, 75])
        controlador_eventos_menu('menu')  # Chama a função para capturas e controle de eventos

    if tela1:
        mapa1.rolagem_tela = controle_rolagem_tela(personagem1, personagem2)  # Cahama o controle de camera

        display.blit(fundo, (0, 0))  # Preenche o fundo da tela coma a imagem

        mapa1.preencher_fundo_cenario()  # Chama ao método que preenche os itens de fundo do cenário

        preencher_mapa(mapa1)  # Cahama a função que preenche a plataforma do mapa

        movimentar(personagem1)  # Move o retangulo de colisão do personagem pela tela, acompanhado da sprite
        movimentar(personagem2)

        animar_movimento(personagem1)  # Alterar animação de acordo com o movimento
        animar_movimento(personagem2)

        controlar_colisoes(personagem1)  # Chama a função que controla as colisões entre os solidos e o personagem
        controlar_colisoes(personagem2)

        controlar_animacao(personagem1)  # Chama a função que controla as animaçoes das sprites do personagem
        controlar_animacao(personagem2)

        controlador_eventos_mapa(personagem1, personagem2)  # Cama a função para capturas e controle de eventos

    # Escala o display (onde estão os elementos do jogo) para o tamanho da janela
    tela_visivel = pygame.transform.scale(display, janela_tamanho)
    # tela_visivel = pygame.transform.scale(display, (janela_game.get_width(), janela_game.get_height()))
    janela_game.blit(tela_visivel, (0, 0))  # Exibe na janela do game a tela_visivel'''
    pygame.display.update()  # Comando para atualizar a tela acada loop
    clock.tick(60)  # Define que o game vai rodar a 60 FPS
