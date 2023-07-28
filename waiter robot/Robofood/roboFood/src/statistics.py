from copy import deepcopy
from config import config
from simpy.rt import RealtimeEnvironment
class Stats:
    """Class  statistics ."""
    def __init__(self,x,y) -> None:
        """Init statistics."""
        self.rte = RealtimeEnvironment(factor=config["speed_simu"])
        self.rte.process(self.stats_event())
        self.freq = 10
        self.clean()
        self.total_stats = {
            "total_tables_delivered": 0,
            "total_energy_consumed": 0,
            "total_distance": 0,
            "path":"("+str(y)+","+str(x)+")",
        }
        self.duration = 0
        self.refresh_rate = config["size"]["width"] + config["size"]["height"] - 1
        self.old = [deepcopy(self.total_stats)]
    def clean(self):
        """Reset temporary stats."""
        self.stats = {
            "tables_delivered": 0,
            "energy_consumed": 0,
            "path":"",
        }
    def archiver(self):
        """Archive data."""
        tmp = deepcopy(self.total_stats)
        self.old.append(tmp)

        self.total_stats = {
            "total_tables_delivered": 0,
            "total_energy_consumed": 0,
            "total_distance": 0,
            "path":"",
            }
        self.duration = 0

    def stats_event(self):
        """Stats mainloop."""
        while True:
            yield self.rte.timeout(self.freq)
            self.duration += self.freq  # self.rte.now

            tmp = deepcopy(self.stats)
            self.total_stats["total_tables_delivered"] += tmp["tables_delivered"]
            self.total_stats["total_energy_consumed"] += tmp["energy_consumed"]

            self.total_stats["total_distance"] += (
                tmp["energy_consumed"] - tmp["tables_delivered"]
            )
            self.total_stats["path"] += tmp["path"]
            self.clean()

    def run(self):
        """Start the simulation."""
        self.rte.run()
