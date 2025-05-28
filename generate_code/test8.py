class Piece:
    def __init__(self, name, color):
        self.name = name  # e.g., 'P', 'K'
        self.color = color  # 'white' or 'black'

    def __repr__(self):
        symbol = self.name
        return symbol.upper() if self.color == 'white' else symbol.lower()


class Board:
    def __init__(self):
        self.board = self.create_initial_board()
        self.turn = 'white'

    def create_initial_board(self):
        b = [[None] * 8 for _ in range(8)]

        # Back ranks
        order = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for i in range(8):
            b[0][i] = Piece(order[i], 'black')
            b[7][i] = Piece(order[i], 'white')
            b[1][i] = Piece('P', 'black')
            b[6][i] = Piece('P', 'white')
        return b

    def print_board(self):
        print("\n  a b c d e f g h")
        for i, row in enumerate(self.board):
            print(8 - i, end=' ')
            for piece in row:
                print(piece if piece else '.', end=' ')
            print(8 - i)
        print("  a b c d e f g h\n")

    def move(self, start, end):
        sx, sy = self.parse_pos(start)
        ex, ey = self.parse_pos(end)

        piece = self.board[sx][sy]
        if not piece:
            print("No piece at start position.")
            return False
        if piece.color != self.turn:
            print(f"It's {self.turn}'s turn.")
            return False

        valid = self.is_valid_move(piece, sx, sy, ex, ey)
        if not valid:
            print("Invalid move.")
            return False

        captured = self.board[ex][ey]
        self.board[ex][ey] = piece
        self.board[sx][sy] = None

        if self.in_check(self.turn):
            # Undo move
            self.board[sx][sy] = piece
            self.board[ex][ey] = captured
            print("Move puts or leaves king in check.")
            return False

        self.turn = 'black' if self.turn == 'white' else 'white'
        return True

    def parse_pos(self, pos):
        file = ord(pos[0]) - ord('a')
        rank = 8 - int(pos[1])
        return rank, file

    def is_valid_move(self, piece, sx, sy, ex, ey):
        dx = ex - sx
        dy = ey - sy
        target = self.board[ex][ey]
        if target and target.color == piece.color:
            return False

        name = piece.name.upper()
        if name == 'P':  # Pawn
            direction = -1 if piece.color == 'white' else 1
            start_row = 6 if piece.color == 'white' else 1
            if sy == ey:
                if dx == direction and not target:
                    return True
                if sx == start_row and dx == 2 * direction and not target and not self.board[sx + direction][sy]:
                    return True
            elif abs(dy) == 1 and dx == direction and target:
                return True
            return False
        elif name == 'R':  # Rook
            if dx != 0 and dy != 0:
                return False
            return self.clear_path(sx, sy, ex, ey)
        elif name == 'N':  # Knight
            return (abs(dx), abs(dy)) in [(2, 1), (1, 2)]
        elif name == 'B':  # Bishop
            if abs(dx) != abs(dy):
                return False
            return self.clear_path(sx, sy, ex, ey)
        elif name == 'Q':  # Queen
            if dx == 0 or dy == 0 or abs(dx) == abs(dy):
                return self.clear_path(sx, sy, ex, ey)
            return False
        elif name == 'K':  # King
            return max(abs(dx), abs(dy)) == 1
        return False

    def clear_path(self, sx, sy, ex, ey):
        dx = (ex - sx)
        dy = (ey - sy)
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
        x, y = sx + step_x, sy + step_y
        while (x, y) != (ex, ey):
            if self.board[x][y]:
                return False
            x += step_x
            y += step_y
        return True

    def in_check(self, color):
        king_pos = None
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece and piece.name.upper() == 'K' and piece.color == color:
                    king_pos = (i, j)
                    break

        if not king_pos:
            return True  # No king found = checkmate

        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece and piece.color != color:
                    if self.is_valid_move(piece, i, j, king_pos[0], king_pos[1]):
                        return True
        return False


def main():
    board = Board()
    while True:
        board.print_board()
        print(f"{board.turn.capitalize()}'s move (e.g., e2 e4): ", end='')
        move = input().strip().lower()
        if move in ['exit', 'quit']:
            print("Thanks for playing!")
            break
        if len(move.split()) != 2:
            print("Please enter move as: e2 e4")
            continue
        start, end = move.split()
        board.move(start, end)


if __name__ == "__main__":
    main()
