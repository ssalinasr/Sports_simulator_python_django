from abc import ABC, abstractmethod
from .games_interface import GamesInterface
import random

class MarioKartInterface(GamesInterface):


    def __init__(self, game_name, game_type, time, lives):
        super().__init__(game_name, game_type)
        self.time = time
        self.lives = lives

    def get_player_probability(self):
        return random.random()

    def generate_point(self, prob):
        if prob < 0.05:
            return 1
        else:
            return 0
        
    def simulate_game(self, type_game):
        return super().simulate_game(type_game)

    def simulate_game_by_time(self):
        pass

    def simulate_game_by_lives(self):
        pass

    def simulate_game_by_rev_lives(self):
        curr_lives_a = self.lives
        curr_lives_b = self.lives

        while curr_lives_a > 0 and curr_lives_b > 0:           
            point_a = self.get_player_probability()
            point_b = self.get_player_probability()

            if point_a < 0.33:
                curr_lives_a -= 1

            if point_b < 0.33:
                curr_lives_b -= 1

            while curr_lives_a == curr_lives_b:
                curr_lives_a += self.generate_point(self.get_player_probability())
                curr_lives_b += self.generate_point(self.get_player_probability())
                if curr_lives_a != curr_lives_b:
                    break
            
        return [curr_lives_a, curr_lives_b]

    def simulate_game_by_cumulative(self):
        pass