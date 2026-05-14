from .sports_interface import SportsInterface
import random

class TimedPointsSport(SportsInterface):

    def __init__(self, sport_name, sets, set_points, extra_time, double_round):
        super().__init__(sport_name)
        self.sets = sets
        self.set_points = set_points
        self.probs = []
        self.has_extra_time = extra_time
        self.has_double_round = double_round

    def get_probability_list(self):
        self.probs = [1/292, 1/237, 1/123, 1/92, 1/46, 1/35, 1/30, 1/25, 1/23, 1/17, 1/11, 1/5, 1/2]

    def get_team_probability(self, rank1, rank2, probs):
        return super().get_team_probability(rank1, rank2, probs)

    def simulate_match(self, rank1, rank2):
        globalsets_1 = 0
        globalsets_2 = 0

        if not self.has_double_round:
            sets_1 = 0
            sets_2 = 0
            marker_1 = []
            marker_2 = []
            while sets_1 < self.sets and sets_2 < self.sets:
                puntos_a = 0
                puntos_b = 0
                while True:
                    puntos_a += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                    puntos_b += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))

                    if puntos_a == 14 and puntos_b == 14:
                        choicer = random.randint(0,1)
                        if choicer == 0:
                            puntos_a += 1

                        elif choicer == 1:
                            puntos_b += 1
                        
                    if (puntos_a > self.set_points or puntos_b > self.set_points):
                        if puntos_a > puntos_b:
                            sets_1 += 1
                            marker_1.append('⬤')
                            marker_2.append('◯')
                        else:
                            sets_2 += 1
                            marker_2.append('⬤')
                            marker_1.append('◯')
                        break
                
            return [sets_1, sets_2, marker_1, marker_2]
        else:
            #Primera Ronda
            sets_1 = 0
            sets_2 = 0
            marker_1 = []
            marker_2 = []
            while sets_1 < self.sets and sets_2 < self.sets:
                puntos_a = 0
                puntos_b = 0
                while True:
                    puntos_a += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                    puntos_b += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))

                    if puntos_a == 14 and puntos_b == 14:
                        choicer = random.randint(0,1)
                        if choicer == 0:
                            puntos_a += 1

                        elif choicer == 1:
                            puntos_b += 1
            
                        
                    if (puntos_a > self.set_points or puntos_b > self.set_points):
                        if puntos_a > puntos_b:
                            sets_1 += 1
                            marker_1.append('⬤')
                            marker_2.append('◯')
                        else:
                            sets_2 += 1
                            marker_2.append('⬤')
                            marker_1.append('◯')
                        break

            globalsets_1 += sets_1
            globalsets_2 += sets_2
            #Segunda Ronda
            sets_1 = 0
            sets_2 = 0
            while sets_1 < self.sets and sets_2 < self.sets:
                puntos_a = 0
                puntos_b = 0
                while True:
                    puntos_a += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                    puntos_b += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))

                    if puntos_a == 14 and puntos_b == 14:
                        choicer = random.randint(0,1)
                        if choicer == 0:
                            puntos_a += 1

                        elif choicer == 1:
                            puntos_b += 1
                        
                    if (puntos_a > self.set_points or puntos_b > self.set_points):
                        if puntos_a > puntos_b:
                            sets_1 += 1
                            marker_1.append('⬤')
                            marker_2.append('◯')
                        else:
                            sets_2 += 1
                            marker_2.append('⬤')
                            marker_1.append('◯')
                        break
            
            globalsets_1 += sets_1
            globalsets_2 += sets_2
            return [globalsets_1, globalsets_2, marker_1, marker_2]

    def generate_goal(self, probs):
        rand = random.random()
        if rand < probs:
            return 1
        else:
            return 0


    def do_tiebreaker(self, score_a, score_b, rank1, rank2, marker_1, marker_2, probs):
        pass
    