"""Robot."""
from copy import deepcopy
from algorithm import AStar
from config import config
from simpy.rt import RealtimeEnvironment
class Sensor:

    def __init__(self, env, robot) -> None:
        """Creation of the sensor"""
        self.environment = env
        self.robot = robot

    def observe_environment(self):
        """Retrieves environment data."""
        self.robot.gridd = deepcopy(self.environment.grid)
        self.robot.position = deepcopy(self.environment.position_robot)

class actuator:
    """Action on the environment."""
    def __init__(self, env, robot) -> None:
        """Creation of the actuator."""
        self.environment = env
        self.robot = robot

    def move(self, dx, dy):
        """Move the robot."""
        self.environment.move_robot(dx, dy)
        self.robot.perf.stats["path"] += "("+str(dy)+","+str(dx)+")"
        self.robot.perf.stats["energy_consumed"] += 1

    def deliver(self, x, y):
        """deliver an order to a table."""
        self.robot.perf.stats["energy_consumed"] += 1

        if self.environment.grid["table"][x][y]:
            self.environment.unset_objet("table", x, y)
            self.robot.perf.stats["tables_delivered"] += 1

    def stay_put(self):
        """Don't do anything."""
    def execute(self):
        """Execute the action in the list."""
        try:
            action = self.robot.actions.pop(0)

            if action[0] == "table":
                x, y = action[1]
                self.deliver(x, y)

            elif action[0] == "move":
                dx, dy = action[1]
                dx=self.robot.position["x"] + dx
                dy=self.robot.position["y"] + dy
                self.move(dx, dy)
        except IndexError:
            self.stay_put()
        finally:
            self.environment.update_stats()

        return len(self.robot.actions) > 0
class Robot:

    def __init__(self, env, stats) -> None:

        self.rte = RealtimeEnvironment(factor=config["speed_simu"])
        self.rte.process(self.robot_event())
        # Sensor(s)
        self.sensor = Sensor(env, self)
        self.algo = AStar(self)
        # actuator(s)
        self.Actuator = actuator(env, self)

        self.has_strategy = False
        self.gridd = []
        self.position = {}
        self.actions = []
        self.perf = stats

    def run(self):
        self.rte.run()
    def robot_event(self):
        """Robot mainloop."""
        iteration = 0
        refresh_rate = config["size"]["width"] + config["size"]["height"] - 1
        while True:
            yield self.rte.timeout(1)
            iteration += 1
            # Sensor
            self.sensor.observe_environment()
            # Change state
            if not (
                any(any(x) for x in self.gridd["table"])
            ):
                self.Actuator.execute()
                continue
            # choose action
            if (iteration % refresh_rate == 0) | (not self.has_strategy):
                self.algo.search()
                self.has_strategy = True
            # Perform the action
            self.has_strategy = self.Actuator.execute()

