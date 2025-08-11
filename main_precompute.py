import numpy as np
import time

class BoopGame:
    ID_LIST = (-1, 1)
    NEIGHBORS = np.array([
        (1, 1), (1, 0), (1, -1),
        (0, 1), (0, -1),
        (-1, 1), (-1, 0), (-1, -1)
    ], dtype=np.int8)

    def __init__(self):
        self.board = np.zeros((6, 6), dtype=np.int8)
        self.turn = 1
        self.TRIPLETS = self._generate_triplets()

    def _generate_triplets(self):
        triplets = []
        for x in range(6):
            for y in range(6):
                if x <= 3:
                    triplets.append([(x+i, y) for i in range(3)])
                if y <= 3:
                    triplets.append([(x, y+i) for i in range(3)])
                if x <= 3 and y <= 3:
                    triplets.append([(x+i, y+i) for i in range(3)])
                if x <= 3 and y >= 2:
                    triplets.append([(x+i, y-i) for i in range(3)])
        return np.array(triplets, dtype=np.int8)  # Shape: (N, 3, 2)

    def __repr__(self):
        return str(self.board)

    def in_bounds(self, x, y):
        return 0 <= x < 6 and 0 <= y < 6

    def make_move(self, x, y, playerID):
        assert playerID in self.ID_LIST, "Invalid player ID"
        assert self.board[x, y] == 0, f"Space Occupied at ({x}, {y})"

        # Boop logic
        for dx, dy in self.NEIGHBORS:
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny) and self.board[nx, ny] != 0:
                nnx, nny = nx + dx, ny + dy
                if self.in_bounds(nnx, nny):
                    if self.board[nnx, nny] == 0:
                        self.board[nnx, nny] = self.board[nx, ny]
                        self.board[nx, ny] = 0
                else:
                    self.board[nx, ny] = 0

        self.board[x, y] = playerID
        # print(self.board)

        winner = self.check_winner()
        if winner:
            return
            # print(f'Player: {winner} wins!')

    def check_winner(self):
        """Vectorized winner check using precomputed triplets."""
        coords = self.TRIPLETS  # (N, 3, 2)
        bvals = self.board[coords[:, :, 0], coords[:, :, 1]]  # (N, 3)

        # Check if all values in triplet are equal and nonzero
        is_equal = (bvals[:, 0] == bvals[:, 1]) & (bvals[:, 1] == bvals[:, 2])
        non_zero = bvals[:, 0] != 0
        mask = is_equal & non_zero

        if np.any(mask):
            return bvals[mask][0, 0]  # Return the winning ID
        return 0

def benchmark_random_games(num_games=1000, max_moves=50):
    game = BoopGame()
    moves_made = 0
    winners = 0
    start_time = time.time()

    for _ in range(num_games):
        game.__init__()  # Reset board
        move_count = 0
        while move_count < max_moves:
            # Choose random empty cell
            empty_cells = np.argwhere(game.board == 0)
            if empty_cells.size == 0:
                break  # Board full

            x, y = empty_cells[np.random.choice(len(empty_cells))]
            player = game.ID_LIST[move_count % 2]

            game.make_move(x, y, player)

            move_count += 1
            moves_made += 1

            if game.check_winner() != 0:
                winners += 1
                break

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Simulated {num_games} games with up to {max_moves} moves each")
    print(f"Total moves made: {moves_made}")
    print(f"Games with winner: {winners}")
    print(f"Total time: {total_time:.4f} seconds")
    print(f"Average time per move: {total_time / moves_made * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark_random_games()
