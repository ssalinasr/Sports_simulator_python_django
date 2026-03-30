from abc import ABC, abstractmethod

class SportsInterface(ABC):

    def __init__(self, sport_name):
        self.sport_name = sport_name
    @abstractmethod
    def get_probability_list(self):
        pass

    @abstractmethod
    def get_team_probability(self, rank1, rank2, probs):
        dif = rank1 - rank2
        middle = len(probs)//2

        if dif > 0:
            return probs[max(middle - dif, 0):middle + 1][::-1][-1]
        elif dif < 0:
            return probs[middle:min(middle - dif + 1, len(probs))][-1]
        else:
            return probs[middle]

    @abstractmethod
    def simulate_points(self, rank1, rank2, probs):
        pass

    @abstractmethod
    def generate_round(self, probs):
        pass
