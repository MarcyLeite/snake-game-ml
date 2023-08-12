from Board import default_color

initial_size = 3

class Snake():
    def __init__(self, board, fruit_handler):
        self.dead = False
        self.grow = False
        self.color = (177, 255, 177)
        self.fruit_handler = fruit_handler

        self.board = board
        body = [(int(board.get_size()[0]/2), int(board.get_size()[1]/2))]
        
        for _ in range(initial_size - 1):
            body.append((body[-1][0]-1, body[-1][1]))

        self.body = body
        self.old_body = body

        self.direction = 2

        self.draw()
    
    def new_body(self):
        direction = self.direction
        body = self.body.copy()
        head = body[0]

        if direction == 1:
            body.insert(0, (head[0], head[1] + 1))
        elif direction == 2:
            body.insert(0, (head[0] + 1, head[1]))
        elif direction == 3:
            body.insert(0, (head[0], head[1] -1))
        elif direction == 4:
            body.insert(0, (head[0] - 1, head[1]))

        if not self.grow:
            body.pop()
        
        self.grow = False

        return body

    def check_death(self, next_body):
        board = self.board
        board_size = self.board.get_size()
        head = next_body[0]

        if head[0] < 0 or head[0] >= board_size[0] or head[1] < 0 or head[1] >= board_size[1]:
            self.dead = True
            return

        for i, cell in enumerate(next_body):
            if i == 0:
                continue
            if head[0] == cell[0] and head[1] == cell[1]:
                self.dead = True
                return
        
        head_cell = board.get_resident(head[0], head[1])
        head_cell.set_smell(head_cell.get_smell() + 0.1)
        if head_cell.get_smell() > 1:
            self.dead = True
            return

    def set_direction(self, new_direction):
        direction = self.direction

        if direction % 2 == new_direction % 2:
            return

        self.direction = new_direction

    def get_direction(self):
        return self.direction

    def draw(self):
        board = self.board

        for cell in self.old_body:
            board.set_cell(cell[0], cell[1], '', default_color)

        for cell in self.body:
            board.set_cell(cell[0], cell[1], 'snake', self.color)

        board.set_cell(self.body[0][0], self.body[0][1], 'head', (0, 255, 0))

    def get_state(self):
        body = self.body
        direction = self.direction
        board = self.board
        board_size = board.get_size()
        head = body[0]
        danger_prox = [0] * 3

        if direction == 1:
            if head[1] + 1 >= board_size[1]:
                danger_prox[1] = 2
            elif board.get_resident(head[0], head[1] + 1).get_name() == 'snake':
                danger_prox[1] = 1
            if head[0] - 1 < 0:
                danger_prox[0] = 2
            elif board.get_resident(head[0] - 1, head[1]).get_name() == 'snake':
                danger_prox[0] = 1
            if head[0] + 1 >= board_size[0]:
                danger_prox[2] = 2
            elif board.get_resident(head[0] + 1, head[1]).get_name() == 'snake':
                danger_prox[2] = 1
        elif direction == 2:
            if head[0] + 1 >= board_size[0]:
                danger_prox[1] = 2
            elif board.get_resident(head[0] + 1, head[1]).get_name() == 'snake':
                danger_prox[1] = 1
            if head[1] + 1 >= board_size[1]:
                danger_prox[0] = 2
            elif board.get_resident(head[0], head[1] + 1).get_name() == 'snake':
                danger_prox[0] = 1
            if head[1] - 1 < 0:
                danger_prox[2] = 2
            elif board.get_resident(head[0], head[1] - 1).get_name() == 'snake':
                danger_prox[2] = 1
        elif direction == 3:
            if head[1] - 1 < 0:
                danger_prox[1] = 2
            elif board.get_resident(head[0], head[1] - 1).get_name() == 'snake':
                danger_prox[1] = 1
            if head[0] + 1 >= board_size[0]:
                danger_prox[0] = 2
            elif board.get_resident(head[0] + 1, head[1]).get_name() == 'snake':
                danger_prox[0] = 1
            if head[0] - 1 < 0:
                danger_prox[2] = 2
            elif board.get_resident(head[0] - 1, head[1]).get_name() == 'snake':
                danger_prox[2] = 1
        elif direction == 4:
            if head[0] - 1 < 0:
                danger_prox[1] = 2
            elif board.get_resident(head[0] - 1, head[1]).get_name() == 'snake':
                danger_prox[1] = 1
            if head[1] - 1 < 0:
                danger_prox[0] = 2
            elif board.get_resident(head[0], head[1] - 1).get_name() == 'snake':
                danger_prox[0] = 1
            if head[1] + 1 >= board_size[1]:
                danger_prox[2] = 2
            elif board.get_resident(head[0], head[1] + 1).get_name() == 'snake':
                danger_prox[2] = 1

        fruit_pos = self.fruit_handler.get_pos()
        fruit_dir = [0] * 4

        if head[0] > fruit_pos[0]:
            fruit_dir[0] = 1
        if head[0] < fruit_pos[0]:
            fruit_dir[1] = 1
        if head[1] > fruit_pos[1]:
            fruit_dir[2] = 1
        if head[1] < fruit_pos[1]:
            fruit_dir[3] = 1

        return [*danger_prox, *fruit_dir, self.direction]

    def get_fruit_distance(self, body):
        fruit_pos = self.fruit_handler.get_pos()
        head = body[0]
        x_distance = head[0] - fruit_pos[0]
        y_distance = head[1] - fruit_pos[1]
        
        return abs(x_distance) + abs(y_distance)

    def step(self):
        self.old_body = self.body
        board = self.board
        
        next_body = self.new_body()
        self.check_death(next_body)

        head = next_body[0]

        reward = 0

        if self.dead:
            self.color = (255, 0, 0)
            reward += -10
        else:
            if board.get_resident(head[0], head[1]).get_name() == 'fruit':
                reward += 10
                board.reset_smell()
                self.fruit_handler.kill()
                self.grow = True

            self.body = next_body

        self.draw()
        return reward