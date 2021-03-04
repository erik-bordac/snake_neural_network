 
class Snake():
    def __init__(self):
        self.body = [{"x": 5, "y":5}, {"x": 4, "y":5}, {"x": 3, "y":5},]
        self.direction = "right"
        self.ate = False
        self.moves_left = 400

    def move(self):
        """
        Moves the snake in self.direction
        If snake ate apple in this iteration, prevents removing last block
        return None
        """
        if self.direction == "right":
            head = self.body[0]
            self.body.insert(0, {"x": head["x"]+1, "y": head["y"]})
        elif self.direction == "up":
            head = self.body[0]
            self.body.insert(0, {"x": head["x"], "y": head["y"]-1})
        elif self.direction == "left":
            head = self.body[0]
            self.body.insert(0, {"x": head["x"]-1, "y": head["y"]})
        elif self.direction == "down":
            head = self.body[0]
            self.body.insert(0, {"x": head["x"], "y": head["y"]+1})

        if not self.ate:
            del self.body[-1]
        self.ate = False
        self.moves_left -= 1

