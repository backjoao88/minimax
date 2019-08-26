 
# @author João Paulo Back
# @author Mathias Artur Schulz

from math import inf # Número float infinito
from random import choice
import platform
import time
from os import system

JOGADOR = -1
COMPUTADOR = +1
tabuleiro = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


# Método que verifica se um dos players ganharam
# Se o computador ganhou retorna +1
# Se o jogador ganhou retorna -1
# Se houve empate retorna 0
def verificaPossuiGanhador(estadoTabuleiro):
    if verificaSeGanhou(estadoTabuleiro, COMPUTADOR):
        return +1
    elif verificaSeGanhou(estadoTabuleiro, JOGADOR):
        return -1
    else:
        return 0


# Verifica se ou jogador ou o computador ganhou
# De acordo com as possibilidades em três linhas, três colunas ou duas diagonais
# -1 -1 -1 = jogador ganhou
# +1 +1 +1 = computador ganhou
def verificaSeGanhou(estadoTabuleiro, player):
    possibilidades_vitoria = [
        [estadoTabuleiro[0][0], estadoTabuleiro[0][1], estadoTabuleiro[0][2]],
        [estadoTabuleiro[1][0], estadoTabuleiro[1][1], estadoTabuleiro[1][2]],
        [estadoTabuleiro[2][0], estadoTabuleiro[2][1], estadoTabuleiro[2][2]],
        [estadoTabuleiro[0][0], estadoTabuleiro[1][0], estadoTabuleiro[2][0]],
        [estadoTabuleiro[0][1], estadoTabuleiro[1][1], estadoTabuleiro[2][1]],
        [estadoTabuleiro[0][2], estadoTabuleiro[1][2], estadoTabuleiro[2][2]],
        [estadoTabuleiro[0][0], estadoTabuleiro[1][1], estadoTabuleiro[2][2]],
        [estadoTabuleiro[2][0], estadoTabuleiro[1][1], estadoTabuleiro[0][2]],
    ]
    if [player, player, player] in possibilidades_vitoria:
        return True
    else:
        return False


# Método que testa se ouve um ganhador e o jogo terminou
def fimDeJogo(estadoTabuleiro):
    return verificaSeGanhou(estadoTabuleiro, JOGADOR) or verificaSeGanhou(estadoTabuleiro, COMPUTADOR)


# Método que retorna uma lista com todas as células vazias no tabuleiro
def celulasVazias(estadoTabuleiro):
    celulas = []
    for x, row in enumerate(estadoTabuleiro):
        for y, celula in enumerate(row):
            if celula == 0:
                celulas.append([x, y])

    return celulas


# Verifica se o movimento é válido
# Para ser válido deve ser uma célula vazia
def validaMovimento(x, y):
    if [x, y] in celulasVazias(tabuleiro):
        return True
    else:
        return False


# Seta o movimento no tabuleiro se o movimento for válido
def setarMovimento(x, y, player):
    if validaMovimento(x, y):
        tabuleiro[x][y] = player
        return True
    else:
        return False


# Método minimax que escolhe o melhor movimento ao COMPUTADOR
def minimax(estadoTabuleiro, profundidade, player):

    # COMPUTADOR escolhe a melhor opção
    # JOGADOR escolhe a pior opção
    if player == COMPUTADOR:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, +inf]

    if profundidade == 0 or fimDeJogo(estadoTabuleiro):
        score = verificaPossuiGanhador(estadoTabuleiro)
        return [-1, -1, score]

    # Percorre as células vazias
    # Cada célula possui uma posição [x,y]
    for celula in celulasVazias(estadoTabuleiro):
        x, y = celula[0], celula[1]
        estadoTabuleiro[x][y] = player
        # Recursidade para avançar entre as camadas da árvore
        # Cada camada representa um player diferente
        
        score = minimax(estadoTabuleiro, profundidade - 1, -player)
        
        estadoTabuleiro[x][y] = 0
        score[0], score[1] = x, y

        if player == COMPUTADOR:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best # [melhor linha, melhor coluna, melhor score]


# Limpa o console
def clearConsole():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


# Apresenta o tabuleiro no console
def apresentaTabuleiro(estadoTabuleiro, simboloComputador, simboloJogador):
    chars = {
        -1: simboloJogador,
        +1: simboloComputador,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in estadoTabuleiro:
        for celula in row:
            symbol = chars[celula]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


# Método que chama o Minimax
def vezDoComputador(simboloComputador, simboloJogador):
    # Verifica se o jogo ainda não terminou
    profundidade = len(celulasVazias(tabuleiro))
    if profundidade == 0 or fimDeJogo(tabuleiro):
        return

    # clearConsole()
    print(f'VEZ DO COMPUTADOR[{simboloComputador}]')
    apresentaTabuleiro(tabuleiro, simboloComputador, simboloJogador)

    print('\n\n\n\n\n')
    if profundidade == 9:
        x, y = 0, 0
    else:
        move = minimax(tabuleiro, profundidade, COMPUTADOR)
        x, y = move[0], move[1]

    setarMovimento(x, y, COMPUTADOR)
    # Tempo de espera de 1 segundos
    time.sleep(1)


# O jogador escolhe uma posição válida no tabuleiro
def vezDoJogador(simboloComputador, simboloJogador):
    profundidade = len(celulasVazias(tabuleiro))
    if profundidade == 0 or fimDeJogo(tabuleiro):
        return

    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    # clearConsole()
    print(f'VEZ DO HUMANO [{simboloJogador}]')
    apresentaTabuleiro(tabuleiro, simboloComputador, simboloJogador)

    while move < 1 or move > 9:
        try:
            move = int(input('Digite um número de 1 a 9: '))
            coord = moves[move]
            can_move = setarMovimento(coord[0], coord[1], JOGADOR)

            if not can_move:
                print('Movimento inválido')
                move = -1
        except (EOFError, KeytabuleiroInterrupt):
            print('Fim')
            exit()
        except (KeyError, ValueError):
            print('Movimento inválido')


# Função principal
def main():
    # Inicia limpando o console
    # clearConsole()
    print('### JOGO DA VELHA ###')

    # Símbolo: X ou O
    simboloJogador = ''
    simboloComputador = ''
    # Verifica se jogador é o primeiro ou não
    jogadorPrimeiro = ''

    # Jogador escolhe X ou O
    while simboloJogador != 'O' and simboloJogador != 'X':
        try:
            print('\nEscolha o seu símbolo (X ou O) ')
            simboloJogador = input('\nEscolha: ').upper()
        except (EOFError, KeytabuleiroInterrupt):
            print('\n\n:(\n')
            exit()

    # Seta o símbolo do COMPUTADORutador
    if simboloJogador == 'X':
        simboloComputador = 'O'
    else:
        simboloComputador = 'X'

    # Limpa o console
    # clearConsole()

    # Verifica quem iniciará primeiro
    while jogadorPrimeiro != 'S' and jogadorPrimeiro != 'N':
        try:
            jogadorPrimeiro = input('Deseja iniciar primeiro? (S/N): ').upper()
        except (EOFError, KeytabuleiroInterrupt):
            print('\n\n:(\n')
            exit()

    # Main loop of this game
    while len(celulasVazias(tabuleiro)) > 0 and not fimDeJogo(tabuleiro):
        if jogadorPrimeiro == 'N':
            vezDoComputador(simboloComputador, simboloJogador)
            jogadorPrimeiro = ''

        vezDoJogador(simboloComputador, simboloJogador)
        vezDoComputador(simboloComputador, simboloJogador)

    # Game over message
    if verificaSeGanhou(tabuleiro, JOGADOR):
        # clearConsole()
        print(f'VEZ DO JOGADOR[{simboloJogador}]')
        apresentaTabuleiro(tabuleiro, simboloComputador, simboloJogador)
        print('Você venceu!')
    elif verificaSeGanhou(tabuleiro, COMPUTADOR):
        # clearConsole()
        print(f'VEZ DO COMPUTADOR [{simboloComputador}]')
        apresentaTabuleiro(tabuleiro, simboloComputador, simboloJogador)
        print('Vocẽ foi derrotado!')
    else:
        # clearConsole()
        apresentaTabuleiro(tabuleiro, simboloComputador, simboloJogador)
        print('Empate!')

    exit()


main()
