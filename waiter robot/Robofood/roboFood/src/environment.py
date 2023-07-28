"""Environment."""
from threading import Thread
from board import Board
from events import Events
from robot import Robot
from statistics import Stats
class Environment:
    def __init__(self, line, col, x,y, goal) -> None:
        """Creation of the environment."""
        # Dimension of the grid
        self.line = line
        self.col = col
        self.goal=goal
        # Creation of the grid
        self.grid = {
            "table": [[False for y in range(self.line)] for x in range(self.col)],
        }
        # initial robot
        self.position_robot = {
            "x": x,
            "y": y,
        }
        ##### Stats #####
        stats = Stats(x,y)
        thread_stats = Thread(target=stats.run)
        thread_stats.daemon = True
        thread_stats.start()

        ##### GUI #####
        self.board = Board(self, stats,x, y)

        self.set_objet("robot", self.position_robot["x"], self.position_robot["y"])

        ##### Event #####
        events = Events(self)
        thread_event = Thread(target=events.run)
        thread_event.daemon = True
        thread_event.start()

        ##### Robot #####
        robot = Robot(self, stats)
        thread_robot = Thread(target=robot.run)
        thread_robot.daemon = True
        thread_robot.start()

        self.board.display()

    def set_objet(self, objet, x, y):
        """Place the object in the grid."""
        if objet != "robot":
            self.grid[objet][x][y] = True

        self.board.display_objet(x, y, objet)

    def unset_objet(self, objet, x, y):
        """Removes the object from the grid."""
        self.grid[objet][x][y] = False

        self.board.hide_objet(objet, self.position_robot["x"], self.position_robot["y"])

    def move_robot(self, dx, dy):
        """Move the robot."""
        self.board.hide_objet(
            "robot", self.position_robot["x"], self.position_robot["y"]
        )
        self.position_robot["x"] = dx
        self.position_robot["y"] = dy
        self.board.display_objet(
            self.position_robot["x"], self.position_robot["y"], "robot"
        )

    def update_stats(self):
        """Update the statistics to display."""
        self.board.update_stats()
