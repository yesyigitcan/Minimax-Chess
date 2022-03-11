import chess
import math

# This function gives the inverse matrix for chess board of given board state matrix
def mirror(valList):
    temp = []
    lenList = len(valList)
    for i in range(lenList):
        temp.append(valList[lenList-i-1])
    return temp

# This function calculates evaluation score of the current board
def evaluation(board):
    evaluation = 0
    for i in range(64):
        x = board.color_at(i)
        if x is not None:
            if x == chess.WHITE:
                # White pieces always try to maximize
                evaluation += getValue(str(board.piece_at(i)), i, chess.WHITE)
            else:
                # Black pieces always try to minimize
                evaluation -= getValue(str(board.piece_at(i)), i, chess.BLACK)
    return evaluation

# This function gives the value of each piece on the board
def getValue(piece, i, color):
    # values and the value matrix depending on piece's current state is set after search on web
    # many websites say I need to set a matrix for each state on board to improve my ai movement
    if(piece == None):
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 100
        pawn_matrix = [0, 0, 0, 0, 0, 0, 0, 0,
                       50, 50, 50, 50, 50, 50, 50, 50,
                       10, 10, 20, 30, 30, 20, 10, 10,
                       5, 5, 10, 25, 25, 10, 5, 5,
                       0, 0, 0, 20, 20, 0, 0, 0,
                       5, -5, -10, 0, 0, -10, -5, 5,
                       5, 10, 10, -20, -20, 10, 10, 5,
                       0, 0, 0, 0, 0, 0, 0, 0]
        if color != chess.WHITE:
            pawn_matrix = mirror(pawn_matrix)

        value += pawn_matrix[i]
    elif piece == "N" or piece == "n":
        value = 300
        knight_matrix = [-50, -40, -30, -30, -30, -30, -40, -50,
                         -40, -20, 0, 0, 0, 0, -20, -40,
                         -30, 0, 10, 15, 15, 10, 0, -30,
                         -30, 5, 15, 20, 20, 15, 5, -30,
                         -30, 0, 15, 20, 20, 15, 0, -30,
                         -30, 5, 10, 15, 15, 10, 5, -30,
                         -40, -20, 0, 5, 5, 0, -20, -40,
                         -50, -40, -30, -30, -30, -30, -40, -50]
        if color != chess.WHITE:
            knight_matrix = mirror(knight_matrix)
        value += knight_matrix[i]

    elif piece == "B" or piece == "b":
        value = 300
        bishop_matrix = [-20, -10, -10, -10, -10, -10, -10, -20,
                             -10, 0, 0, 0, 0, 0, 0, -10,
                             -10, 0, 5, 10, 10, 5, 0, -10,
                             -10, 5, 5, 10, 10, 5, 5, -10,
                             -10, 0, 10, 10, 10, 10, 0, -10,
                             -10, 10, 10, 10, 10, 10, 10, -10,
                             -10, 5, 0, 0, 0, 0, 5, -10,
                             -20, -10, -10, -10, -10, -10, -10, -20]
        if color != chess.WHITE:
            bishop_matrix = mirror(bishop_matrix)
        value += bishop_matrix[i]
    elif piece == "R" or piece == "r":
        value = 500
        rook_matrix = [  0,  0,  0,  0,  0,  0,  0,  0,
          5, 10, 10, 10, 10, 10, 10,  5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
          0,  0,  0,  5,  5,  0,  0,  0]
        if color != chess.WHITE:
            rook_matrix = mirror(rook_matrix)
        value += rook_matrix[i]
    elif piece == "Q" or piece == "q":
        value = 900
        queen_matrix = [-20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20]
        if color != chess.WHITE:
            queen_matrix = mirror(queen_matrix)
        value += queen_matrix[i]
    elif piece == 'K' or piece == 'k':
        value = 9000
        king_matrix = [-30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
         20, 20,  0,  0,  0,  0, 20, 20,
         20, 30, 10,  0,  0, 10, 30, 20]
        if color != chess.WHITE:
            king_matrix = mirror(king_matrix)
        value += king_matrix[i]

    return value

def minimax(depth, color, board, alpha, beta, ai_color):
    # Checking if there is a checkmate. If there is, it checks if ai wins or not
    # When depth is higher importance of checkmate getting lower. It means 2nd move checkmate is more valuable than 3rd
    # move check mate

    if board.is_checkmate():
        if color == ai_color: # AI won
            if ai_color == chess.WHITE:
                return 100000 * depth
            else:
                return -100000 * depth
        else:
            if ai_color == chess.WHITE:
                return -100000 * depth
            else:
                return 100000 * depth
    # If there is stalemate, it is neither gain nor lose for ai
    if board.is_stalemate():
        return 0
    # When it reaches the last leaf of graph, it calculates evaluation point for the state of current board
    if depth == 0:
        return evaluation(board)

    if color == chess.WHITE:
        # White pieces always trying to maximize no matter if ai color is white or not
        # bestMove is used to compare current value with previous values of same legal moves set
        bestMove = -math.inf
        for child in board.legal_moves:
            board.push(child)
            eval = minimax(depth - 1, chess.BLACK , board, alpha, beta, ai_color)
            board.pop()
            # Checking of 100000 is giving info about if any checkmate happened or not
            if eval / 100000 >= 1 or eval / 100000 <= -1:
                return eval
            bestMove = max(bestMove, eval)
            # alphas and betas providing less calculation by skipping unnecessary calculation if previous results satisfy
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return bestMove
    else:
        bestMove = math.inf
        # Black pieces always trying to minimize no matter if ai color is white or not
        for child in board.legal_moves:
            board.push(child)
            eval = minimax(depth - 1, True, board, alpha, beta, ai_color)
            board.pop()
            # Checking of 100000 is giving info about if any checkmate happened or not
            if eval / 100000 >= 1 or eval / 100000 <= -1:
                return eval
            bestMove = min(bestMove, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return bestMove

def ai_play(board):
    plays = []
    plays_es = [] # plays evaluation scores
    # Determine the color of ai by checking board's current turn info
    if board.fen().split(" ")[1] == "w":
        color = chess.WHITE
    else:
        color = chess.BLACK
    for play in board.legal_moves:
        plays.append(str(play))
        board.push(play)
        # if ai can make checkmate for first move, it is the highest value checkmate and value is infinite
        if board.is_checkmate():
            if color == chess.WHITE:
                plays_es.append(math.inf)
            else:
                plays_es.append(-math.inf)
        else:
            # if there is no ai checkmate for first move, then go to minimax function and search for it
            # or at least calculate the evaluation score for any case
            # For some cases depth 5 pushes system performance. Frame sometimes looks like it is crashed but it is not
            # According to my tests, depth 3 is one that gives the best performance results.
            plays_es.append(minimax(5, color , board, -math.inf, math.inf, color))
        board.pop()

    # In order to determine what move is happened by ai and what are the values for evaluation, I print these two
    # set of legal moves and their scores
    print(plays)
    print(plays_es)

    # If ai color is white, it needs to check for the maximum value, otherwise for the minimum value
    # I could take a random of the same maximum scores, but I just do not want to do for no purpose
    if color == chess.WHITE:
        played = plays[plays_es.index(max(plays_es))]
    else:
        played = plays[plays_es.index(min(plays_es))]
    print("Played: ", played) # Print which move is played by ai
    return played