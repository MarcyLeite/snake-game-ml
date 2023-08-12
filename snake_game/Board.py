import pygame

pixel_size = 10
board_size = 40
default_color = (25, 25, 25)

class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = ''
        self.color = default_color
        self.smell = 0

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    
    def set_resident(self, name, color):
        self.name = name
        self.color = color

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color
    
    def get_smell(self):
        return self.smell
    
    def set_smell(self, smell):
        self.smell = smell

class Board():
    def __init__(self, surface):
        self.surface = surface
        board = []
        for x in range(board_size):
            board.append([])
            for y in range(board_size):
                board[x].append(Cell(x, y))
        
        self.board = board

    def render(self):
        board = self.board
        surface = self.surface
        for col in board:
            for cell in col:
                x = cell.get_x()
                y = cell.get_y()
                color = pygame.Color(cell.get_color())

                surface_x = (x) * pixel_size
                surface_y = (y) * pixel_size

                smell = cell.get_smell()

                if smell > 1:
                    smell = 1

                if cell.get_name() == '':
                    color = color.lerp(pygame.Color(0, 0, 255), smell)

                pygame.draw.rect(surface, color, pygame.Rect(surface_x, surface_y + 100, pixel_size - 2, pixel_size - 2))

        pygame.display.update()

    def set_cell(self, x, y, name, color):
        board = self.board
        board[x][y].set_resident(name, color)
    
    def to_state(self):
        state = []
        for col_list in self.board:
            for cell in col_list:
                name = cell.get_name()
                if name == '':
                    state.append(0)
                elif name == 'snake':
                    state.append(1)
                elif name == 'fruit':
                    state.append(2)
        return state

    def reset_smell(self):
        board = self.board
        for col_list in board:
            for cell in col_list:
                cell.set_smell(0)

    def get_resident(self, x, y):
        return self.board[x][y]

    def get_size(self):
        board = self.board
        return (len(board), len(board[0]))