import pygame
from tabuleiro import *
from minimax_ia import escolher_melhor_jogada

pygame.init()

largura_tela = 800
altura_tela = 800
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("JOGO HEX 11 x 11")
fonte = pygame.font.Font(None, 40)

largura_botao = 100
altura_botao = 40
espacamento_x = 120
espacamento_y = 80
inicio_x = 60
inicio_y = 200

margem_esquerda, margem_superior = calcular_margens(largura_tela, altura_tela)

jogador_vez = vermelho
menu_ativo = True
fase_menu = "algoritmo"
algoritmo_ia = None
profundidade_escolhida = None

def desenhar_botao(tela, texto, x, y, largura, altura, cor_fundo, cor_texto, fonte):
    pygame.draw.rect(tela, cor_fundo, (x, y, largura, altura), border_radius=10)
    texto_renderizado = fonte.render(texto, True, cor_texto)
    texto_centralizado = texto_renderizado.get_rect(center=(x + largura // 2, y + altura // 2))
    tela.blit(texto_renderizado, texto_centralizado)

def clique_dentro(x, y, largura, altura, pos_mouse):
    px, py = pos_mouse
    return x <= px <= x + largura and y <= py <= y + altura

while menu_ativo:
    tela.fill(branco)

    if fase_menu == "algoritmo":
        botao_largura = 300
        x_central = (largura_tela - botao_largura) // 2  

        desenhar_botao(tela, "Minimax puro", x_central, 200, botao_largura, 50, cinza, preto, fonte)
        desenhar_botao(tela, "Minimax com Alfa-Beta", x_central, 300, botao_largura, 50, cinza, preto, fonte)

    elif fase_menu == "profundidade":
        for i in range(4):
            numero = i + 1
            coluna = i % 5
            linha = i // 5
            x = inicio_x + coluna * espacamento_x
            y = inicio_y + linha * espacamento_y
            desenhar_botao(tela, f"{numero}", x, y, largura_botao, altura_botao, cinza, preto, fonte)

    pygame.display.flip()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if fase_menu == "algoritmo":
                if clique_dentro(x_central, 200, botao_largura, altura_botao, pos):
                    algoritmo_ia = "minimax"
                    fase_menu = "profundidade"
                elif clique_dentro(x_central, 300, botao_largura, altura_botao, pos):
                    algoritmo_ia = "alfa_beta"
                    fase_menu = "profundidade"
            elif fase_menu == "profundidade":
                for i in range(4):
                    numero = i + 1
                    coluna = i % 5
                    linha = i // 5
                    x = inicio_x + coluna * espacamento_x
                    y = inicio_y + linha * espacamento_y
                    if clique_dentro(x, y, largura_botao, altura_botao, pos):
                        profundidade_escolhida = numero
                        menu_ativo = False

vencedor = None
rodando = True

while rodando:
    tela.fill(branco)
    desenhar_tabuleiro(tela, margem_esquerda, margem_superior)

    if vencedor:
        texto_vitoria = f"Vitória do jogador {'VERMELHO' if vencedor == vermelho else 'AZUL'}"
        texto_renderizado = fonte.render(texto_vitoria, True, (0, 128, 0))
        rect = texto_renderizado.get_rect(center=(largura_tela // 2, 50))
        tela.blit(texto_renderizado, rect)

    pygame.display.flip()

    if jogador_vez == azul and not vencedor:
        linha, coluna = escolher_melhor_jogada(tabuleiro, profundidade_escolhida, azul, algoritmo_ia)
        tabuleiro[linha][coluna] = azul
        if verificar_vitoria(azul):
            vencedor = azul
        else:
            jogador_vez = vermelho

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and not vencedor:
            pos = pygame.mouse.get_pos()
            celula = obter_celula_clicada(pos, margem_esquerda, margem_superior)
            if celula:
                linha, coluna = celula
                if tabuleiro[linha][coluna] is None:
                    tabuleiro[linha][coluna] = jogador_vez
                    if verificar_vitoria(jogador_vez):
                        vencedor = jogador_vez
                    else:
                        jogador_vez = azul if jogador_vez == vermelho else vermelho

pygame.quit()
