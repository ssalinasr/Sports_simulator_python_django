from .sports_interface import SportsInterface
import random

class TimeSport(SportsInterface):
    
    def __init__(self, sport_name, periods, period_time, extra_time, double_round):
        super().__init__(sport_name)
        self.periods = periods
        self.period_time = period_time
        self.probs = []
        self.has_extra_time = extra_time
        self.has_double_round = double_round

    def get_probability_list(self):
        self.sport_name = self.sport_name.replace(" Masculino","").replace(" Femenino","")  
        if self.sport_name == 'Futbol':
            self.probs = [1/585, 1/475, 1/255, 1/184, 1/135, 1/80, 1/59, 1/50, 1/45, 1/34, 1/22, 1/9, 1/4]
        elif self.sport_name in ['Futsal','Hockey']:
            self.probs = [1/292, 1/237, 1/123, 1/92, 1/46, 1/35, 1/30, 1/25, 1/23, 1/17, 1/11, 1/5, 1/2]
        elif self.sport_name in ['Rugby', 'Balonmano']:
            self.probs = [1/75.5, 1/55.5, 1/43.5, 1/35.5, 1/22.5, 1/17.5, 1/14.5, 1/12.5, 1/8.5, 1/5.5, 1/4.5, 1/2.5, 1/1.05]
        elif self.sport_name == 'Basketball':
            self.probs = [1/17.5, 1/12.5, 1/8.5, 1/4.15, 1/3.55, 1/2.75, 1/2.75, 1/2.05, 1/1.85, 1/1.65, 1/1.45, 1/1.2, 1/1.02]
        else:
            self.probs = [1/585, 1/475, 1/255, 1/184, 1/90, 1/60, 1/59, 1/50, 1/45, 1/34, 1/22, 1/9, 1/4]

    def get_team_probability(self, rank1, rank2, probs):
        return super().get_team_probability(rank1, rank2, probs)

    def simulate_match(self, rank1, rank2):
        goals1 = 0
        goals2 = 0
        if self.sport_name in ['Basketball Masculino', 'Basketball Femenino']:
            self.has_extra_time = True
        
        if not self.has_double_round:
            for i in range(self.period_time * self.periods):
                goals1 += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                goals2 += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))       

            if self.has_extra_time and goals1 == goals2:
                print('Aqui hubo un empate...')
                return self.do_tiebreaker(goals1, goals2, rank1, rank2)
            else:
                return [goals1, goals2]
        else:
            #Primera ronda
            for i in range(self.period_time * self.periods):
                goals1 += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                goals2 += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))
            #Segunda ronda
            for i in range(self.period_time * self.periods):
                goals1 += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                goals2 += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))           
            if self.has_extra_time:
                return self.do_tiebreaker(goals1, goals2, rank1, rank2)
            else:
                return [goals1, goals2]      


    def generate_goal(self, probs):
        if self.sport_name in ['Futbol', 'Futsal', 'Balonmano','Hockey']:
            rand = random.random()
            if rand < probs:
                return 1
            else:
                return 0
            
        elif self.sport_name == 'Basketball':
            r1 = random.random()
            if r1 < probs:
                eventos = [(1,0.2),(2,0.55),(3,0.25)]
                rand = random.random()
                acum = 0
                for pts, prob in eventos:
                    acum += prob
                    if rand <= acum:  
                        return pts
                    else:
                        return 0
            else:
                return 0
                
        elif self.sport_name == 'Rugby':
            r1 = random.random()
            if r1 < probs:
                eventos = [(3,0.6),(5,0.2),(3,0.15),(7,0.05)]
                rand = random.random()
                acum = 0
                for pts, prob in eventos:
                    acum += prob
                    if rand <= acum:  
                        return pts
                    else:
                        return 0
            else:
                return 0


    def do_tiebreaker(self, score_a, score_b, rank1, rank2):
        if self.sport_name == 'Basketball':
            is_active = True
            while is_active:      
                for i in range(30):
                    score_a += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                    score_b += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))
                if score_a != score_b or score_b != score_a:
                    is_active = False
            
            return [score_a, score_b]
        elif self.sport_name == 'Futbol':
            for i in range(30):
                score_a += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                score_b += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))
            
            if score_a == score_b:
                return self.penalties(score_a, score_b)
            else:
                return [score_a, score_b]
            
        elif self.sport_name in ['Futsal', 'Rugby', 'Hockey']:
            for i in range(20):
                score_a += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                score_b += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))
            if score_a == score_b:
                return self.penalties(score_a, score_b)
            else:
                return [score_a, score_b]
            
        elif self.sport_name == 'Balonmano':
            for i in range(10):
                score_a += self.generate_goal(self.get_team_probability(rank1, rank2, self.probs))
                score_b += self.generate_goal(self.get_team_probability(rank2, rank1, self.probs))
            if score_a == score_b:
                return self.penalties(score_a, score_b)
            else:
                return [score_a, score_b]
    

    def penalties(self, score_a, score_b):
        prob_goal = 0.75
        penalties_a = 0
        shots_a = 0
        penalties_b = 0
        shots_b = 0
        marker_a = []
        marker_b = []

        if self.sport_name == 'Hockey':
            for r in range(3):
                if random.random() < prob_goal:
                    penalties_a += 1
                    marker_a.append('⬤')
                else:
                    marker_a.append('◯')
                shots_a += 1

                if penalties_a > penalties_b + (5 - shots_b):
                    return [score_a, score_b, penalties_a, penalties_b, marker_a, marker_b]
                
                if random.random() < prob_goal:
                    penalties_b += 1
                    marker_b.append('⬤')
                else:
                    marker_b.append('◯')
                shots_b += 1

                if penalties_b > penalties_a + (5 - shots_a):
                    return [score_a, score_b, penalties_a, penalties_b, marker_a, marker_b]
        else:       
            for r in range(5):
                if random.random() < prob_goal:
                    penalties_a += 1
                    marker_a.append('⬤')
                else:
                    marker_a.append('◯')
                shots_a += 1

                if penalties_a > penalties_b + (5 - shots_b):
                    return [score_a, score_b, penalties_a, penalties_b, marker_a, marker_b]
                
                if random.random() < prob_goal:
                    penalties_b += 1
                    marker_b.append('⬤')
                else:
                    marker_b.append('◯')
                shots_b += 1

                if penalties_b > penalties_a + (5 - shots_a):
                    return [score_a, score_b, penalties_a, penalties_b, marker_a, marker_b]

        while penalties_a == penalties_b:
            gol_a = random.random() < prob_goal
            gol_b = random.random() < prob_goal
            if gol_a:
                penalties_a += 1
                marker_a.append('⬤')
            else:
                marker_a.append('◯')
            if gol_b:
                penalties_b += 1
                marker_b.append('⬤')
            else:
                marker_b.append('◯')
            if gol_a != gol_b:
                break
        
        return [score_a, score_b, penalties_a, penalties_b, marker_a, marker_b]