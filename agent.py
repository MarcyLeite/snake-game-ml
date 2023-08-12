import sys, os
import random, json

sys.path.insert(0, os.path.abspath('./snake_game'))

from snake_game.main import run_game

LEARNING_RATE = 0.1
DISCOUNT_RATE = 0.95

# Tabela da verdade

def generate_q_table():
    q_table = []
    for i1 in range(3):
        for i2 in range(3):
            for i3 in range(3):
                for i4 in range(2):
                    for i5 in range(2):
                        for i6 in range(2):
                            for i7 in range(2):
                                    for i8 in range(4):
                                        state = [[i1, i2, i3, i4, i5, i6, i7, i8 + 1]]
                                        options = []
                                        for i10 in [-1, 0, 1]:
                                            options.append([i10, random.randint(1, 1)])
                                        state.append(options)
                                        q_table.append(state)
    return q_table
    
a = 0

loop_count = 0

if not os.path.exists(os.path.abspath('./data.json')):
    file = open(os.path.abspath('./data.json'), 'w+')
    save_data = {
        'q_table': generate_q_table(),
        'steps': 0
    }
    json_data = json.dumps(save_data, indent=4)
    file.write(json_data)
    file.close()

file = open(os.path.abspath('./data.json'), 'r')
raw = file.read()
file.close()

dict_data = json.loads(raw)
q_table = dict_data['q_table']
steps = dict_data['steps']

def choose_action(state, steps):

    global q_table

    if steps % 10000 == 0:
        file = open(os.path.abspath('./data.json'), 'w+')
        save_data = {
            'q_table': q_table,
            'steps': steps
        }
        json_data = json.dumps(save_data, indent=4)
        file.write(json_data)
        file.close()

    for i in range(len(q_table)):
        if q_table[i][0] == state:
            print(q_table[i])
            better_reward = max(q_table[i][1], key= lambda x: x[1])
            index = q_table[i][1].index(better_reward)
            direction = q_table[i][0][7]
            new_direction = direction + better_reward[0]

            if new_direction == 5:
                new_direction = 1
            if new_direction == 0:
                new_direction = 4

            def controller(snake):
                snake.set_direction(new_direction)
                
            def update_q(reward, new_state):
                old_value = q_table[i][1][index][1]
                predict_reward = 0
                for j in range(len(q_table)):
                    if q_table[j][0] == new_state:
                        predict_reward = max(q_table[j][1], key= lambda x: x[1])[1]
                        break

                new_value = (1 - LEARNING_RATE)*old_value + LEARNING_RATE*(reward + DISCOUNT_RATE*(predict_reward))
                q_table[i][1][index][1] = new_value
                
            
            return [controller, update_q]

run_game(choose_action, steps)