import pygame  # importa o pygame
import sys  # importa recursos do sistema
from pygame.locals import *  # importa os modulos do pygame

clock = pygame.time.Clock()  # Cria uma variavel de controle de clock (Ciclos/tempo)
pygame.init()  # Inicializando o pygame


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


janela_tamanho = (820, 640)  # Cria uma variavel com o tamenho da janela em pixels
pygame.display.set_caption("Meu jogo")  # Define o título do game que aparece na janela
janela_game = pygame.display.set_mode(janela_tamanho, 0, 32)  # Exibindo a tela
display = pygame.Surface((410, 320))

personagem_sprite = pygame.image.load('imagens/player.png')  # Adiciona a imagem do player  que está na pasta imagens
personagem_sprite = pygame.transform.scale(personagem_sprite, (32, 32))  # Redimensiona o personagem para 32 x 32 pixels
# personagem.set_colorkey((255, 255, 255)) Define que no personagem a cor branca se torna transparente se tiver com
# fundo branco, neste caso já renovi o fundo em um editor de image

bloco_grama = pygame.image.load('imagens/grama.png')  # Importa o bloco com grama
bloco_grama = pygame.transform.scale(bloco_grama, (32, 32))
tamanho_blocos = bloco_grama.get_width()  # Define o tamanho dos blocos, para o tamanho da imagem grama

bloco_terra = pygame.image.load('imagens/terra.png')  # Importa o bloco de terra
bloco_terra = pygame.transform.scale(bloco_terra, (32, 32))

# Cria a base do nosos mapa 0-Epaço vazio(céu) 1-Bloco de terra 2-Bloco com grama
mapa_game = [
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '2', '2', '2', '2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '2', '2', '2', '2', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '2', '2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '2'],
            ['1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1', '1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]

andando_dir = False
andando_esq = False
personagem_y_momentum = 0
tempo_no_ar = 0
personagem_colisao = pygame.Rect(50, 50, personagem_sprite.get_width(),
                                 personagem_sprite.get_height())  # Cria o retangulo de colisaão do personagem,
# com base na sua posição e tamanho

while True:  # Lop infinito do game
    display.fill((146, 244, 255))  # Preenche o fundo da tela

    # loop para prrencher o mapa percorrendo o lista bidimensional
    y = 0
    colisao_blocos = []
    for linha in mapa_game:
        x = 0
        for celula in linha:
            if celula == '1':  # Se a celula for 1
                display.blit(bloco_terra, (x * tamanho_blocos, y * tamanho_blocos))  # Desenha a terra
            if celula == '2':
                display.blit(bloco_grama, (x * tamanho_blocos, y * tamanho_blocos))  # Desenha a grama
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
    personagem_y_momentum += 0.28  # Poder da gravidade, qnd maior mais pesado, menor mais leve
    if personagem_y_momentum > 5:  # Se a força da gravidade chegar a 5
        personagem_y_momentum = 5  # Não aumentara mais, estaciona no 5

    personagem_colisao, colisoes = mover(personagem_colisao, personagem_movimentacao, colisao_blocos)

    if colisoes['abaixo']:  # Se estiver no chão (Colidindo com algo abaixo)
        personagem_y_momentum = 0
        tempo_no_ar = 0
    else:
        tempo_no_ar += 1

    if colisoes['acima']:
        personagem_y_momentum = 0

    # Renderiza a imagem do personagem sobre a tela na posição do personagem_colisao
    display.blit(personagem_sprite, (personagem_colisao.x, personagem_colisao.y))

    for evento in pygame.event.get():  # event loop
        if evento.type == QUIT:  # Se o evento for QUIT (sair)
            pygame.quit()  # Finaliza o game e fecha a tela
            sys.exit()  # Fecha o programa

        if evento.type == KEYDOWN:  # Ao pressionar alguma tecla
            if evento.key == K_RIGHT:  # Se for direita
                andando_dir = True  # Andar pra direita passa a ser verdadeiro
            if evento.key == K_LEFT:
                andando_esq = True
            if evento.key == K_SPACE:
                if tempo_no_ar < 6 :  # Para um double jump experimente 30
                    personagem_y_momentum = -5

        if evento.type == KEYUP:  # Ao soltar alguma tecla
            if evento.key == K_RIGHT:  # Se for seta direita
                andando_dir = False  # Andar direita passa a ser falso
            if evento.key == K_LEFT:
                andando_esq = False

    # escala o display (onde estão os elementos do jogo) para o tamanho da janela
    tela_visivel = pygame.transform.scale(display, janela_tamanho)
    janela_game.blit(tela_visivel, (0, 0))  # Exibe na janela do game a tela_visivel
    pygame.display.update()  # Comando para atualizar a tela acada loop
    clock.tick(60)  # Define queo game vai rodar a 60 FPS
