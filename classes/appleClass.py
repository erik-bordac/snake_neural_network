
import random

class Apple():
    def __init__(self, WIDTH, HEIGHT, CELL_WIDTH, snake_body):
        self.coords = self.create_apple(WIDTH, HEIGHT, CELL_WIDTH, snake_body)
    
    def create_apple(self, WIDTH, HEIGHT, CELL_WIDTH, snake_body):
        """
        Generates dictionary containing valid coordination, where the apple can spawn
        return {"x": x, "y": y}
        """
        possible_coords = []
        for i in range(int(WIDTH / CELL_WIDTH)):
            for j in range(int(HEIGHT / CELL_WIDTH)):
                coord = {"x": i, "y": j}

                if coord not in snake_body:
                    possible_coords.append(coord)
                

        return random.choice(possible_coords)
