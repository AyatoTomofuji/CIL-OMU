import time
import random
from kesslergame import Scenario, KesslerGame, GraphicsType
from Controller import NewController
scenario1 = Scenario(name='Test Scenario',
                            #num_asteroids=10,
                            asteroid_states=[
                                {'position':(200, 800), 'angle':180, 'speed':500},
                                {'position':(200, 700), 'angle':180, 'speed':500},
                                {'position': (200, 600), 'angle': 180, 'speed': 500},
                                {'position': (200, 500), 'angle': 180, 'speed': 500},
                                {'position': (200, 400), 'angle': 180, 'speed': 500},
                                {'position': (200, 300), 'angle': 180, 'speed': 500},
                            ],
                            ship_states=[
                                {'position': (400, 400), 'angle': 90, 'lives': 5, 'team': 1},
                                {'position': (400, 600), 'angle': 90, 'lives':5, 'team': 2},
                            ],
                            map_size=(1000, 800),
                            time_limit=60,
                            ammo_limit_multiplier=0,
                            stop_if_no_ammo=False)




def timeout(input_data):
    # Function for testing the timing out by the simulation environment
    wait_time = random.uniform(0.02, 0.03)
    time.sleep(wait_time)

"""
class FuzzyController(ControllerBase):
    @property
    def name(self) -> str:
        return "Example Controller Name"

    def actions(self, ships: Tuple[SpaceShip], input_data: Dict[str, Tuple]) -> None:
        timeout(input_data)

        for ship in ships:
            ship.turn_rate = random.uniform(ship.turn_rate_range[0]/2.0, ship.turn_rate_range[1])
            ship.thrust = random.uniform(ship.thrust_range[0], ship.thrust_range[1])
            ship.fire_bullet = random.uniform(0.45, 1.0) < 0.5
"""


def cil_run():
    if __name__ == "__main__":
        # Available settings
        settings = {
            "frequency": 60,
            "real_time_multiplier": 2,
            "graphics_on": True,
            "sound_on": True,
            "prints": True,
            "full_dashboard": True
        }

        # Instantiate an instance of FuzzyAsteroidGame
        game = KesslerGame(settings=settings)

        scenario_ship = scenario1

        run10_hit_env_child5 = [ 16.83714325,  34.80430902, 188.32179048,  86.97881193]
        run10_hit_env_child1 = [ 13.94107016,  53.73100038, 235.7052832,  101.09256617]
        run10_hit_best = [-6.73947456,  31.06759868, 170.07489844, 110.53856904]
        base = [0, 100, 200, 90]
        run_run_run_best = [27.09657822, 104.49485255, 208.69140721,  79.7928394]
        controllers = [NewController(run_run_run_best), NewController(run_run_run_best)]

        pre = time.perf_counter()
        score, perf_data = game.run(scenario=scenario_ship, controllers=controllers)
        print('Scenario eval time: '+str(time.perf_counter()-pre))
        print(score.stop_reason)
        print('Asteroids hit: ' + str([team.asteroids_hit for team in score.teams]))
        print('Deaths: ' + str([team.deaths for team in score.teams]))
        print('Accuracy: ' + str([team.accuracy for team in score.teams]))
        print('Mean eval time: ' + str([team.mean_eval_time for team in score.teams]))

cil_run()