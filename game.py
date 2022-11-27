import pyxel


class Game:
    def __init__(self):
        pyxel.init(640, 512, title="Brick Breaker", fps=60)
        self.bricks = generateBricks(pyxel.width, pyxel.height)
        self.ball = {"x": pyxel.width / 2, "y": pyxel.height - 30, "radius": 8}
        self.player = {"x": pyxel.width / 2 - 25, "y": pyxel.height - 20}
        pyxel.run(self.update, self.draw)

    def update(self):
        self.handleBoard()
        self.handleBall()

    def handleBoard(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player.update({"x": self.player["x"] + 10})
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player.update({"x": self.player["x"] - 10})

        if self.player["x"] < 0:
            self.player.update({"x": 0})
        if self.player["x"] >= pyxel.width:
            self.player.update({"x": pyxel.width - 10})

    def handleBall(self):
        movement = {"y": self.ball["y"] - 10}
        if self.ball["x"] < self.ball["radius"]:
            self.ball.update({"x": self.ball["radius"]})
        if self.ball["y"] < self.ball["radius"]:
            movement = {"y": self.ball["y"] + 10}
        if self.ball["x"] >= pyxel.width - self.ball["radius"]:
            self.ball.update({"x": pyxel.width - self.ball["radius"]})
        if self.ball["y"] >= pyxel.height - self.ball["radius"]:
            self.ball.update({"x": pyxel.width / 2, "y": pyxel.height - 30})

        self.ball.update(movement)

        for dic in self.bricks:
            if collision(
                self.ball,
                {
                    "x": dic["x"],
                    "y": dic["y"],
                    "width": dic["width"],
                    "height": dic["height"],
                },
            ):
                if dic["color"] == 11:
                    self.bricks.remove(dic)
                if dic["color"] == 12:
                    dic["color"] = 11
                if dic["color"] == 8:
                    dic["color"] = 12

    def draw(self):
        pyxel.cls(0)
        for dic in self.bricks:
            pyxel.rect(dic["x"], dic["y"], dic["width"], dic["height"], dic["color"])
        pyxel.circ(self.ball["x"], self.ball["y"], self.ball["radius"], 7)
        pyxel.rect(self.player["x"], self.player["y"], 52, 12, 4)


def generateBricks(width, height):
    brick_width = 30
    brick_height = 14
    positionBricks = [
        {
            "x": x if y % 2 == 0 else x + brick_width / 2,
            "y": y,
            "width": brick_width,
            "height": brick_height,
        }
        for y in range(int(height / 8), int(height - 2 * height / 8), brick_height + 1)
        for x in range(int(width / 8), int(width - width / 8), brick_width + 1)
    ]
    bricks = []
    for index, dic in enumerate(positionBricks):
        bricks.append(
            {**dic, "color": 12 if index % 2 == 0 else (8 if index % 3 == 0 else 11)}
        )
    return bricks


def collision(circle: dict, rectangle: dict):
    xdistance = abs(circle["x"] - rectangle["x"] - rectangle["width"] / 2)
    ydistance = abs(circle["y"] - rectangle["y"] - rectangle["height"] / 2)

    if (
        xdistance > (rectangle["width"] / 2 + circle["radius"])
        or ydistance > rectangle["height"] / 2 + circle["radius"]
    ):
        return False

    if xdistance <= (rectangle["width"] / 2) or ydistance <= rectangle["height"] / 2:
        return True

    return (xdistance - rectangle["x"] / 2) ** 2 + (
        ydistance - rectangle["height"] / 2
    ) ** 2 <= circle["radius"] ** 2


Game()
