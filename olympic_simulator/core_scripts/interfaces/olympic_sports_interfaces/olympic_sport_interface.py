from abc import ABC, abstractmethod
import random

class OlympicSportsInterface(ABC):

    def __init__(self, sport_name, best_res, last_res, type_mode):
        self.sport_name = sport_name
        self.best_res = best_res
        self.last_res = last_res
        self.type_mode = type_mode
        self.intervals_list = []
        self.probs = []

    @abstractmethod
    def get_probability_list(self, rank):
        if rank == 1:
            self.probs = [1.0,0.25,0.1,0.013,0.004,0.0004,0.00001]
        elif rank == 2:
            self.probs = [0.25,1.0,0.25,0.1,0.013,0.004,0.0004]
        elif rank == 3:
            self.probs = [0.1,0.25,1.0,0.25,0.1,0.013,0.004]
        elif rank == 4:
            self.probs = [0.013,0.1,0.25,1.0,0.25,0.1,0.013]
        elif rank == 5:
            self.probs = [0.004,0.013,0.1,0.25,1.0,0.25,0.1]
        elif rank == 6:
            self.probs = [0.0004,0.004,0.013,0.1,0.25,1.0,0.25]
        elif rank == 7:
            self.probs = [0.00001,0.0004,0.004,0.013,0.1,0.25,1.0]
        else:
            self.probs = [1.0,0.25,0.1,0.013,0.004,0.0004,0.00001]

    @abstractmethod
    def generate_intervals(self):
        self.intervals_list.clear()
        difference = (self.best_res - self.last_res) / 7
        first_value = self.best_res
        for _ in range(7):
            interval = (first_value, first_value - difference)
            first_value = interval[1]
            self.intervals_list.append(interval)
        

    @abstractmethod
    def get_team_interval(self, rank):
        rand = random.random()
        self.get_probability_list(rank)

        order_map = {
            1: [1,2,3,4,5,6,0],
            2: [0,2,3,4,5,6,1],
            3: [0,1,3,4,5,6,2],
            4: [0,1,2,4,5,6,3],
            5: [0,1,2,3,5,6,4],
            6: [0,1,2,3,4,6,5],
            7: [0,1,2,3,4,5,6],
        }

        for i in order_map.get(rank, []):
            if rand <= self.probs[i]:
                return self.intervals_list[i]
            

    @abstractmethod
    def simulate_points(self, interval):
        return round((random.random() * (interval[0] - interval[1]) + interval[1]), 3)

    @abstractmethod
    def generate_round_individual(self, rank):
        pass

    @abstractmethod
    def generate_round_by_heats(self, rank, num_heats):
        pass

    @abstractmethod
    def generate_round_by_rounds(self, rank, num_rounds, num_scores):
        pass

    @abstractmethod
    def select_type_game(self, rank, num_rounds, num_scores):
        if self.type_mode == 'I':
            return self.generate_round_individual(rank)
        if self.type_mode == 'H':
            return self.generate_round_by_heats(rank, num_rounds)
        if self.type_mode == 'R':
            return self.generate_round_by_rounds(rank, num_rounds, num_scores)

        
