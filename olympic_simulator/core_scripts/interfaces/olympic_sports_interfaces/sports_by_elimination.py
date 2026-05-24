from .olympic_sport_interface import OlympicSportsInterface
import random, math

class SportsByElimination(OlympicSportsInterface):

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

    def get_fail_chance(self, rank, base_fail):
        return rank * base_fail

    def generate_round_by_elimination(self, rank, num_rounds, num_scores):
        self.generate_intervals()
        intervals = self.get_team_interval(rank)
        alive = True
        base_fail = 0.1
        current_score = self.last_res
        attempts = []
        num_tries = 1
        if self.category_name in ['Atletismo','Munecos']:
            current_score = self.last_res
            while alive:    
                print(num_tries, end=' ')
                marks = ''  
                rand = random.random()
                if rand < self.get_fail_chance(rank, base_fail):
                    num_tries += 1
                    marks += 'X'
                else:
                    base_fail += .05
                    marks += 'O'
                    attempts.append((round(current_score,2), marks))
                    current_score += 0.02
                    num_tries = 1
                
                if num_tries == 3:
                    alive = False
                    attempts.append((round(current_score,2), marks))
            print()
                   
        elif self.category_name == 'Halterofilia':
            self.generate_intervals()
            current_score = intervals[1]
            while alive:    
                print(num_tries, end=' ')
                marks = ''  
                rand = random.random()
                if rand < self.get_fail_chance(rank, base_fail):
                    num_tries += 1
                    marks += 'X'
                else:
                    base_fail += .05
                    marks += 'O'
                    attempts.append((math.floor(round(current_score,2)), marks))
                    current_score += random.randint(2,10)
                    num_tries += 1
                
                if num_tries == 3:
                    alive = False
                    attempts.append((math.floor(round(current_score,2)), marks))
            print()
            pass
        if len(attempts) > 1:
            return [attempts, math.floor(round(current_score,2))]
        else:
            return [attempts, 0]
    
    def generate_round_by_rounds(self, rank, num_rounds, num_scores):
        pass

        
    def select_type_game(self, rank, num_rounds, num_scores):
        return super().select_type_game(rank, num_rounds, num_scores)
