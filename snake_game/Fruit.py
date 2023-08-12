import random
from Board import default_color

class FruitHandler():
    def __init__(self, board):
        self.board = board
        self.spawned = False
        self.pos = (0, 0)

    def kill(self):
        board = self.board
        fruit_location = self.fruit_location

        board.set_cell(fruit_location[0], fruit_location[1], '', default_color)
        self.spawned = False

    def get_pos(self):
        return self.pos

    def step(self):
        if self.spawned:
            return
        
        board = self.board
        board_size = board.get_size()

        filtered_coords = []

        for x in range(board_size[0]):
            for y in range(board_size[1]):
                if board.get_resident(x, y).get_name() == '':
                    filtered_coords.append((x, y))
        
        fruit_location = random.choice(filtered_coords)
        self.pos = fruit_location
        board.set_cell(fruit_location[0], fruit_location[1], 'fruit', (255, 0, 0))
        
        self.fruit_location = fruit_location
        self.spawned = True
