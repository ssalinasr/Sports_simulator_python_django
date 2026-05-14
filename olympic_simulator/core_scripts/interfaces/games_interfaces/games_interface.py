from abc import ABC, abstractmethod

class GamesInterface(ABC):


    def __init__(self, game_name, game_type):
        self.game_name = game_name
        self.game_type = game_type

    @abstractmethod
    def get_player_probability(self):
        pass

    @abstractmethod
    def generate_point(self, prob):
        pass

    @abstractmethod
    def simulate_game(self, type_game):
        if type_game == 'Tiempo':
            return self.simulate_game_by_time()
        elif type_game == 'Vidas':
            return self.simulate_game_by_lives()
        elif type_game == 'Vidas Reversa':
            return self.simulate_game_by_rev_lives()
        elif type_game == 'Cumulativo':
            return self.simulate_game_by_cumulative()
        else:
            return self.simulate_game_by_time()
    
    @abstractmethod
    def simulate_game_by_time(self):
        pass

    @abstractmethod
    def simulate_game_by_lives(self):
        pass

    @abstractmethod
    def simulate_game_by_rev_lives(self):
        pass

    @abstractmethod
    def simulate_game_by_cumulative(self):
        pass