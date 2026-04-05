from .olympic_sport_interface import OlympicSportsInterface

class SportsByHeats(OlympicSportsInterface):

    def __init__(self, sport_name, best_res, last_res, type_mode):
        super().__init__(sport_name, best_res, last_res, type_mode)

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
        self.generate_intervals()
        interval = self.get_team_interval(rank)
        list = [self.simulate_points(interval) * num_heats]
        return [sum(list)]
    
    def generate_round_by_rounds(self, rank, num_rounds, num_scores):
        pass
        
    def select_type_game(self, rank, num_rounds, num_scores):
        return super().select_type_game(rank, num_rounds, num_scores)
