"""Events."""
from config import config
from simpy.rt import RealtimeEnvironment
class Events:
    """Real-Time Simulation."""
    def __init__(self, env) -> None:
        self.rte = RealtimeEnvironment(factor=config["speed_simu"])
        self.environment = env
        input_list = self.environment.goal
        for x,y in input_list:
            self.environment.set_objet(
                    "table",x,y
                )

    def run(self):
        self.rte.run()