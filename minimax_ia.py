from tabuleiro import *
import random

def avaliar_tabuleiro(tabuleiro, jogador_ia):
    jogador_ia = azul
    jogador_oponente = vermelho

    contador_ia = 0
    contador_oponente = 0
    pontos_pontes_virtuais = 0
    penalidade_bloqueio = 0

    for linha in range(tamanho):
        for coluna in range(tamanho):
            celula = tabuleiro[linha][coluna]
            if celula == jogador_ia:
                contador_ia += 1
                if linha + 1 < tamanho and coluna + 1 < tamanho:
                    if (
                        tabuleiro[linha + 1][coluna + 1] == jogador_ia and
                        tabuleiro[linha][coluna + 1] is None
                    ):
                        pontos_pontes_virtuais += 1
                if linha + 1 < tamanho and coluna - 1 >= 0:
                    if (
                        tabuleiro[linha + 1][coluna - 1] == jogador_ia and
                        tabuleiro[linha + 1][coluna] is None
                    ):
                        pontos_pontes_virtuais += 1

            elif celula == jogador_oponente:
                contador_oponente += 1

    for i in range(tamanho):
        if tabuleiro[0][i] == jogador_oponente or tabuleiro[tamanho - 1][i] == jogador_oponente:
            penalidade_bloqueio += 2

    return (
        (contador_ia - contador_oponente) * 1.5 +
        pontos_pontes_virtuais * 3 -
        penalidade_bloqueio
    )


def minimax(tabuleiro, profundidade, maximizando, jogador_ia, jogador_da_vez):
    if profundidade == 0:
        return avaliar_tabuleiro(tabuleiro, jogador_ia)
    melhor_valor = float("-inf") if maximizando else float("inf")
    for linha in range(tamanho):
        for coluna in range(tamanho):
            if tabuleiro[linha][coluna] is None:
                tabuleiro_simulado = [linha[:] for linha in tabuleiro]
                tabuleiro_simulado[linha][coluna] = jogador_da_vez
                proximo_jogador = vermelho if jogador_da_vez == azul else azul
                valor = minimax(tabuleiro_simulado, profundidade - 1, not maximizando, jogador_ia, proximo_jogador)
                
                if maximizando:
                    melhor_valor = max(melhor_valor, valor)
                else:
                    melhor_valor = min(melhor_valor, valor)

    return melhor_valor

def poda_alfa_beta(tabuleiro, profundidade, alfa, beta, maximizando, jogador_ia, jogador_da_vez):
    if profundidade == 0:
        return avaliar_tabuleiro(tabuleiro, jogador_ia)
    melhor_valor = float("-inf") if maximizando else float("inf")
    for linha in range(tamanho):
        for coluna in range(tamanho):
            if tabuleiro[linha][coluna] is None:
                tabuleiro_simulado = [linha[:] for linha in tabuleiro]
                tabuleiro_simulado[linha][coluna] = jogador_da_vez
                proximo_jogador = vermelho if jogador_da_vez == azul else azul
                valor = poda_alfa_beta(tabuleiro_simulado, profundidade -1, alfa, beta, not maximizando, jogador_ia, proximo_jogador)
                if maximizando:
                    melhor_valor = max(melhor_valor, valor)
                    alfa = max(alfa, melhor_valor)
                else:
                    melhor_valor = min(melhor_valor, valor)
                    beta = min(beta, melhor_valor)
                    
                if beta <= alfa:
                    break
    return melhor_valor
                

def escolher_melhor_jogada(tabuleiro, profundidade, jogador_ia, algoritmo="minimax"):
    melhor_valor = float("-inf")
    melhores_jogadas = []
    jogador_oponente = vermelho if jogador_ia == azul else azul

    for linha in range(tamanho):
        for coluna in range(tamanho):
            if tabuleiro[linha][coluna] is None:
                tabuleiro_simulado = [linha[:] for linha in tabuleiro]
                tabuleiro_simulado[linha][coluna] = jogador_ia

                if algoritmo == "minimax":
                    valor = minimax(tabuleiro_simulado, profundidade - 1, False, jogador_ia, jogador_oponente)
                else:
                    valor = poda_alfa_beta(tabuleiro_simulado, profundidade - 1, float("-inf"), float("inf"), False, jogador_ia, jogador_oponente)

                if valor > melhor_valor:
                    melhor_valor = valor
                    melhores_jogadas = [(linha, coluna)] 
                elif valor == melhor_valor:
                    melhores_jogadas.append((linha, coluna)) 

    return random.choice(melhores_jogadas) if melhores_jogadas else None

    
