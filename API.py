
import numpy as np

def get_state(snake, apple, game):
        """
        return binary array
        """
        ####### 0 - not in danger // not left/right/.. #######
        ####### 1 - in danger // apple is left/right.. #######
        state = []
        
        ####### --------snake danger in moving direction----------- ############
        # moving right
        if snake.direction == "right":
            next_pos = {"x": snake.body[0].get("x") + 1, "y": snake.body[0]["y"]}
            state.append(next_pos in snake.body or next_pos["x"] >= game.WIDTH / game.CELL_WIDTH)
        
        # moving left
        elif snake.direction == "left":
            next_pos = {"x": snake.body[0].get("x") - 1, "y": snake.body[0]["y"]}
            state.append(next_pos in snake.body or next_pos["x"] < 0)
        
        # moving up
        elif snake.direction == "up":
            next_pos = {"x": snake.body[0]["x"], "y": snake.body[0].get("y") - 1}
            state.append(next_pos in snake.body or next_pos["y"] < 0)
        
        # moving down
        elif snake.direction == "down":
            next_pos = {"x": snake.body[0]["x"], "y": snake.body[0].get("y") + 1}
            state.append(next_pos in snake.body or next_pos["y"] >= game.HEIGHT / game.CELL_WIDTH)
        
        ####### --------snake danger left --------- ###########
        # moving right
        if snake.direction == "right":
            tile = {"x": snake.body[0]["x"], "y": snake.body[0].get("y") - 1}
            state.append(tile in snake.body or tile["y"] < 0)
        
        # moving up
        elif snake.direction == "up":
            tile = {"x": snake.body[0].get("x") - 1, "y": snake.body[0]["y"]}
            state.append(tile in snake.body or tile["x"] < 0)

        # moving left
        elif snake.direction == "left":
            tile = {"x": snake.body[0]["x"], "y": snake.body[0].get("y") + 1}
            state.append(tile in snake.body or tile["y"] >= game.HEIGHT / game.CELL_WIDTH)
        
        # moving down
        elif snake.direction == "down":
            tile = {"x": snake.body[0].get("x") + 1, "y": snake.body[0]["y"]}
            state.append(tile in snake.body or tile["x"] >= game.WIDTH / game.CELL_WIDTH)
        
        ####### --------snake danger right --------- ###########
        # moving right
        if snake.direction == "right":
            tile = {"x": snake.body[0]["x"], "y": snake.body[0].get("y") + 1}
            state.append(tile in snake.body or tile["y"] >= game.HEIGHT / game.CELL_WIDTH)
        
        # moving up
        elif snake.direction == "up":
            tile = {"x": snake.body[0].get("x") + 1, "y": snake.body[0]["y"]}
            state.append(tile in snake.body or tile["x"] >= game.WIDTH / game.CELL_WIDTH)

        # moving left
        elif snake.direction == "left":
            tile = {"x": snake.body[0]["x"], "y": snake.body[0].get("y") - 1}
            state.append(tile in snake.body or tile["y"] < 0)
        
        # moving down
        elif snake.direction == "down":
            tile = {"x": snake.body[0].get("x") - 1, "y": snake.body[0]["y"]}
            state.append(tile in snake.body or tile["x"] < 0)

        state.extend([
            snake.direction == "right",
            snake.direction == "up",
            snake.direction == "left",
            snake.direction == "down",
            apple.coords["x"] > snake.body[0]["x"],  # apple right
            apple.coords["x"] < snake.body[0]["x"],  # apple left
            apple.coords["y"] > snake.body[0]["y"],  # apple down
            apple.coords["y"] < snake.body[0]["y"],  # apple up
        ])
        
        # convert True/False to 1/0
        for i in range(len(state)):
            state[i] = int(state[i])

        return np.asarray(state)