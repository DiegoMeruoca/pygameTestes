import pygame


class Mapa:
    def __init__(self, bloco_superficie, bloco_base, fundo, obj_perto, obj_longe, musica, display):
        self.bloco_superficie = bloco_superficie
        self.bloco_base = bloco_base
        self.fundo = fundo
        self.obj_cenario_perto = obj_perto
        self.obj_cenario_longe = obj_longe
        self.musica_fundo = musica
        self.objetos_cenario = []
        self.display = display
        self.rolagem_tela = 0
        self.colisao_blocos = []
        self.colisoes = []
        self.mapa_game = self.carregar_mapa('mapas/mapa1')

    # Carrega a base do nosos mapa de um txt (0-Epaço vazio(céu) 1-Bloco de terra 2-Bloco com grama)
    def carregar_mapa(self, path):
        arquivo = open(path + '.txt', 'r')
        dados = arquivo.read()
        arquivo.close()
        dados = dados.split('\n')
        mapa = []
        for linha in dados:
            mapa.append(list(linha))
        return mapa

    # Insere na tela os objetos de fundo do cenário de acordo com a variavel objetos_cenario
    def preencher_fundo_cenario(self):
        for objeto in self.objetos_cenario:
            posicao_obj = (objeto[1][0] - self.rolagem_tela[0] * objeto[0],
                           objeto[1][1] - self.rolagem_tela[1] * objeto[0])
            if objeto[1][2] == 'ilha_perto':
                self.display.blit(self.obj_cenario_perto, posicao_obj)
            elif objeto[1][2] == 'ilha_fundo':
                self.display.blit(self.obj_cenario_longe, posicao_obj)
