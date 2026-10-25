"""
Tic-Tac-Toe Game - Beginner Mini Project
Two players play on the same keyboard.

Run: python tic_tac_toe.py
"""

def create_board():
    """Create and return a fresh 3 x 3 board."""
    return [[" " for _ in range(3)] for _ in range(3)]


def display_board(board):
    """Display the board with row and column separators."""
    print()
    print("  1   2   3")
    for row_index in range(3):
        print(f"{row_index + 1} " + " | ".join(board[row_index]))
        if row_index < 2:
            print(" ---+---+---")
    print()


def check_winner(board, mark):
    """Return True if mark has three in a row, column, or diagonal."""
    # Check rows
    for row in board:
        if row[0] == mark and row[1] == mark and row[2] == mark:
            return True

    # Check columns
    for col in range(3):
        if board[0][col] == mark and board[1][col] == mark and board[2][col] == mark:
            return True

    # Check both diagonals
    if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark:
        return True

    if board[0][2] == mark and board[1][1] == mark and board[2][0] == mark:
        return True

    return False


def get_move(board, player_name, mark):
    """Ask for row and column until the player enters a valid empty cell."""
    while True:
        print(f"{player_name}'s turn ({mark})")
        choice = input("Enter a cell number (1-9): ").strip()

        if choice == "":
            print("Input cannot be empty. Please try again.")
            continue

        try:
            cell = int(choice)
        except ValueError:
            print("Please enter a number from 1 to 9.")
            continue

        if cell < 1 or cell > 9:
            print("Invalid number. Choose a cell from 1 to 9.")
            continue

        row = (cell - 1) // 3
        col = (cell - 1) % 3

        if board[row][col] != " ":
            print("That cell is already occupied. Choose an empty cell.")
            continue

        return row, col


def ask_play_again():
    """Return True if the players want another round."""
    while True:
        answer = input("Would you like to play again? (y/n): ").strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("Please enter y for yes or n for no.")


def play_game(player1, player2):
    """Play one complete round; return the winning player's name or None for a draw."""
    board = create_board()
    players = [(player1, "X"), (player2, "O")]
    current_index = 0
    move_count = 0

    print("\nNew game started!")
    display_board(board)

    while True:
        player_name, mark = players[current_index]
        row, col = get_move(board, player_name, mark)
        board[row][col] = mark
        move_count += 1

        display_board(board)

        if check_winner(board, mark):
            print(f"Congratulations, {player_name} ({mark}) wins!")
            return player_name

        if move_count == 9:
            print("It's a draw! No one wins this round.")
            return None

        # Switch between player 1 and player 2.
        current_index = 1 - current_index


def main():
    print("=" * 36)
    print("       TIC-TAC-TOE GAME")
    print("=" * 36)

    player1 = input("Enter Player 1 name (X): ").strip() or "Player 1"
    player2 = input("Enter Player 2 name (O): ").strip() or "Player 2"

    scores = {player1: 0, player2: 0}
    draws = 0
    rounds = 0

    while True:
        winner = play_game(player1, player2)
        rounds += 1

        if winner is None:
            draws += 1
        else:
            scores[winner] += 1

        print("\n--- Scoreboard ---")
        print(f"{player1} (X): {scores[player1]}")
        print(f"{player2} (O): {scores[player2]}")
        print(f"Draws: {draws} | Rounds played: {rounds}")

        if not ask_play_again():
            print("\nThanks for playing Tic-Tac-Toe. Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nGame ended. Thanks for playing!")
