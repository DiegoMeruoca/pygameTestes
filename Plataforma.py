import pygame  # importa o pygame
import sys  # importa recursos do sistema
from pygame.locals import *  # importa os modulos do pygame
import random

global frames_animacao  # Declarando uma variavel global
frames_animacao = {}


def testador_colisoes(player_colisao, blocos_colisao):
    lista_colisoes = []
    for bloco in blocos_colisao:
        if player_colisao.colliderect(bloco):  # Se o personagem colidir com o bloco
            lista_colisoes.append(bloco)  # Adiciona o bloco na lista de colisões
    return lista_colisoes


def mover(player_colisao, movimento, blocos_colisao):
    tipos_colisao = {'acima': False, 'abaixo': False, 'esquerda': False, 'direita': False}
    # Colisão no eixo X
    player_colisao.x += movimento[0]
    lista_colisoes = testador_colisoes(player_colisao, blocos_colisao)
    for bloco in lista_colisoes:
        if movimento[0] > 0:  # Se está se movimentando para direita
            player_colisao.right = bloco.left  # A colisão sera a direita do player e a esquerda do bloco
            tipos_colisao['direita'] = True
        elif movimento[0] < 0:
            player_colisao.left = bloco.right
            tipos_colisao['esquerda'] = True
    # Colisão no eixo Y
    player_colisao.y += movimento[1]
    lista_colisoes = testador_colisoes(player_colisao, blocos_colisao)
    for bloco in lista_colisoes:
        if movimento[1] > 0:  # Se está caindo
            player_colisao.bottom = bloco.top  # A colisão sera a abaixo do player e acima do bloco
            tipos_colisao['abaixo'] = True
        elif movimento[1] < 0:
            player_colisao.top = bloco.bottom
            tipos_colisao['acima'] = True
    return player_colisao, tipos_colisao


# Carrega a base do nosos mapa de um txt (0-Epaço vazio(céu) 1-Bloco de terra 2-Bloco com grama)
def carregar_mapa(path):
    arquivo = open(path + '.txt', 'r')
    dados = arquivo.read()
    arquivo.close()
    dados = dados.split('\n')
    mapa = []
    for linha in dados:
        mapa.append(list(linha))
    return mapa


# Controla a rolagem da tela - Movimentação da Camera
def controle_rolagem_tela():
    rolagem_verdadeira[0] += (personagem_colisao.x - rolagem_verdadeira[0] - display.get_width() / 2) / 20
    rolagem_verdadeira[1] += (personagem_colisao.y - rolagem_verdadeira[1] - display.get_height() / 2) / 20
    rolagem_tela = rolagem_verdadeira.copy()
    rolagem_tela[0] = int(rolagem_tela[0])
    rolagem_tela[1] = int(rolagem_tela[1])
    return rolagem_tela


# Insere na tela os objetos de fundo do cenário de acordo com a variavel objetos_cenario
def preencher_fundo_cenario():
    for objeto in objetos_cenario:
        posicao_obj = (objeto[1][0] - rolagem_tela[0] * objeto[0],
                       objeto[1][1] - rolagem_tela[1] * objeto[0])
        if objeto[1][2] == 'ilha_perto':
            display.blit(ilha_perto, posicao_obj)
        elif objeto[1][2] == 'ilha_fundo':
            display.blit(ilha_longe, posicao_obj)


# Funcção para carregar e armazenar as animaçoes do personagem
def carregar_animacoes(path, duracao_frame, sprite_largura, sprite_altura):
    global frames_animacao
    nome_animacao = path.split('/')[-2]  # Divide a string do path nas baras e retorna o ultimo item encontrado "parado"
    base_frames_animacao = []  # Cria uma lista pra servir de base para as imagens
    n = 0
    for frame in duracao_frame:
        id_animacao_frame = nome_animacao + '_' + str(n)  # Define o id por exemplo correndo_1
        imagem_loc = path + str(n) + '.png'  # Define o caminho completo da imagems
        imagem_animacao = pygame.image.load(imagem_loc).convert_alpha()  # Carrega a imagem
        imagem_animacao = pygame.transform.scale(imagem_animacao, (sprite_largura, sprite_altura))  # Escala
        frames_animacao[id_animacao_frame] = imagem_animacao.copy()  # Adiciona na lista
        for i in range(frame):
            base_frames_animacao.append(id_animacao_frame)
        n += 1
    return base_frames_animacao


# Função para alterar a animação que está sendo utilizada
def alterar_animacao(acao, frame, nova_acao):
    if acao != nova_acao:
        acao = nova_acao
        frame = 0
    return acao, frame


# Inicicializador
pygame.init()  # Inicializando o pygame
clock = pygame.time.Clock()  # Cria uma variavel de controle de clock (Ciclos/tempo)

# Configurações da janela
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h - 65]  # tamanho do monitor menos 65 pixels (Pra barra de titulo)
janela_tamanho = monitor_size  # Cria uma variavel com o tamanho da janela em pixels
pygame.display.set_caption("Meu jogo")  # Define o título do game que aparece na janela
janela_game = pygame.display.set_mode(janela_tamanho, 0, 32)  # Exibindo a tela
display = pygame.Surface((640, 360))  # Cria o Display do game, area visivel do jogo

# Importação da imagens
personagem_sprite = pygame.image.load('imagens/personagens/player1/parado/0.png')  # Adiciona a imagem do player  que está na pasta imagens
personagem_sprite = pygame.transform.scale(personagem_sprite, (32, 32))  # Redimensiona o personagem para 32 x 32 pixels
# personagem.set_colorkey((255, 255, 255)) Define que no personagem a cor branca se torna transparente se tiver com
# fundo branco, neste caso já renovi o fundo em um editor de image

tamanho_blocos = 32  # Define o tamanho dos blocos do jogo para 32 pixels
bloco_grama = pygame.image.load('imagens/cenario/blocos/BlocoSuperficie.png')  # Importa o bloco com grama
bloco_grama = pygame.transform.scale(bloco_grama, (tamanho_blocos, tamanho_blocos))

bloco_terra = pygame.image.load('imagens/cenario/blocos/BlocoBase.png')  # Importa o bloco de terra
bloco_terra = pygame.transform.scale(bloco_terra, (tamanho_blocos, tamanho_blocos))

fundo = pygame.image.load('imagens/cenario/fundo.jpg')
fundo = pygame.transform.scale(fundo, (display.get_width(), display.get_height()))

ilha_perto = pygame.image.load('imagens/cenario/ObjCenarioPerto.png')
ilha_perto = pygame.transform.scale(ilha_perto, (100, 100))

ilha_longe = pygame.image.load('imagens/cenario/ObjCenarioLonge.png')
ilha_longe = pygame.transform.scale(ilha_longe, (120, 120))

# Importar os sons
som_pulo = pygame.mixer.Sound('sons/pulo.wav')
musica_fundo = pygame.mixer.Sound('sons/musica.mp3')
# Play na musica. 0 - Toca uma e repete 0. 3 - Toaca uma e repete 3. -1 - Toca uma e repete ate fechar
musica_fundo.play(-1)
'''# Tocar a musica outra maneira
pygame.mixer.music.load('sons/musica.wav')
pygame.mixer.music.play(-1)  '''

# Definição da variaveis do jogo
mapa_game = carregar_mapa('mapas/mapa1')
andando_dir = False
andando_esq = False
personagem_y_momentum = 0
tempo_no_ar = 0
rolagem_verdadeira = [0, 0]
animacao_atual = 'parado'
frame_aimacao_atual = 0
pulando = False
personagem_espelhado = False
fullscreen = False
personagem_altura = 40
personagem_largura = 32
personagem_colisao = pygame.Rect(320, 50, personagem_largura, personagem_altura)  # Cria o retangulo de colisaão do personagem,
# com base na sua posição e tamanho
'''objetos_cenario = [[0.25, [220, 20, 'ilha_fundo']],  # [% de Paralax, [X, Y, tipo]
                   [0.25, [480, 60, 'ilha_fundo']],
                   [0.25, [730, 30, 'ilha_fundo']],
                   [0.5, [230, 40, 'ilha_perto']],
                   [0.5, [450, 90, 'ilha_perto']],
                   [0.5, [810, 120, 'ilha_perto']],
                   [0.5, [950, 45, 'ilha_perto']],
                   [0.5, [1170, 100, 'ilha_perto']]]'''

objetos_cenario = [[0.25, [200, random.randrange(10, 80), 'ilha_fundo']],  # [% de Paralax, [X, Y, tipo]
                   [0.25, [480, random.randrange(60, 140), 'ilha_fundo']],
                   [0.25, [730, random.randrange(20, 100), 'ilha_fundo']],
                   [0.25, [990, random.randrange(40, 150), 'ilha_fundo']],
                   [0.5, [230, random.randrange(50, 180), 'ilha_perto']],
                   [0.5, [450, random.randrange(80, 220), 'ilha_perto']],
                   [0.5, [810, random.randrange(50, 180), 'ilha_perto']],
                   [0.5, [950, random.randrange(80, 220), 'ilha_perto']],
                   [0.5, [1170, random.randrange(50, 180), 'ilha_perto']],
                   [0.5, [1390, random.randrange(80, 220), 'ilha_perto']]]

# Preenchendo a base de dados de animações
database_animacoes = {
    'correndo': carregar_animacoes('imagens/personagens/player1/correndo/', [4, 4, 4, 4, 4, 4, 4, 4], personagem_largura, personagem_altura),
    'parado': carregar_animacoes('imagens/personagens/player1/parado/', [14, 14], personagem_largura, personagem_altura),
    'pulando': carregar_animacoes('imagens/personagens/player1/pulando/', [14, 21], personagem_largura, personagem_altura)}

while True:  # Lop infinito do game
    # display.fill((146, 244, 255))  # Cor do fundo do game - 'Céu'

    rolagem_tela = controle_rolagem_tela()  # Cahama o controle de camera

    display.blit(fundo, (0, 0))  # Preenche o fundo da tela coma a imagem

    preencher_fundo_cenario()  # Chama a funçao que preenche os itens de fundo do cenário

    # loop para prrencher o mapa percorrendo a lista bidimensional na variavel mapa_game (Populada com dados do txt)
    y = 0
    colisao_blocos = []
    for linha in mapa_game:
        x = 0
        for celula in linha:
            if celula == '1':  # Se a celula for 1
                display.blit(bloco_terra, (x * tamanho_blocos - rolagem_tela[0], y * tamanho_blocos - rolagem_tela[1]))
                # Desenha a terra, na posição subtraimos rolagem_tela, isso permite que o bloco se mova para esquerda
                # caso o valor de rolagem_tela aumente, e para esquerda caso diminua, dando o efeito de rolagem de tela
            if celula == '2':
                display.blit(bloco_grama, (x * tamanho_blocos - rolagem_tela[0], y * tamanho_blocos - rolagem_tela[1]))
            if celula != '0':  # Se a celula for diferente de 0, ou seja, é um solido
                colisao_blocos.append(pygame.Rect(x * tamanho_blocos, y * tamanho_blocos,
                                                  tamanho_blocos, tamanho_blocos))
                # Adiciona um bloco solido no array de solidos com a posição atual do mapa e tamanho de bloco padrão
            x += 1
        y += 1

    # Movimentação
    personagem_movimentacao = [0, 0]
    if andando_dir:
        personagem_movimentacao[0] += 2
    if andando_esq:
        personagem_movimentacao[0] -= 2

    personagem_movimentacao[1] += personagem_y_momentum  # Simular a gravidade
    personagem_y_momentum += 0.3  # Poder da gravidade, qnd maior mais pesado, menor mais leve
    if personagem_y_momentum > 5:  # Se a força da gravidade chegar a 5
        personagem_y_momentum = 5  # Não aumentara mais, estaciona no 5

    # Alterar animação de acordo com o movimento
    if not pulando:
        if personagem_movimentacao[0] > 0:  # Se estiver se movendo para direita
            animacao_atual, frame_aimacao_atual = alterar_animacao(animacao_atual, frame_aimacao_atual, 'correndo')
            personagem_espelhado = False
        if personagem_movimentacao[0] < 0:  # Se estiver se movendo para esquerda
            animacao_atual, frame_aimacao_atual = alterar_animacao(animacao_atual, frame_aimacao_atual, 'correndo')
            personagem_espelhado = True
        if personagem_movimentacao[0] == 0:  # Se estiver se movendo para direita
            animacao_atual, frame_aimacao_atual = alterar_animacao(animacao_atual, frame_aimacao_atual, 'parado')
    else:
        animacao_atual, frame_aimacao_atual = alterar_animacao(animacao_atual, frame_aimacao_atual, 'pulando')
        if personagem_movimentacao[0] > 0:  # Se estiver se pulando para direita
            personagem_espelhado = False
        if personagem_movimentacao[0] < 0:  # Se estiver se pulando para esquerda
            personagem_espelhado = True

    # Colisões
    personagem_colisao, colisoes = mover(personagem_colisao, personagem_movimentacao, colisao_blocos)

    if colisoes['abaixo']:  # Se estiver no chão (Colidindo com algo abaixo)
        personagem_y_momentum = 0
        tempo_no_ar = 0
        pulando = False
    else:
        tempo_no_ar += 1

    if colisoes['acima']:
        personagem_y_momentum = 0

    # Controle da animação
    frame_aimacao_atual += 1
    if frame_aimacao_atual >= len(database_animacoes[animacao_atual]):
        frame_aimacao_atual = 0
    personagem_sprite_id = database_animacoes[animacao_atual][frame_aimacao_atual]
    personagem_sprite = frames_animacao[personagem_sprite_id]
    # Renderiza a imagem do personagem sobre a tela na posição do personagem_colisao
    display.blit(pygame.transform.flip(personagem_sprite, personagem_espelhado, False),
                 (personagem_colisao.x - rolagem_tela[0], personagem_colisao.y - rolagem_tela[1]))
    # Transform flip espelha ou não o personagem de acordo com a variavel personagem_espelhado

    # Captura de eventos
    for evento in pygame.event.get():  # event loop
        if evento.type == QUIT:  # Se o evento for QUIT (sair)
            pygame.quit()  # Finaliza o game e fecha a tela
            sys.exit()  # Fecha o programa

        if evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        if evento.type == KEYDOWN:  # Ao pressionar alguma tecla
            if evento.key == K_RIGHT:  # Se for direita
                andando_dir = True  # Andar pra direita passa a ser verdadeiro
            if evento.key == K_LEFT:
                andando_esq = True
            if evento.key == K_SPACE:
                if tempo_no_ar < 6:  # Para um double jump experimente 30
                    personagem_y_momentum = -5
                    pulando = True
                    som_pulo.play()

        if evento.type == KEYUP:  # Ao soltar alguma tecla
            if evento.key == K_RIGHT:  # Se for seta direita
                andando_dir = False  # Andar direita passa a ser falso
            if evento.key == K_LEFT:
                andando_esq = False

    # Escala o display (onde estão os elementos do jogo) para o tamanho da janela
    tela_visivel = pygame.transform.scale(display, janela_tamanho)
    # tela_visivel = pygame.transform.scale(display, (janela_game.get_width(), janela_game.get_height()))
    janela_game.blit(tela_visivel, (0, 0))  # Exibe na janela do game a tela_visivel'''
    pygame.display.update()  # Comando para atualizar a tela acada loop
    clock.tick(60)  # Define que o game vai rodar a 60 FPS
