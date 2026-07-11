from abc import ABC, abstractmethod
import random

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
        prob_value = 0

        if dif > 0:
            prob_value = probs[max(middle - dif, 0):middle + 1][::-1][-1]
        elif dif < 0:
            prob_value = probs[middle:min(middle - dif + 1, len(probs))][-1]
        else:
            prob_value = probs[middle]

        moral = random.uniform(0.9,1.2) #Moral del equipo
        local = random.uniform(0.95,1.15) #Modificador de Localía
        fatigue = random.uniform(0.8,1) #Indicador de fatiga
        weather = random.uniform(0.85,1) #Clima en el encuentro
        prob_value = prob_value * moral * local * fatigue * weather
        return prob_value

    @abstractmethod
    def simulate_match(self, rank1, rank2, probs):
        pass

    @abstractmethod
    def generate_goal(self, probs):
        pass

    @abstractmethod
    def do_tiebreaker(self, score_a, score_b, rank1, rank2, probs):
        pass