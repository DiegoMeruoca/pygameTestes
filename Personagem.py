import pygame


class Personagem:
    def __init__(self, altura, largura, pulo, controle, spawn_inicial):
        self.andando_dir = False
        self.andando_esq = False
        self.personagem_y_momentum = 0
        self.personagem_movimentacao = []
        self.tempo_no_ar = 0
        self.animacao_atual = 'parado'
        self.frame_aimacao_atual = 0
        self.pulando = False
        self.personagem_espelhado = False
        self.personagem_altura = altura
        self.personagem_largura = largura
        self.controle = controle
        self.spaw_inicial = spawn_inicial
        self.frames_animacao = {}
        self.som_pulo = pulo
        self.personagem_colisao = pygame.Rect(spawn_inicial, 50, self.personagem_largura,
                                              self.personagem_altura)  # Cria o retangulo de colisaão do personagem,
        self.database_animacoes = {}

    def testador_colisoes(self, player_colisao, blocos_colisao):
        lista_colisoes = []
        for bloco in blocos_colisao:
            if player_colisao.colliderect(bloco):  # Se o personagem colidir com o bloco
                lista_colisoes.append(bloco)  # Adiciona o bloco na lista de colisões
        return lista_colisoes

    def mover(self, player_colisao, movimento, blocos_colisao):
        tipos_colisao = {'acima': False, 'abaixo': False, 'esquerda': False, 'direita': False}
        # Colisão no eixo X
        player_colisao.x += movimento[0]
        lista_colisoes = self.testador_colisoes(player_colisao, blocos_colisao)
        for bloco in lista_colisoes:
            if movimento[0] > 0:  # Se está se movimentando para direita
                player_colisao.right = bloco.left  # A colisão sera a direita do player e a esquerda do bloco
                tipos_colisao['direita'] = True
            elif movimento[0] < 0:
                player_colisao.left = bloco.right
                tipos_colisao['esquerda'] = True
        # Colisão no eixo Y
        player_colisao.y += movimento[1]
        lista_colisoes = self.testador_colisoes(player_colisao, blocos_colisao)
        for bloco in lista_colisoes:
            if movimento[1] > 0:  # Se está caindo
                player_colisao.bottom = bloco.top  # A colisão sera a abaixo do player e acima do bloco
                tipos_colisao['abaixo'] = True
            elif movimento[1] < 0:
                player_colisao.top = bloco.bottom
                tipos_colisao['acima'] = True
        return player_colisao, tipos_colisao

    # Funcção para carregar e armazenar as animaçoes do personagem
    def carregar_animacoes(self, path, duracao_frame, sprite_largura, sprite_altura):
        nome_animacao = path.split('/')[
            -2]  # Divide a string do path nas baras e retorna o ultimo item encontrado "parado"
        base_frames_animacao = []  # Cria uma lista pra servir de base para as imagens
        n = 0
        for frame in duracao_frame:
            id_animacao_frame = nome_animacao + '_' + str(n)  # Define o id por exemplo correndo_1
            imagem_loc = path + str(n) + '.png'  # Define o caminho completo da imagems
            imagem_animacao = pygame.image.load(imagem_loc).convert_alpha()  # Carrega a imagem
            imagem_animacao = pygame.transform.scale(imagem_animacao, (sprite_largura, sprite_altura))  # Escala
            self.frames_animacao[id_animacao_frame] = imagem_animacao.copy()  # Adiciona na lista
            for i in range(frame):
                base_frames_animacao.append(id_animacao_frame)
            n += 1
        return base_frames_animacao

    # Função para alterar a animação que está sendo utilizada
    def alterar_animacao(self, acao, frame, nova_acao):
        if acao != nova_acao:
            acao = nova_acao
            frame = 0
        return acao, frame

    # Retorna a lista de animaçoes
    def get_frames_animacao(self):
        return self.frames_animacao
