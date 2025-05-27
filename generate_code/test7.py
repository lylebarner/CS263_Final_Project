import random
import time
import os
import sys
import threading

WIDTH = 60
HEIGHT = 20
DELAY = 0.2
LIVE = '⬜'
DEAD = '  '

class GameOfLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.create_grid()
        self.running = True

    def create_grid(self):
        return [[random.choice([0, 1]) for _ in range(self.width)] for _ in range(self.height)]

    def print_grid(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.grid:
            print(''.join([LIVE if cell else DEAD for cell in row]))

    def count_neighbors(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.height and 0 <= ny < self.width:
                count += self.grid[nx][ny]
        return count

    def update(self):
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] == 1:
                    if neighbors in [2, 3]:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if neighbors == 3:
                        new_grid[i][j] = 1
        self.grid = new_grid

    def toggle_running(self):
        self.running = not self.running

    def run(self):
        while True:
            if self.running:
                self.print_grid()
                self.update()
            time.sleep(DELAY)

def keyboard_listener(game):
    try:
        import msvcrt  # Windows
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b' ':
                    game.toggle_running()
                elif key == b'q':
                    print("Exiting...")
                    os._exit(0)
    except ImportError:
        import termios
        import tty
        def getch():
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                return sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

        while True:
            key = getch()
            if key == ' ':
                game.toggle_running()
            elif key == 'q':
                print("Exiting...")
                os._exit(0)

def main():
    print("Conway's Game of Life")
    print("Controls:")
    print("  [space] Pause/Resume")
    print("  [q]     Quit")
    time.sleep(2)

    game = GameOfLife(WIDTH, HEIGHT)
    threading.Thread(target=keyboard_listener, args=(game,), daemon=True).start()
    game.run()

if __name__ == "__main__":
    main()
