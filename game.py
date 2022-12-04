from random import choice
import pyxel


class Player:
    def __init__(self):
        self.x = pyxel.width / 2 - 40
        self.y = pyxel.height - 20
        self.width = 80
        self.height = 10
        self.color = pyxel.COLOR_GRAY

    def update(self):
        self.control()
        self.bound()

    def control(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 10
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 10

    def bound(self):
        if self.x < 0:
            self.x = 0
        if self.x >= pyxel.width - self.width:
            self.x = pyxel.width - self.width

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)


class Bricks:
    def __init__(self):
        self.width = 30
        self.height = 14
        self.layout = self.generateBricks()

    def generateBricks(self) -> list:
        bricks = []
        for y in range(60, 380, self.height + 1):
            for x in range(60, 550, self.width + 1):
                bricks.append(
                    {
                        "x": x if y % 2 == 0 else x + self.width / 2,
                        "y": y,
                        "color": self.colorBrick(x),
                    }
                )
        return bricks

    def colorBrick(self, n) -> int:
        if n % 2 == 0:
            return pyxel.COLOR_CYAN
        elif n % 3 == 0:
            return pyxel.COLOR_RED
        else:
            return pyxel.COLOR_LIME

    def draw(self):
        for dic in self.layout:
            pyxel.rect(dic["x"], dic["y"], self.width, self.height, dic["color"])


class Ball:
    def __init__(self):
        self.x = pyxel.width / 2
        self.y = pyxel.height - 30
        self.radius = 8
        self.trajectory = {"x": choice([-1, 1]), "y": -1}
        self.speed = 2
        self.color = pyxel.COLOR_WHITE

    def update(self):
        self.wallCollision()
        self.x += self.trajectory["x"] * self.speed
        self.y += self.trajectory["y"] * self.speed

    def wallCollision(self):
        if self.x < self.radius or self.x >= pyxel.width - self.radius:
            self.trajectory["x"] = -self.trajectory["x"]
        if self.y < self.radius:
            self.trajectory["y"] = -self.trajectory["y"]

    def collision(self, x, y, width, height):
        """detects collision between a circle and a rectangle"""
        distance = {
            "x": abs(self.x - x - width / 2),
            "y": abs(self.y - y - height / 2),
        }

        distance["corner"] = (distance["x"] - width / 2) ** 2 + (
            distance["y"] - height / 2
        ) ** 2

        if not (
            distance["x"] > width / 2 + self.radius
            or distance["y"] > height / 2 + self.radius
        ):
            if distance["x"] <= width / 2:
                self.trajectory["y"] = -self.trajectory["y"]
                return True
            if distance["y"] <= height / 2:
                self.trajectory["x"] = -self.trajectory["x"]
                return True

        if distance["corner"] <= self.radius**2:
            self.trajectory["x"] = -self.trajectory["x"]
            self.trajectory["y"] = -self.trajectory["y"]
            return True

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)


class Game:
    def __init__(self):
        pyxel.init(640, 512, title="Brick Breaker", fps=60)
        self.start = False
        self.player = Player()
        self.bricks = Bricks()
        self.ball = Ball()
        pyxel.sound(0).set("a1", "t", "7742", "v", 8)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.start = True
        if self.start == True:
            self.player.update()
            self.ball.update()
            self.ball.speed = round(2 + (352 - len(self.bricks.layout)) / 352 * 3, 1)
            self.handleCollisions()
            self.detectWin()
            self.detectGameOver()

    def handleCollisions(self):
        self.ball.collision(
            self.player.x, self.player.y, self.player.width, self.player.height
        )
        for dic in self.bricks.layout:
            if self.ball.collision(
                dic["x"], dic["y"], self.bricks.width, self.bricks.height
            ):
                pyxel.play(0, 0)
                if dic["color"] == pyxel.COLOR_LIME:
                    self.bricks.layout.remove(dic)
                if dic["color"] == pyxel.COLOR_CYAN:
                    dic["color"] = pyxel.COLOR_LIME
                if dic["color"] == pyxel.COLOR_RED:
                    dic["color"] = pyxel.COLOR_CYAN

    def detectWin(self):
        if len(self.bricks.layout) == 0:
            pyxel.text(10, 10, "You Won!", 7)
            pyxel.quit()

    def detectGameOver(self):
        if self.ball.y >= pyxel.height - self.ball.radius:
            # self.ball.trajectory["y"] = -self.ball.trajectory["y"]
            self.start = False
            self.bricks.layout = self.bricks.generateBricks()
            self.ball.x = pyxel.width / 2
            self.ball.y = pyxel.height - 30
            self.ball.trajectory = {"x": choice([-1, 1]), "y": -1}
            self.player.x = pyxel.width / 2 - 40
            self.player.y = pyxel.height - 20

    def draw(self):
        pyxel.cls(0)
        self.player.draw()
        self.bricks.draw()
        self.ball.draw()


Game()
