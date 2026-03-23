from .sports_interface import SportsInterface
import random

class SpecialSetsSport(SportsInterface):

    def __init__(self, sport_name, sets, extra_time, double_round):
        super().__init__(sport_name)
        self.sets = sets
        self.probs = []
        self.has_extra_time = extra_time
        self.has_double_round = double_round

    def get_probability_list(self):
        self.probs = [1/585, 1/475, 1/255, 1/184, 1/90, 1/60, 1/69, 1/50, 1/45, 1/34, 1/22, 1/9, 1/4]

    def get_team_probability(self, rank1, rank2, probs):
        return super().get_team_probability(rank1, rank2, probs)

    def simulate_match(self, rank1, rank2):
        sets_1 = 0
        sets_2 = 0
        marker_1 = []
        marker_2 = []
        num_sets = 0

        while sets_1 < self.sets and sets_2 < self.sets:
            puntos_a = sum(self.generate_goal(rank1) for _ in range(3))
            puntos_b = sum(self.generate_goal(rank2) for _ in range(3))
            num_sets += 1
            if puntos_a > puntos_b:
                sets_1 += 2
                marker_1.append('⬤')
                marker_2.append('◯')
            elif puntos_b > puntos_a:
                sets_2 += 2
                marker_2.append('⬤')
                marker_1.append('◯')
            else:
                sets_1 += 1
                sets_2 += 1
                marker_1.append('//')
                marker_2.append('//')
            

            if sets_1 == 5 and sets_2 == 5:
                flecha_a = self.generate_goal(rank1)
                flecha_b = self.generate_goal(rank2)

                if flecha_a > flecha_b:
                    sets_1 += 1
                    marker_1.append('⬤')
                    marker_2.append('◯')
                    
                elif flecha_b > flecha_a:
                    sets_2 += 1
                    marker_2.append('⬤')
                    marker_1.append('◯')
                else:
                    while flecha_a == flecha_b:
                        flecha_a = self.generate_goal(rank1)
                        flecha_b = self.generate_goal(rank2)

                        if flecha_a > flecha_b:
                            sets_1 += 1
                            marker_1.append('||')
                            marker_2.append('|')           
                        else:
                            sets_2 += 1
                            marker_2.append('||')
                            marker_1.append('|')
                        
                if num_sets == 5:
                    break
        return [sets_1, sets_2, marker_1, marker_2]              

    def generate_goal(self, rank_team):
        if rank_team == 1:
            return random.randint(8,10)
        elif rank_team >= 2 or rank_team <= 3:
            return random.randint(6,10)
        elif rank_team >= 4 or rank_team <= 6:
            return random.randint(4,8)
        else:
            return random.randint(1,6)


    def do_tiebreaker(self, score_a, score_b, rank1, rank2, marker_1, marker_2, probs):
        pass
    