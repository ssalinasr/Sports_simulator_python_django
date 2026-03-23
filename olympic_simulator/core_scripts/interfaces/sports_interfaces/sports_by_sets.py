from .sports_interface import SportsInterface
import random

class SetsSport(SportsInterface):

    def __init__(self, sport_name, sets, set_points, tiebreaker, extra_time, double_round):
        super().__init__(sport_name)
        self.sets = sets
        self.set_points = set_points
        self.tiebreaker = tiebreaker
        self.probs = []
        self.has_extra_time = extra_time
        self.has_double_round = double_round

    def get_probability_list(self):
        self.probs = [1/585, 1/475, 1/255, 1/184, 1/90, 1/60, 1/69, 1/50, 1/45, 1/34, 1/22, 1/9, 1/4]

    def get_team_probability(self, rank1, rank2, probs):
        return super().get_team_probability(rank1, rank2, probs)

    def simulate_match(self, rank1, rank2):
        if not self.has_double_round: 
            self.sport_name = self.sport_name.replace(" Masculino","").replace(" Femenino","")
            sets_1 = 0
            sets_2 = 0
            marker_1 = []
            marker_2 = []
            
            while sets_1 < self.sets and sets_2 < self.sets:
                points_1 = 0
                points_2 = 0
                while True:
                    points_1 += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                    points_2 += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))
                    if (points_1 > self.set_points or points_2 > self.set_points) and abs(points_1 - points_2) >= 2:
                        if points_1 > points_2:
                            sets_1 += 1
                            marker_1.append('⬤')
                            marker_2.append('◯')
                        else:
                            sets_2 += 1
                            marker_2.append('⬤')
                            marker_1.append('◯')
                        break
                
                if self.sport_name in ['Volleyball','Voley Playa','Badminton']:
                    if sets_1 == 2 and sets_2 == 2:
                        results = self.do_tiebreaker(sets_1, sets_2, rank1, rank2, marker_1, marker_2, self.probs)
                        print(results)
                        sets_1 = results[0]
                        sets_2 = results[1]
                        marker_1 = results[2]
                        marker_2 = results[3]
            
            return [sets_1, sets_2, marker_1, marker_2]
        else:
            globalsets_1 = 0
            globalsets_2 = 0
            self.sport_name = self.sport_name.replace(" Masculino","").replace(" Femenino","")
            sets_1 = 0
            sets_2 = 0
            marker_1 = []
            marker_2 = []
            
            while sets_1 < self.sets and sets_2 < self.sets:
                points_1 = 0
                points_2 = 0
                while True:
                    points_1 += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                    points_2 += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))
                    if (points_1 > self.set_points or points_2 > self.set_points) and abs(points_1 - points_2) >= 2:
                        if points_1 > points_2:
                            sets_1 += 1
                            marker_1.append('⬤')
                            marker_2.append('◯')
                        else:
                            sets_2 += 1
                            marker_2.append('⬤')
                            marker_1.append('◯')
                        break
                
                if self.sport_name in ['Volleyball','Voley Playa','Badminton']:
                    if sets_1 == 2 and sets_2 == 2:
                        results = self.do_tiebreaker(sets_1, sets_2, rank1, rank2, marker_1, marker_2, self.probs)
                        sets_1 = results[0]
                        sets_2 = results[1]
                        marker_1 = results[2]
                        marker_2 = results[3]

                        self.sport_name = self.sport_name.replace(" Masculino","").replace(" Femenino","")
            globalsets_1 += sets_1
            globalsets_2 += sets_2
            
            #Segunda Ronda#
            sets_1 = 0
            sets_2 = 0
            
            while sets_1 < self.sets and sets_2 < self.sets:
                points_1 = 0
                points_2 = 0
                while True:
                    points_1 += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                    points_2 += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))
                    if (points_1 > self.set_points or points_2 > self.set_points) and abs(points_1 - points_2) >= 2:
                        if points_1 > points_2:
                            sets_1 += 1
                            marker_1.append('⬤')
                            marker_2.append('◯')
                        else:
                            sets_2 += 1
                            marker_2.append('⬤')
                            marker_1.append('◯')
                        break
                
                if self.sport_name in ['Volleyball','Voley Playa','Badminton']:
                    if sets_1 == 2 and sets_2 == 2:
                        results = self.do_tiebreaker(sets_1, sets_2, rank1, rank2, marker_1, marker_2, self.probs)
                        sets_1 = results[0]
                        sets_2 = results[1]
                        marker_1 = results[2]
                        marker_2 = results[3]
            globalsets_1 += sets_1
            globalsets_2 += sets_2
            return [globalsets_1, globalsets_2, marker_1, marker_2]
            
            
            

    def generate_goal(self, probs):
        self.sport_name = self.sport_name.replace(" Masculino","").replace(" Femenino","")
        if self.sport_name != 'Tenis':
            rand = random.random()
            if rand < probs:
                return 1
            else:
                return 0
        else:
            rand = random.random()
            if rand < probs:
                return 15
            else:
                 return 0

    def do_tiebreaker(self, score_a, score_b, rank1, rank2, marker_1, marker_2, probs):
        points_1 = 0
        points_2 = 0
        results = []
        while True:
            points_1 += self.generate_goal(self.get_team_probability(rank1, rank2, probs))
            points_2 += self.generate_goal(self.get_team_probability(rank2, rank1, probs))
            if (points_1 > self.tiebreaker or points_2 > self.tiebreaker) and abs(points_1 - points_2) >= 2:
                if points_1 > points_2:
                    score_a += 1
                    marker_1.append('⬤')
                    marker_2.append('◯')
                else:
                    score_b += 1
                    marker_2.append('⬤')
                    marker_1.append('◯')
                break
        results = [score_a, score_b, marker_1, marker_2]
        return results
    