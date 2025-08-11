import numpy as np


class BoopGame:
    ID_LIST = (-1, 1)
    NEIGHBORS = (
        (1,1),
        (1,0),
        (1,-1),
        (0,1),
        (0,-1),
        (-1,1),
        (-1,0),
        (-1,-1)
    )

    def __init__(self):
        self.board = np.zeros((6,6), dtype=np.int8)
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
        return np.array(triplets, dtype=np.int8)   
    
    def __repr__(self):        
        return str(self.board)
    
    def in_bounds(self,x, y):
        return 0 <= x < 6 and 0 <= y < 6

    def make_move(self, x, y, playerID):
        assert playerID in self.ID_LIST, "Invalid player ID"
        assert self.board[x, y] == 0, f"Space Occupied at ({x}, {y}) by {self.board[x,y]}"

        for dx, dy in self.NEIGHBORS:
            nx, ny = x+dx, y+dy 
            # check if occupied
            if self.in_bounds(nx,ny) and self.board[nx,ny] != 0:
                # check if boop square is open
                nnx, nny = nx+dx, ny+dy 
                if self.in_bounds(nnx, nny):
                    if self.board[nnx,nny] == 0:
                        self.board[nnx,nny] = self.board[nx,ny]
                        self.board[nx,ny] = 0
                else:
                    self.board[nx, ny] = 0
        self.board[x,y] = playerID
        print(self.board)
        if x:= self.check_winner():
            print(f'Player: {x} wins!')

    def check_winner(self):
        """Fast check using precomputed triplets."""
        b = self.board
        for triplet in self.TRIPLETS:
            vals = [b[x, y] for x, y in triplet]
            if vals[0] != 0 and vals.count(vals[0]) == 3:
                return vals[0]
        return 0

        
if __name__ == '__main__':
    boop = BoopGame()
    boop.make_move(1,2,-1)
    boop.make_move(1,0,1)
