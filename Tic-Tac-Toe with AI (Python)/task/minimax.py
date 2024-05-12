# human
hu_player = "O"
# ai
ai_player = "X"

# this is the board flattened and filled with some values to easier asses the Artificial Intelligence.
# orig_board = ["O", 1, "X", "X", 4, "X", 6, "O", "O"]
orig_board = [0, 1, 2, 3, 4, 5, 6, 7, 8]

# keeps count of function calls
fc = 0


# returns the available spots on the board
def empty_indices(board):
    return [i for i, x in enumerate(board) if x != "O" and x != "X"]


# winning combinations using the board indices
def winning(board, player):
    wins = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    for win in wins:
        if board[win[0]] == board[win[1]] == board[win[2]] == player:
            return True
    return False


# the main minimax function
def minimax(new_board, player):
    global fc
    # add one to function calls
    fc += 1

    # available spots
    available_spots = empty_indices(new_board)

    # checks for the terminal states such as win, lose, and tie and returning a value accordingly
    if winning(new_board, hu_player):
        return {"score": -10}
    elif winning(new_board, ai_player):
        return {"score": 10}
    elif len(available_spots) == 0:
        return {"score": 0}

    # an array to collect all the objects
    moves = []

    # loop through available spots
    for i in range(len(available_spots)):
        # create an object for each and store the index of that spot that was stored as a number in the object's
        # index key
        move = {"index": new_board[available_spots[i]]}

        # set the empty spot to the current player
        new_board[available_spots[i]] = player

        # if collect the score resulted from calling minimax on the opponent of the current player
        if player == ai_player:
            result = minimax(new_board, hu_player)
            move["score"] = result["score"]
        else:
            result = minimax(new_board, ai_player)
            move["score"] = result["score"]

        # reset the spot to empty
        new_board[available_spots[i]] = move["index"]

        # append the object to the array
        moves.append(move)

    # if it is the computer's turn loop over the moves and choose the move with the highest score
    if player == ai_player:
        best_score = -10000
        best_move = None
        for i in range(len(moves)):
            if moves[i]["score"] > best_score:
                best_score = moves[i]["score"]
                best_move = i
    else:
        # else loop over the moves and choose the move with the lowest score
        best_score = 10000
        best_move = None
        for i in range(len(moves)):
            if moves[i]["score"] < best_score:
                best_score = moves[i]["score"]
                best_move = i

    # return the chosen move (object) from the array to the higher depth
    return moves[best_move]
