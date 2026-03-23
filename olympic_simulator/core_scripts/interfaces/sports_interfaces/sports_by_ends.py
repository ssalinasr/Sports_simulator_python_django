from .sports_interface import SportsInterface
import random

class EndsSport(SportsInterface):

    def __init__(self, sport_name, innings, extra_time, double_round):
        super().__init__(sport_name)
        self.innings = innings
        self.probs = []
        self.has_extra_time = extra_time
        self.has_double_round = double_round

    def get_probability_list(self):
        self.probs = [1/585, 1/475, 1/255, 1/184, 1/90, 1/60, 1/69, 1/50, 1/45, 1/34, 1/22, 1/9, 1/4]

    def get_team_probability(self, rank1, rank2, probs):
        return super().get_team_probability(rank1, rank2, probs)

    def simulate_match(self, rank1, rank2):
        if not self.has_double_round:
            score_a = 0
            score_b = 0
            current_inning = 1
            markers_a = []
            markers_b = []
            while True:
                #Equipo A<
                outs = 0
                curr_round = []
                while outs < 3:
                    if random.random() < self.get_team_probability(rank1, rank2, self.probs):
                        score_a += 1
                        curr_round.append('⬤')
                    else:
                        outs += 1
                if curr_round == []:
                    curr_round.append('◯')
                markers_a.append(curr_round)

                #Equipo B
                outs = 0
                curr_round = []
                while outs < 3:
                    if random.random() < self.get_team_probability(rank2, rank1, self.probs):
                        score_b += 1
                        curr_round.append('⬤')
                    else:
                        outs += 1
                if curr_round == []:
                    curr_round.append('◯')
                markers_b.append(curr_round)

                if current_inning >= self.innings and (score_a != score_b):
                    break
                    
                current_inning += 1

            return [score_a, score_b, markers_a, markers_b]
        else:
            #Primera Ronda
            score_a = 0
            score_b = 0
            globalscore_a = 0
            globalscore_b = 0
            current_inning = 1
            markers_a = []
            markers_b = []
            while True:
                #Equipo A
                outs = 0
                curr_round = []
                while outs < 3:
                    r1 = random.random()
                    if r1 < self.get_team_probability(rank1, rank2, self.probs):
                        score_a += self.generate_goal(r1, self.get_team_probability(rank1, rank2, self.probs))
                        curr_round.append('⬤')
                    else:
                        outs += 1
                if curr_round == []:
                    curr_round.append('◯')
                markers_a.append(curr_round)

                #Equipo B
                outs = 0
                curr_round = []
                while outs < 3:
                    r1 = random.random()
                    if r1 < self.get_team_probability(rank1, rank2, self.probs):
                        score_b += self.generate_goal(r1, self.get_team_probability(rank2, rank1, self.probs))
                        curr_round.append('⬤')
                    else:
                        outs += 1
                if curr_round == []:
                    curr_round.append('◯')
                markers_b.append(curr_round)

                if current_inning >= self.innings and (score_a != score_b):
                    break
                    
                current_inning += 1
            
            globalscore_a += score_a
            globalscore_b += score_b
            #Segunda ronda
            score_a = 0
            score_b = 0
            current_inning = 1
            while True:
                #Equipo A
                outs = 0
                curr_round = []
                while outs < 3:
                    r1 = random.random()
                    if  r1 < self.get_team_probability(rank1, rank2, self.probs):
                        score_a += self.generate_goal(r1, self.get_team_probability(rank1, rank2, self.probs))
                        curr_round.append('⬤')
                    else:
                        outs += 1
                if curr_round == []:
                    curr_round.append('◯')
                markers_a.append(curr_round)

                #Equipo B
                outs = 0
                curr_round = []
                while outs < 3:
                    r1 = random.random()
                    if r1 < self.get_team_probability(rank2, rank1, self.probs):
                        score_b += self.generate_goal(r1, self.get_team_probability(rank2, rank1, self.probs))
                        curr_round.append('⬤')
                    else:
                        outs += 1
                if curr_round == []:
                    curr_round.append('◯')
                markers_b.append(curr_round)

                if current_inning >= self.innings and (score_a != score_b):
                    break
                    
                current_inning += 1
            globalscore_a += score_a
            globalscore_b += score_b
            return [globalscore_a, globalscore_b, markers_a, markers_b]
        

            

    def generate_goal(self, r1, probs):
        self.sport_name = self.sport_name.replace(" Masculino","").replace(" Femenino","")
        if self.sport_name == 'Beisbol':
            if r1 < probs:
                eventos = [(1,0.75),(2,0.15),(3,0.07),(4,0.03)]
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
        elif self.sport_name == 'Curling':
            if r1 < probs:
                eventos = [(1,0.35),(2,0.35),(3,0.2),(4,0.1)]
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

    def do_tiebreaker(self, score_a, score_b, rank1, rank2, marker_1, marker_2, probs):
        pass