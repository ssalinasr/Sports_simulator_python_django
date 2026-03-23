from abc import ABC, abstractmethod
from .games_interface import GamesInterface
import random

class GoldeneyeInterface(GamesInterface):


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
        score_a = 0
        score_b = 0
        for _ in range(self.time*60):
            score_a += self.generate_point(self.get_player_probability())
            score_b += self.generate_point(self.get_player_probability())

        while score_a == score_b:
            score_a += self.generate_point(self.get_player_probability())
            score_b += self.generate_point(self.get_player_probability())
            if score_a != score_b:
                break
        return [score_a, score_b]

    def simulate_game_by_lives(self):
        score_a = 0
        score_b = 0

        while score_a < self.lives and score_b < self.lives:
            score_a += self.generate_point(self.get_player_probability())
            score_b += self.generate_point(self.get_player_probability())                        
        
        while score_a == score_b:
            score_a += self.generate_point(self.get_player_probability())
            score_b += self.generate_point(self.get_player_probability())
            if score_a != score_b:
                break

        return [score_a, score_b]

    def simulate_game_by_rev_lives(self):
        score_a = 0
        score_b = 0
        curr_lives_a = self.lives
        curr_lives_b = self.lives

        while curr_lives_a > 0 and curr_lives_b > 0:           
            point_a = self.get_player_probability()
            point_b = self.get_player_probability()

            if point_a < 0.33:
                score_a += 1
                curr_lives_b -= 1
            elif point_a >= 0.33 and point_a < 0.66:
                curr_lives_a -= 1
            else:
                pass

            if point_b < 0.33:
                score_b += 1
                curr_lives_a -= 1
            elif point_b >= 0.33 and point_b < 0.66:
                curr_lives_b -= 1
            else:
                pass
        
        while score_a == score_b:
            score_a += self.generate_point(self.get_player_probability())
            score_b += self.generate_point(self.get_player_probability())
            if score_a != score_b:
                break
            
        return [score_a, score_b]

    def simulate_game_by_cumulative(self):
        pass