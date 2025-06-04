import pygame
import math

branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
azul = (0, 0, 255)
cinza = (180, 180, 180)

tamanho = 11
raio = 25
altura_hexagono = math.sqrt(3) * raio  #1.73 * 25 = 43.3

tabuleiro = [[None for _ in range(tamanho)] for _ in range(tamanho)]

def calcular_margens(largura_tela, altura_tela):
    largura_total = tamanho * raio * 1.5
    altura_total = tamanho * altura_hexagono + ((tamanho - 1) * altura_hexagono / 2)
    margem_esquerda = (largura_tela - largura_total) / 2
    margem_superior = (altura_tela - altura_total) / 2
    return margem_esquerda, margem_superior

def desenhar_hexagono(tela, centro_x, centro_y, raio, cor):
    pontos = []
    for i in range(6):
        angulo = math.radians(60 * i)
        x = centro_x + raio * math.cos(angulo)
        y = centro_y + raio * math.sin(angulo)
        pontos.append((x, y))
    pygame.draw.polygon(tela, cor, pontos)
    pygame.draw.polygon(tela, preto, pontos, 2)
    
def desenhar_tabuleiro(tela, margem_esquerda, margem_superior):
    for linha in range(tamanho):
        for coluna in range(tamanho):
            centro_x = margem_esquerda + coluna * raio * 1.5
            centro_y = margem_superior + linha * altura_hexagono + (coluna * altura_hexagono / 2)
            cor = tabuleiro[linha][coluna] or cinza
            desenhar_hexagono(tela, centro_x, centro_y, raio, cor)

def obter_celula_clicada(pos_mouse, margem_esquerda, margem_superior):
    for linha in range(tamanho):
        for coluna in range(tamanho):
            centro_x = margem_esquerda + coluna * raio * 1.5
            centro_y = margem_superior + linha * altura_hexagono + (coluna * altura_hexagono / 2)
            distancia = math.hypot(pos_mouse[0] - centro_x, pos_mouse[1] - centro_y)
            if distancia < raio:
                return linha, coluna
    return None

def verificar_vitoria(jogador_atual):
    direcoes_hexagonais = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]

    def buscar_conexao(linha_atual, coluna_atual, posicoes_visitadas):
        if (linha_atual, coluna_atual) in posicoes_visitadas:
            return False

        posicoes_visitadas.add((linha_atual, coluna_atual))

        if jogador_atual == vermelho and linha_atual == tamanho - 1:
            return True
        if jogador_atual == azul and coluna_atual == tamanho - 1:
            return True

        for deslocamento_linha, deslocamento_coluna in direcoes_hexagonais:
            nova_linha = linha_atual + deslocamento_linha
            nova_coluna = coluna_atual + deslocamento_coluna

            if 0 <= nova_linha < tamanho and 0 <= nova_coluna < tamanho:
                if tabuleiro[nova_linha][nova_coluna] == jogador_atual:
                    if buscar_conexao(nova_linha, nova_coluna, posicoes_visitadas):
                        return True

        return False

    if jogador_atual == vermelho:
        for coluna_inicial in range(tamanho):
            if tabuleiro[0][coluna_inicial] == vermelho:
                if buscar_conexao(0, coluna_inicial, set()):
                    return True
    else: 
        for linha_inicial in range(tamanho):
            if tabuleiro[linha_inicial][0] == azul:
                if buscar_conexao(linha_inicial, 0, set()):
                    return True

    return False


