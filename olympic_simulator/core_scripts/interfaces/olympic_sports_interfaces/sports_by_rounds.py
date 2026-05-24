from .olympic_sport_interface import OlympicSportsInterface
import random

class SportsByRounds(OlympicSportsInterface):

    def __init__(self, sport_name, best_res, last_res, type_mode, category_name):
        super().__init__(sport_name, best_res, last_res, type_mode, category_name)

    def get_probability_list(self, rank):
        super().get_probability_list(rank)

    def generate_intervals(self):
        super().generate_intervals()
        
    def get_team_interval(self, rank):
        return super().get_team_interval(rank)

    def simulate_points(self, interval):
        return super().simulate_points(interval)

    def generate_round_individual(self, rank):
        pass
    
    def generate_round_by_heats(self, rank, num_heats):
        pass

    def get_fail_chance(self, rank):
        return rank * 0.1


    def generate_round_by_rounds(self, rank, num_rounds, num_scores):
        self.generate_intervals()
        interval = self.get_team_interval(rank)
        results = []
        for _ in range(num_rounds):
            round_score = self.simulate_points(interval)
            rand = random.random()
            if rand < self.get_fail_chance(rank):
                results.append(0.00)
            else:
                results.append(round(round_score,2))
        return [results, round(max(results),2)]
        
    def generate_round_by_elimination(self, rank, num_rounds, num_scores):
        pass
    
    def select_type_game(self, rank, num_rounds, num_scores):
        return super().select_type_game(rank, num_rounds, num_scores)
