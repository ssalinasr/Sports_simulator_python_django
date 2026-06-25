from abc import ABC, abstractmethod
from .games_interface import GamesInterface
import random

class MarioGamesInterface(GamesInterface):


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
        if type_game == 'Tiempo':
            return self.simulate_game_by_time()
        elif type_game == 'Vidas':
            return self.simulate_game_by_lives()
        elif type_game == 'Vidas Reversa':
            return self.simulate_game_by_rev_lives()
        elif type_game == 'Cumulativo':
            return self.simulate_game_by_cumulative()
        elif type_game == 'Stamina':
            return self.simulate_game_by_stamina()
        else:
            return self.simulate_game_by_time()

    def simulate_game_by_time(self):
        pass

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
       pass

    def simulate_game_by_cumulative(self):
        score_a = 0
        score_b = 0
        coins_a = 0 
        coins_b = 0

        for _ in range(self.time*60):
            points_a = self.get_player_probability()
            points_b = self.get_player_probability()
            coins_a  += random.randint(1,10)
            coins_b  += random.randint(1,10)


            if points_a < 0.05:
                score_a += 1
                score_b -= 1
                coins_b //= 2

            elif points_a >= 0.05 and points_a < 0.1:
                score_a -= 1
                coins_a //= 2
                        
            if points_b < 0.05:
                score_b += 1
                score_a -= 1
                coins_a //= 2

            elif points_b >= 0.05 and points_b < 0.1:
                score_b -= 1
                coins_b //= 2


        while coins_a == coins_b:
            points_a = self.get_player_probability()
            points_b = self.get_player_probability() 
            if points_a < 0.05:
                score_a += 1
                score_b -= 1
                coins_b //= 2

            elif points_a >= 0.05 and points_a < 0.1:
                score_a -= 1
                coins_a //= 2
                        
            if points_b < 0.05:
                score_b += 1
                score_a -= 1
                coins_a //= 2

            elif points_b >= 0.05 and points_b < 0.1:
                score_b -= 1
                coins_b //= 2

            if coins_a != coins_b:
                break

        return [coins_a, coins_b]
    
    def simulate_game_by_stamina(self):
        pass