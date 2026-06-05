from appolympics.models import Teamregion, Nationalteams, Olympicplayers, Teamsports, Clubleague, Clubs, Playercountry, Playertournamentsports, Teamranks, Sportsrecords, Clubmatchesregister, Teamtournamentregister
from appolympics.models import Teammatchesregister, Teamtitleregister, Playertitleregister, Clubtitleregister, Playertournamentregister, Clubtournamentregister
from core_scripts.interfaces.olympic_sports_interfaces import sports_by_heats, sports_by_individual, sports_by_rounds, sports_by_elimination
import itertools, random

class SimulatedSports():
    def __init__(self, sport, deporte, table_results, ranks, match_class):
        self.sport = sport
        self.deporte = deporte
        self.table_results = table_results
        self.ranks = ranks
        self.nombres = []
        self.num_heats = 0
        self.match_class = match_class
        pass

    def simulate_olympic_sport(self):
        if self.deporte.sport_class == 'H':
            olympic_sim = sports_by_heats.SportsByHeats(self.deporte.sp_record_name, float(self.deporte.sp_record_best), float(self.deporte.sp_record_last), self.deporte.sport_class, self.sport.team_sport_name)   
            self.num_heats = 1
            if self.sport.team_sport_name == 'Ciclismo de Montania':
                self.num_heats = 8
            elif self.sport.team_sport_name == 'Tiro Deportivo':
                if any(k in self.deporte.sp_record_name for k in ['25m']):
                    self.num_heats = 5
                else:
                    self.num_heats = 6
            elif self.sport.team_sport_name in ['Bobsleigh', 'Luge', 'Skeleton','Remo']:
                self.num_heats = 4
            elif self.sport.team_sport_name in ['Esqui Alpino','Snowboard de Velocidad']:
                self.num_heats = 2
            for r in self.ranks:
                results = (r[0] ,r[1] ,olympic_sim.select_type_game(r[1], self.num_heats, 0))
                self.table_results.append(results)
        elif self.deporte.sport_class == 'T':
            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(self.deporte.sp_record_best), float(self.deporte.sp_record_last), self.deporte.sport_class, self.sport.team_sport_name)
            for r in self.ranks:
                if self.match_class in [2,4]:
                    rand = random.randint(1,7)
                    results = (r[0] ,rand, olympic_sim.select_type_game(rand, 1, 0))
                else:
                    results = (r[0] ,r[1], olympic_sim.select_type_game(r[1], 1, 0))
                self.table_results.append(results)
        elif self.deporte.sport_class == 'R':
            olympic_sim = sports_by_rounds.SportsByRounds(self.deporte.sp_record_name, float(self.deporte.sp_record_best), float(self.deporte.sp_record_last), self.deporte.sport_class, self.sport.team_sport_name)
            for r in self.ranks:
                num_rondas = 6
                self.num_heats = num_rondas
                results = (r[0] ,r[1] ,olympic_sim.select_type_game(r[1], num_rondas, 0))
                self.table_results.append(results)
        elif self.deporte.sport_class == 'E':
            olympic_sim = sports_by_elimination.SportsByElimination(self.deporte.sp_record_name, float(self.deporte.sp_record_best), float(self.deporte.sp_record_last), self.deporte.sport_class, self.sport.team_sport_name)
            for r in self.ranks:
                results = (r[0] ,r[1] ,olympic_sim.select_type_game(r[1], 0, 0))
                self.table_results.append(results)
        
        elif self.deporte.sport_class == 'P':
            try:
                rules = dict(self.sport.team_sport_rules)
            except TypeError:
                rules = ''

            if 'Heptatlón' in self.deporte.sp_record_name:
                current_rules = rules['disciplines']['heptathlon'] 
                score = 0
                final_score = 0
                sports_done = []
                for event in current_rules['events']:
                    current_sport = Sportsrecords.objects.get(sp_record_name__contains = event['name']+' Femenino', team_sport = self.sport.team_sport_id)
                    self.nombres.append(current_sport.sp_record_name)
                for r in self.ranks:
                    final_score = 0
                    sports_done = []
                    for event in current_rules['events']:
                        current_sport = Sportsrecords.objects.get(sp_record_name__contains = event['name']+' Femenino', team_sport = self.sport.team_sport_id)
                        if current_sport.sport_class == 'T':
                            olympic_sim = sports_by_individual.SportsByIndividual(current_sport.sp_record_name, float(current_sport.sp_record_best), float(current_sport.sp_record_last), current_sport.sport_class, self.sport.team_sport_name)
                            result = olympic_sim.select_type_game(r[1], 1, 0)
                            score = float(event['A']) * pow(abs(float(event['B']) - result[0]),float(event['C']))
                            sports_done.append(round(score))
                        elif current_sport.sport_class == 'E':
                            olympic_sim = sports_by_elimination.SportsByElimination(current_sport.sp_record_name, float(current_sport.sp_record_best), float(current_sport.sp_record_last), current_sport.sport_class, self.sport.team_sport_name)
                            result = olympic_sim.select_type_game(r[1], 0, 0)
                            score = float(event['A']) * pow(abs(float(result[1]) - event['B']),float(event['C']))
                            sports_done.append(round(score, 0))
                        elif current_sport.sport_class == 'R':
                            olympic_sim = sports_by_rounds.SportsByRounds(current_sport.sp_record_name, float(current_sport.sp_record_best), float(current_sport.sp_record_last), current_sport.sport_class, self.sport.team_sport_name)
                            result = olympic_sim.select_type_game(r[1], 6, 0)
                            score = float(event['A']) * pow(abs(float(result[1]) - event['B']), float(event['C']))
                            sports_done.append(round(score))
                        final_score += score
                    self.num_heats = len(sports_done)
                    results = (r[0] ,r[1] , [sports_done ,round(final_score, 0)])
                    self.table_results.append(results)
                pass

            elif 'Decatlón' in self.deporte.sp_record_name:
                current_rules = rules['disciplines']['decathlon'] 
                current_sport = None
                score = 0
                final_score = 0
                sports_done = []
                for event in current_rules['events']:
                    try:
                        current_sport = Sportsrecords.objects.get(sp_record_name__contains = event['name']+' Masculino', team_sport = self.sport.team_sport_id)
                        self.nombres.append(current_sport.sp_record_name)
                    except Sportsrecords.MultipleObjectsReturned:
                        current_sport = Sportsrecords.objects.filter(sp_record_name__contains = event['name']+' Masculino', team_sport = self.sport.team_sport_id).first()
                        self.nombres.append(current_sport.sp_record_name)
                for r in self.ranks:
                    final_score = 0
                    sports_done = []
                    for event in current_rules['events']:
                        try:
                            current_sport = Sportsrecords.objects.get(sp_record_name__contains = event['name']+' Masculino', team_sport = self.sport.team_sport_id)
                        except Sportsrecords.MultipleObjectsReturned:
                            current_sport = Sportsrecords.objects.filter(sp_record_name__contains = event['name']+' Masculino', team_sport = self.sport.team_sport_id).first()
                        if current_sport.sport_class == 'T':
                            olympic_sim = sports_by_individual.SportsByIndividual(current_sport.sp_record_name, float(current_sport.sp_record_best), float(current_sport.sp_record_last), current_sport.sport_class, self.sport.team_sport_name)
                            result = olympic_sim.select_type_game(r[1], 1, 0)
                            score = float(event['A']) * pow(abs(float(event['B']) - result[0]),float(event['C']))
                            sports_done.append(round(score))
                        elif current_sport.sport_class == 'E':
                            olympic_sim = sports_by_elimination.SportsByElimination(current_sport.sp_record_name, float(current_sport.sp_record_best), float(current_sport.sp_record_last), current_sport.sport_class, self.sport.team_sport_name)
                            result = olympic_sim.select_type_game(r[1], 0, 0)
                            score = float(event['A']) * pow(abs(float(result[1]) - event['B']),float(event['C']))
                            sports_done.append(round(score, 0))
                        elif current_sport.sport_class == 'R':
                            olympic_sim = sports_by_rounds.SportsByRounds(current_sport.sp_record_name, float(current_sport.sp_record_best), float(current_sport.sp_record_last), current_sport.sport_class, self.sport.team_sport_name)
                            result = olympic_sim.select_type_game(r[1], 6, 0)
                            score = float(event['A']) * pow(abs(float(result[1]) - event['B']), float(event['C']))
                            sports_done.append(round(score))
                        final_score += score
                    self.num_heats = len(sports_done)
                    results = (r[0] ,r[1] , [sports_done ,round(final_score, 0)])
                    self.table_results.append(results)
                pass

            elif self.sport.team_sport_name == 'Gimnasia Artistica':
                if 'Concurso general' in self.deporte.sp_record_name:
                    if 'masculino' in self.deporte.sp_record_name:
                        self.nombres = ['Barras paralelas masculinas','Barra fija masculina','Anillas masculinas','Caballo con arzones masculino','Suelo masculino','Salto de potro masculino']
                        specific_rules = rules['scoring_rules']['variables']
                        difficulty_range = specific_rules['D']['range']
                        execution_range = specific_rules['E']['base_value']
                        penalty_range = specific_rules['P']['range']
                        final_score = 0
                        country_scores = []
                        for r in self.ranks:
                            country_scores = []
                            final_score = 0
                            for _ in range(len(self.nombres)):
                                current_score = 0
                                #Simula dificultad
                                olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(difficulty_range[1]), float(difficulty_range[0]), 'T', self.sport.team_sport_name)
                                dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                                #Simula penalizaciones
                                olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                                pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                                #Puntaje final
                                final_score += dif_result[0] + (execution_range - pen_result[0]) 
                                current_score = dif_result[0] + (execution_range - pen_result[0])
                                country_scores.append(round(current_score, 3))
                            results = (r[0] ,r[1] , [country_scores ,round(final_score, 3)])
                            self.table_results.append(results)

                    else:                  
                        self.nombres = ['Barras asimétricas femeninas','Barra fija femenina','Suelo femenino','Salto de potro femenino']
                        specific_rules = rules['scoring_rules']['variables']
                        difficulty_range = specific_rules['D']['range']
                        execution_range = specific_rules['E']['base_value']
                        penalty_range = specific_rules['P']['range']
                        final_score = 0
                        country_scores = []
                        for r in self.ranks:
                            country_scores = []
                            final_score = 0
                            for _ in range(len(self.nombres)):
                                current_score = 0
                                #Simula dificultad
                                olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(difficulty_range[1]), float(difficulty_range[0]), 'T', self.sport.team_sport_name)
                                dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                                #Simula penalizaciones
                                olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                                pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                                #Puntaje final
                                final_score += dif_result[0] + (execution_range - pen_result[0])
                                current_score = dif_result[0] + (execution_range - pen_result[0])
                                country_scores.append(round(current_score, 3))
                            results = (r[0] ,r[1] , [country_scores ,round(final_score, 3)])
                            self.table_results.append(results)
                    pass   

                else:
                    specific_rules = rules['scoring_rules']['variables']
                    difficulty_range = specific_rules['D']['range']
                    execution_range = specific_rules['E']['base_value']
                    penalty_range = specific_rules['P']['range']
                    final_score = 0
                    country_scores = []
                    self.nombres = ['Dificultad', 'Penalización']
                    for r in self.ranks:
                        country_scores = []
                        final_score = 0
                        #Simula dificultad
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(difficulty_range[1]), float(difficulty_range[0]), 'T', self.sport.team_sport_name)
                        dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(dif_result[0])
                        #Simula penalizaciones
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(pen_result[0])
                        #Puntaje final
                        final_score = dif_result[0] + (execution_range - pen_result[0])
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 3)])
                        self.table_results.append(results)
                pass 

            elif self.sport.team_sport_name == 'Gimnasia Ritmica':
                if 'Concurso completo' in self.deporte.sp_record_name:
                    self.nombres = ['Aro','Pelota','Mazas','Cinta']
                    specific_rules = rules['scoring_rules']['variables']
                    difficulty_range = specific_rules['D']['range']
                    execution_range = specific_rules['E']['base_value']
                    artistic_range = specific_rules['A']['range']
                    penalty_range = specific_rules['P']['range']
                    final_score = 0
                    country_scores = []
                    for r in self.ranks:
                        country_scores = []
                        final_score = 0
                        for _ in range(len(self.nombres)):
                            current_score = 0
                            #Simula dificultad
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(difficulty_range[1]), float(difficulty_range[0]), 'T', self.sport.team_sport_name)
                            dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula Artistico
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(artistic_range[1]), float(artistic_range[0]), 'T', self.sport.team_sport_name)
                            art_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula penalizaciones
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                            pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Puntaje final
                            final_score += dif_result[0] + art_result[0] + (execution_range - pen_result[0])
                            current_score = dif_result[0] + art_result[0] + (execution_range - pen_result[0])
                            country_scores.append(round(current_score, 3))
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 3)])
                        self.table_results.append(results)
                    pass     
                else:
                    specific_rules = rules['scoring_rules']['variables']
                    difficulty_range = specific_rules['D']['range']
                    artistic_range = specific_rules['A']['range']
                    execution_range = specific_rules['E']['base_value']
                    penalty_range = specific_rules['P']['range']
                    final_score = 0
                    country_scores = []
                    self.nombres = ['Dificultad','Componente Artístico', 'Penalización']
                    for r in self.ranks:
                        country_scores = []
                        final_score = 0
                        #Simula dificultad
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(difficulty_range[1]), float(difficulty_range[0]), 'T', self.sport.team_sport_name)
                        dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(dif_result[0])
                        #Simula Artistico
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(artistic_range[1]), float(artistic_range[0]), 'T', self.sport.team_sport_name)
                        art_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(art_result[0])
                        #Simula penalizaciones
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(pen_result[0])
                        #Puntaje final
                        final_score = dif_result[0] + art_result[0] + (execution_range - pen_result[0])
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 3)])
                        self.table_results.append(results)
                pass

            elif self.sport.team_sport_name == 'Saltos':
                has_synced = False
                specific_rules = rules['scoring_rules']['variables']
                difficulty_range = specific_rules['D']['range']
                judges_range = specific_rules['J']['range']
                if 'sincronizado' in self.deporte.sp_record_name or 'sincronizada' in self.deporte.sp_record_name:
                    penalty_range = specific_rules['S']['range']
                    has_synced = True
                else:
                    penalty_range = 0.0
                final_score = 0
                country_scores = []
                if 'Masculino' in self.deporte.sp_record_name or 'Masculina' in self.deporte.sp_record_name or 'Mixto' in self.deporte.sp_record_name or 'Mixta' in self.deporte.sp_record_name:
                    self.nombres = ['Salto '+str(i) for i in range(6)]
                else:
                    self.nombres = ['Salto '+str(i) for i in range(5)]
                for r in self.ranks:
                    total_score = 0
                    country_scores = []
                    for _ in range(len(self.nombres)):
                        final_score = 0
                        #Simula dificultad
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(difficulty_range[1]), float(difficulty_range[0]), 'T', self.sport.team_sport_name)
                        dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                        #Simula Jueces
                        judges_scores = []
                        for _ in range(5):
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(judges_range[1]), float(judges_range[0]), 'T', self.sport.team_sport_name)
                            judge_score = olympic_sim.select_type_game(r[1], 1, 0)
                            judges_scores.append(judge_score)
                        judges_scores.remove(max(judges_scores))
                        judges_scores.remove(min(judges_scores))
                        #Simula penalizaciones
                        if has_synced:
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                            pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                            flat_list = list(itertools.chain.from_iterable(judges_scores))
                            final_score = dif_result[0] * sum(flat_list) * 0.8 - pen_result[0]
                        else:
                            #Puntaje final
                            flat_list = list(itertools.chain.from_iterable(judges_scores))
                            final_score = dif_result[0] * sum(flat_list) * 0.8
                        total_score += final_score
                        country_scores.append(round(final_score, 2))
                    results = (r[0] ,r[1] , [country_scores ,round(total_score, 2)])
                    self.table_results.append(results)
                    pass

            elif self.sport.team_sport_name == 'Gimnasia en Trampolin':
                has_synced = False
                specific_rules = rules['scoring_rules']['variables']
                difficulty_range = specific_rules['D']['range']
                horizontal_range = specific_rules['H']['range']
                time_range = specific_rules['T']['range']
                execution_range = 10.0
                penalty_range = specific_rules['P']['range']
                if 'sincronizado' in self.deporte.sp_record_name or 'sincronizada' in self.deporte.sp_record_name:
                    sync_range = specific_rules['S']['range']
                    has_synced = True
                    self.nombres = ['Dificultad','Ejecución','Tiempo de Vuelo','Despl.Horizontal','Penalización','Sincronización']
                else:
                    sync_range = 0.0
                    self.nombres = ['Dificultad','Ejecución','Tiempo de Vuelo','Despl.Horizontal','Penalización']
                final_score = 0
                country_scores = []
                for r in self.ranks:
                    country_scores = []
                    final_score = 0
                    #Simula dificultad
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(difficulty_range[1]), float(difficulty_range[0]), 'T', self.sport.team_sport_name)
                    dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(dif_result[0])
                    #Simula ejecución
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(execution_range), float(execution_range - 5), 'T', self.sport.team_sport_name)
                    exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(exec_result[0])
                    #Simula tiempo de vuelo
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(time_range[1]), float(time_range[0]), 'T', self.sport.team_sport_name)
                    time_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(time_range[0])
                    #Simula Despl.Horizontal
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(horizontal_range[0]), float(horizontal_range[1]), 'T', self.sport.team_sport_name)
                    hor_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(hor_result[0])
                    #Simula penalizaciones
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                    pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(pen_result[0])
                    if has_synced:
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(sync_range[0]), float(sync_range[1]), 'T', self.sport.team_sport_name)
                        sync_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(sync_result[0])
                        final_score = dif_result[0] + (time_result[0] + hor_result[0] + exec_result[0] + sync_result[0]) - pen_result[0] - random.randint(0,2)
                    else:
                        #Puntaje final
                        final_score = dif_result[0] + (time_result[0] + hor_result[0] + exec_result[0]) - pen_result[0] - random.randint(0,2)

                    results = (r[0] ,r[1] , [country_scores ,round(final_score, 3)])
                    self.table_results.append(results)
                pass

            elif self.sport.team_sport_name == 'Nado Sincronizado':
                has_synced = False
                specific_rules = rules['scoring_rules']['variables']
                difficulty_range = specific_rules['D']['range']
                artistic_range = specific_rules['A']['range']
                execution_range = 10.0
                penalty_range = specific_rules['P']['range']
                if 'sincronizado' in self.deporte.sp_record_name or 'sincronizada' in self.deporte.sp_record_name:
                    sync_range = specific_rules['S']['range']
                    has_synced = True
                    self.nombres = ['Dificultad','Ejecución','Componente Artístico','Penalización','Sincronización']
                else:
                    sync_range = 0.0
                    self.nombres = ['Dificultad','Ejecución','Componenete Artístico','Penalización']
                final_score = 0
                country_scores = []
                for r in self.ranks:
                    country_scores = []
                    final_score = 0
                    #Simula dificultad
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(difficulty_range[1]), float(difficulty_range[0]), 'T', self.sport.team_sport_name)
                    dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(dif_result[0])
                    #Simula ejecución
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(execution_range), float(execution_range - 5), 'T', self.sport.team_sport_name)
                    exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(exec_result[0])
                    #Simula artistico
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(artistic_range[1]), float(artistic_range[0]), 'T', self.sport.team_sport_name)
                    art_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(art_result[0])
                    #Simula penalizaciones
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                    pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(pen_result[0])
                    if has_synced:
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(sync_range[0]), float(sync_range[1]), 'T', self.sport.team_sport_name)
                        sync_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(sync_result[0])
                        if 'libre' in self.deporte.sp_record_name:
                            final_score = (dif_result[0]*0.35) + (exec_result[0]*0.25) + (art_result[0]*0.3) + (sync_result[0]*0.1) - pen_result[0] - random.randint(0,2)
                        elif 'técnica' in self.deporte.sp_record_name:
                            final_score = (dif_result[0]*0.4) + (exec_result[0]*0.35) + (art_result[0]*0.15) + (sync_result[0]*0.1) - pen_result[0] - random.randint(0,2)
                        elif 'acrobática' in self.deporte.sp_record_name:
                            final_score = (dif_result[0]*0.45) + (exec_result[0]*0.2) + (art_result[0]*0.2) + (sync_result[0]*0.15) - pen_result[0] - random.randint(0,2)
                    else:
                        #Puntaje final
                        if 'libre' in self.deporte.sp_record_name:
                            final_score = (dif_result[0]*0.4) + (exec_result[0]*0.3) + (art_result[0]*0.3) - pen_result[0] - random.randint(0,2)
                        elif 'técnica' in self.deporte.sp_record_name:
                            final_score = (dif_result[0]*0.4) + (exec_result[0]*0.4) + (art_result[0]*0.2) - pen_result[0] - random.randint(0,2)
                        elif 'acrobática' in self.deporte.sp_record_name:
                            final_score = (dif_result[0]*0.45) + (exec_result[0]*0.28) + (art_result[0]*0.27) - pen_result[0] - random.randint(0,2)

                    results = (r[0] ,r[1] , [country_scores ,round(final_score, 3)])
                    self.table_results.append(results)
                pass

            elif self.sport.team_sport_name == 'Equitacion':
                if 'Doma' in self.deporte.sp_record_name:
                    best_possible = 100
                    last_possible = 45
                    final_score = 0
                    country_scores = []
                    if 'libre' in self.deporte.sp_record_name:
                        self.nombres = ['Técnica', 'Doma', 'Precisión', 'Sincronía', 'Ritmo', 'Balance']
                    elif 'clásica' in self.deporte.sp_record_name:
                        self.nombres = ['Técnica', 'Doma', 'Precisión', 'Sincronía', 'Ritmo', 'Concentración']

                    for r in self.ranks:
                        if 'equipos' in self.deporte.sp_record_name:
                            self.nombres = ['Puntaje '+str(n) for n in range(3)]
                            country_scores = []
                            for _ in range(len(self.nombres)):
                                final_score = 0
                                #Simula Técnica
                                olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                                tec_result = olympic_sim.select_type_game(r[1], 1, 0)
                                #Simula Doma
                                olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                                dom_result = olympic_sim.select_type_game(r[1], 1, 0)
                                #Simula Precisión/creatividad
                                olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                                prc_result = olympic_sim.select_type_game(r[1], 1, 0)
                                #Simula Sincronía
                                olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                                sync_result = olympic_sim.select_type_game(r[1], 1, 0)
                                #Simula Ritmo
                                olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                                rit_result = olympic_sim.select_type_game(r[1], 1, 0)
                                #Simula Concentración/Balance
                                olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                                cb_result = olympic_sim.select_type_game(r[1], 1, 0)
                                #Puntaje final
                                final_score = (tec_result[0]*0.26) + (dom_result[0]*0.26) + (prc_result[0]*0.14)  +(sync_result[0]*0.14) + (rit_result[0]*0.1) + (cb_result[0]*0.08) + random.randint(0,2)         
                                country_scores.append(round(final_score, 2))
                                pass
                            results = (r[0] ,r[1] , [country_scores ,round(sum(country_scores), 2)])
                            self.table_results.append(results)
                        else:
                            final_score = 0 
                            country_scores = []
                            #Simula Técnica
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            tec_result = olympic_sim.select_type_game(r[1], 1, 0)
                            country_scores.append(tec_result[0])
                            #Simula Doma
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            dom_result = olympic_sim.select_type_game(r[1], 1, 0)
                            country_scores.append(dom_result[0])
                            #Simula Precisión/creatividad
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            prc_result = olympic_sim.select_type_game(r[1], 1, 0)
                            country_scores.append(prc_result[0])
                            #Simula Sincronía
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            sync_result = olympic_sim.select_type_game(r[1], 1, 0)
                            country_scores.append(sync_result[0])
                            #Simula Ritmo
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            rit_result = olympic_sim.select_type_game(r[1], 1, 0)
                            country_scores.append(rit_result[0])
                            #Simula Concentración/Balance
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            cb_result = olympic_sim.select_type_game(r[1], 1, 0)
                            country_scores.append(cb_result[0])
                            if 'libre' in self.deporte.sp_record_name:
                                final_score = (tec_result[0]*0.26) + (prc_result[0]*0.26) + (prc_result[0]*0.15) + (dom_result[0]*0.26) + (sync_result[0]*0.14) + (rit_result[0]*0.1) + (cb_result[0]*0.09) + random.randint(0,2)            
                            elif 'clásica' in self.deporte.sp_record_name:
                                final_score = (tec_result[0]*0.26) + (dom_result[0]*0.26) + (prc_result[0]*0.14)  +(sync_result[0]*0.14) + (rit_result[0]*0.1) + (cb_result[0]*0.08) + random.randint(0,2)         
                                pass
                            results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                            self.table_results.append(results)
                    pass
                elif 'obstáculos' in self.deporte.sp_record_name:
                    best_possible = 0
                    last_possible = 8
                    final_score = 0
                    country_scores = []
                    for r in self.ranks:
                        if 'equipos' in self.deporte.sp_record_name:
                            self.nombres = ['Puntaje '+str(n) for n in range(3)]
                            country_scores = []
                            for _ in range(len(self.nombres)):
                                final_score = 0
                                for _ in range(5):
                                    rand = random.random()
                                    thresholds = {
                                        1: 0.9,
                                        2: 0.75,
                                        3: 0.6,
                                        4: 0.45,
                                        5: 0.15,
                                        6: 0.05,
                                        7: 0.01
                                    }
                                    final_score += 4 if rand >= thresholds.get(r[1], 0) else 0
                                country_scores.append(round(final_score, 2))
                                pass
                            results = (r[0] ,r[1] , [country_scores ,round(sum(country_scores), 2)])
                            self.table_results.append(results)
                        else:
                            final_score = 0 
                            for _ in range(5):
                                rand = random.random()
                                #Puntaje Final
                                thresholds = {
                                    1: 0.9,
                                    2: 0.75,
                                    3: 0.6,
                                    4: 0.45,
                                    5: 0.15,
                                    6: 0.05,
                                    7: 0.01
                                }
                                final_score += 4 if rand >= thresholds.get(r[1], 0) else 0

                            results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                            self.table_results.append(results)
                    pass
                pass

            elif self.sport.team_sport_name == 'Skateboarding':
                if 'Park' in self.deporte.sp_record_name:
                    best_possible = self.deporte.sp_record_best
                    last_possible = self.deporte.sp_record_last
                    self.nombres = ['Ronda '+str(i) for i in range(3)]
                    for r in self.ranks:
                        country_scores = []
                        for _ in range(len(self.nombres)):
                            final_score = 0 
                            #Simula Dificultad
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            dif_result = olympic_sim.select_type_game(r[1], 1, 0)    
                            #Simula Ejecución
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula amplitud    
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            amp_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula flow    
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            flow_result = olympic_sim.select_type_game(r[1], 1, 0)    
                            #Simula Variedad
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            var_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula Originalidad    
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            og_result = olympic_sim.select_type_game(r[1], 1, 0)    
                            #Simula Consistencia
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            cons_result = olympic_sim.select_type_game(r[1], 1, 0)    
                            #Simula Penalización
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(0.0), float(10.0), 'T', self.sport.team_sport_name)
                            pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Puntaje final
                            final_score = (dif_result[0]*0.25)+(exec_result[0]*0.25)+(amp_result[0]*0.15)+(flow_result[0]*0.15)+(var_result[0]*0.1)+(og_result[0]*0.05)+(cons_result[0]*0.05)-(pen_result[0]) - random.randint(0,5)
                            if final_score <= 0: final_score = 0.0 
                            country_scores.append(round(final_score,2))
                        results = (r[0] ,r[1] , [country_scores ,round(sum(country_scores), 2)])
                        self.table_results.append(results)
                    pass
                elif 'Street' in self.deporte.sp_record_name:
                    best_possible = self.deporte.sp_record_best
                    last_possible = self.deporte.sp_record_last
                    all_results = []
                    #Rondas
                    self.nombres = ['Ronda '+str(i) for i in range(2)]
                    self.nombres += ['Trick '+str(i) for i in range(5)]
                    country_scores = []
                    for r in self.ranks:
                        country_scores = []
                        for _ in range(2):
                            final_score = 0 
                            #Simula Dificultad
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            dif_result = olympic_sim.select_type_game(r[1], 1, 0)    
                            #Simula Ejecución
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula flow    
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            flow_result = olympic_sim.select_type_game(r[1], 1, 0)  
                            #Simula Variedad
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            var_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula Uso    
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            use_result = olympic_sim.select_type_game(r[1], 1, 0)    
                            #Simula Penalización
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(0.0), float(10.0), 'T', self.sport.team_sport_name)
                            pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Puntaje final
                            final_score = (dif_result[0]*0.2)+(exec_result[0]*0.3)+(flow_result[0]*0.25)+(var_result[0]*0.15)+(use_result[0]*0.1)-(pen_result[0]) - random.randint(0,5)
                            if final_score <= 0: final_score = 0.0 
                            country_scores.append(round(final_score,2))

                        round_result = max(country_scores)
                        #Tricks
                        tricks_scores = []

                        for _ in range(5):
                            final_score = 0 
                            #Simula Dificultad
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            dif_result = olympic_sim.select_type_game(r[1], 1, 0)    
                            #Simula Ejecución
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula flow    
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            flow_result = olympic_sim.select_type_game(r[1], 1, 0)  
                            #Simula Variedad
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            var_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula Uso    
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            use_result = olympic_sim.select_type_game(r[1], 1, 0)    
                            #Simula Penalización
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(0.0), float(10.0), 'T', self.sport.team_sport_name)
                            pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Puntaje final
                            final_score = (dif_result[0]*0.2)+(exec_result[0]*0.3)+(flow_result[0]*0.25)+(var_result[0]*0.15)+(use_result[0]*0.1)-(pen_result[0]) - random.randint(0,5)
                            if final_score <= 0: final_score = 0.0 
                            tricks_scores.append(round(final_score,2))
                        trick_results = sorted(tricks_scores, reverse=True)[:2]
                        all_results = country_scores + tricks_scores
                        full_scores = []
                        full_scores.append(round_result)
                        full_scores.extend(trick_results)
                        results = (r[0] ,r[1] , [all_results ,round(sum(full_scores), 2)])
                        self.table_results.append(results)
                    pass
                pass

            elif self.sport.team_sport_name == 'Vela':
                best_possible = self.deporte.sp_record_best
                last_possible = self.deporte.sp_record_last
                final_score = 0
                specific_rules = rules['disciplines']
                first_range = []
                second_range = []
                third_range = []
                country_scores = []
                if 'Laser' in self.deporte.sp_record_name:
                    specific_rules = specific_rules['laser']['scoring_rules']['variables']
                    first_range = specific_rules['V']['range']
                    second_range = specific_rules['E']['range']
                    third_range = specific_rules['C']['range']
                    self.nombres = ['Tiempo','Variación viento','Errores','Corriente']
                    pass
                elif 'iQfoil' in self.deporte.sp_record_name:
                    specific_rules = specific_rules['iqfoil']['scoring_rules']['variables']
                    first_range = specific_rules['V']['range']
                    second_range = specific_rules['E']['range']
                    third_range = specific_rules['P']['range']
                    self.nombres = ['Tiempo','Variación viento','Errores','Penalizaciones']
                    pass
                elif 'Kite' in self.deporte.sp_record_name:
                    specific_rules = specific_rules['kite']['scoring_rules']['variables']
                    first_range = specific_rules['V']['range']
                    second_range = specific_rules['M']['range']
                    third_range = specific_rules['P']['range']
                    self.nombres = ['Tiempo','Variación viento','Maniobras','Penalizaciones']
                    pass
                elif '49er' in self.deporte.sp_record_name:
                    specific_rules = specific_rules['49er']['scoring_rules']['variables']
                    first_range = specific_rules['V']['range']
                    second_range = specific_rules['B']['range']
                    third_range = specific_rules['M']['range']
                    self.nombres = ['Tiempo','Variación viento','Balance','Maniobras']
                    pass
                elif '470' in self.deporte.sp_record_name:
                    specific_rules = specific_rules['470_mixed']['scoring_rules']['variables']
                    first_range = specific_rules['V']['range']
                    second_range = specific_rules['C']['range']
                    third_range = specific_rules['A']['range']
                    self.nombres = ['Tiempo','Variación viento','Coordinación','Táctica']
                    pass
                elif 'Nacra' in self.deporte.sp_record_name:
                    specific_rules = specific_rules['nacra17_mixed']['scoring_rules']['variables']
                    first_range = specific_rules['V']['range']
                    second_range = specific_rules['M']['range']
                    third_range = specific_rules['P']['range']
                    self.nombres = ['Tiempo','Variación viento','Maniobras','Penalizaciones']
                    pass

                for r in self.ranks:
                    final_score = 0.0
                    country_scores = []
                    #Simula Tiempo
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                    time_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(round(time_result[0],2))
                    #Simula primera variable
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(first_range[0]), float(first_range[1]), 'T', self.sport.team_sport_name)
                    first_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(round(first_result[0],2))
                    #Simula primera variable
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(second_range[0]), float(second_range[1]), 'T', self.sport.team_sport_name)
                    second_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(round(second_result[0],2))
                    #Simula primera variable
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(third_range[0]), float(third_range[1]), 'T', self.sport.team_sport_name)
                    third_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(round(third_result[0],2))
                    #Puntaje final
                    final_score = time_result[0]+first_result[0]+second_result[0]+third_result[0] + random.randint(0,5)
                    results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                    self.table_results.append(results)
                    pass
                
                pass

            elif self.sport.team_sport_name == 'Biatlon':
                best_possible = self.deporte.sp_record_best
                last_possible = self.deporte.sp_record_last
                final_score = 0
                country_scores = []
                self.nombres = ['Tiempo','Penalizaciones']

                for r in self.ranks:
                    final_score = 0.0
                    country_scores = []
                    #Simula Tiempo
                    olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                    time_result = olympic_sim.select_type_game(r[1], 1, 0)
                    country_scores.append(round(time_result[0],2))
                    #Simula Penalizaciones
                    pens = random.randint(0,3)
                    country_scores.append(pens)
                    #Puntaje final
                    if '10km' in self.deporte.sp_record_name or '12,5km' in self.deporte.sp_record_name or '15km' in self.deporte.sp_record_name or '7,5km' in self.deporte.sp_record_name:
                        final_score = time_result[0] + (25 * pens)
                    elif '20km' in self.deporte.sp_record_name:
                        final_score = time_result[0] + (60 * pens)
                    elif '4x7,5km' in self.deporte.sp_record_name or '4x6km' in self.deporte.sp_record_name:
                        final_score = (time_result[0]*4) + (60 * pens)

                
                    results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                    self.table_results.append(results)
                pass

            elif self.sport.team_sport_name == 'Esqui Acrobatico':
                best_possible = self.deporte.sp_record_best
                last_possible = self.deporte.sp_record_last
                final_score = 0
                country_scores = []
                
                for r in self.ranks:
                    if 'Baches' in self.deporte.sp_record_name:
                        final_score = 0
                        country_scores = []
                        self.nombres = ['Giros','Saltos','Tiempo','Penalizaciones']
                        #Simula giros
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        turn_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(turn_result[0], 2))
                        #Simula saltos
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        jump_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(jump_result[0], 2))
                        #Simula tiempo
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        time_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(time_result[0], 2))
                        #Simula penalizaciones
                        penalty_range = rules['disciplines']['baches']['scoring_rules']['variables']['P']['range']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(pen_result[0], 2))
                        #Puntaje final
                        final_score = (turn_result[0]*0.6)+(jump_result[0]*0.2)+(time_result[0]*0.2) - pen_result[0]  - random.randint(0,5)
                        if final_score <= 0: final_score = 0.0
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                        self.table_results.append(results)
                        pass
                    elif 'Halfpipe' in self.deporte.sp_record_name:
                        final_score = 0
                        country_scores = []
                        self.nombres = ['Dificultad','Amplitud','Variedad','Ejecución','Aterrizaje','Penalizaciones']
                        #Simula dificultad
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(dif_result[0], 2))
                        #Simula amplitud
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        amp_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(amp_result[0], 2))
                        #Simula variedad
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        var_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(var_result[0], 2))
                        #Simula ejecución
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(exec_result[0], 2))
                        #Simula aterrizaje
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        land_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(land_result[0], 2))
                        #Simula penalizaciones
                        penalty_range = rules['disciplines']['halfpipe']['scoring_rules']['variables']['P']['range']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(pen_result[0], 2))
                        #Puntaje final
                        final_score = (dif_result[0]*0.25) + (amp_result[0]*0.2) + (var_result[0]*0.15) + (exec_result[0]*0.3) + (land_result[0]*0.1) - pen_result[0]  - random.randint(0,5)
                        if final_score <= 0: final_score = 0.0
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                        self.table_results.append(results)
                        pass
                    elif 'Salto aéreo por equipos' in self.deporte.sp_record_name:
                        final_score = 0
                        country_scores = []
                        self.nombres = ['Puntaje '+str(n) for n in range(3)]
                        for _ in range(len(self.nombres)):
                            #Simula dificultad
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula despuege
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            des_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula ejecución
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula aterrizaje
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            land_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula penalizaciones
                            penalty_range = rules['disciplines']['salto_aereo']['scoring_rules']['variables']['P']['range']
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                            pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Puntaje final
                            final_score = (dif_result[0]*0.2) + (des_result[0]*0.2) + (exec_result[0]*0.3) + (land_result[0]*0.3) - pen_result[0]  - random.randint(0,5)
                            if final_score <= 0: final_score = 0.0
                            country_scores.append(round(final_score, 2))

                        results = (r[0] ,r[1] , [country_scores , round(sum(country_scores),2)])
                        self.table_results.append(results)
                        pass

                    elif 'Salto aéreo' in self.deporte.sp_record_name:
                        final_score = 0
                        country_scores = []
                        self.nombres = ['Grado de dificultad','Despegue','Ejecución','Aterrizaje','Penalizaciones']
                        #Simula dificultad
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(dif_result[0], 2))
                        #Simula despuege
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        des_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(des_result[0], 2))
                        #Simula ejecución
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(exec_result[0], 2))
                        #Simula aterrizaje
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        land_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(land_result[0], 2))
                        #Simula penalizaciones
                        penalty_range = rules['disciplines']['salto_aereo']['scoring_rules']['variables']['P']['range']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(pen_result[0], 2))
                        #Puntaje final
                        final_score = (dif_result[0]*0.2) + (des_result[0]*0.2) + (exec_result[0]*0.3) + (land_result[0]*0.3) - pen_result[0]  - random.randint(0,5)
                        if final_score <= 0: final_score = 0.0
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                        self.table_results.append(results)
                        pass

                    elif 'Big air' in self.deporte.sp_record_name:
                        final_score = 0
                        country_scores = []
                        self.nombres = ['Dificultad','Amplitud','Estilo','Ejecución','Aterrizaje','Penalizaciones']
                        #Simula dificultad
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(dif_result[0], 2))
                        #Simula amplitud
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        amp_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(amp_result[0], 2))
                        #Simula estilo
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        style_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(style_result[0], 2))
                        #Simula ejecución
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(exec_result[0], 2))
                        #Simula aterrizaje
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        land_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(land_result[0], 2))
                        #Simula penalizaciones
                        penalty_range = rules['disciplines']['big_air']['scoring_rules']['variables']['P']['range']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(pen_result[0], 2))
                        #Puntaje final
                        final_score = (dif_result[0]*0.3) + (amp_result[0]*0.15) + (style_result[0]*0.05) + (exec_result[0]*0.3) + (land_result[0]*0.2) - pen_result[0] - random.randint(0,5)
                        if final_score <= 0: final_score = 0.0
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                        self.table_results.append(results)
                        pass
                    elif 'Slopestyle' in self.deporte.sp_record_name:
                        final_score = 0
                        country_scores = []
                        self.nombres = ['Dificultad','Variedad','Fluidez','Ejecución','Aterrizaje','Penalizaciones']
                        #Simula dificultad
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        dif_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(dif_result[0], 2))
                        #Simula variedad
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        var_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(var_result[0], 2))
                        #Simula fluidez
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        flow_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(flow_result[0], 2))
                        #Simula ejecución
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(exec_result[0], 2))
                        #Simula aterrizaje
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        land_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(land_result[0], 2))
                        #Simula penalizaciones
                        penalty_range = rules['disciplines']['slopestyle']['scoring_rules']['variables']['P']['range']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(pen_result[0], 2))
                        #Puntaje final
                        final_score = (dif_result[0]*0.3) + (var_result[0]*0.2) + (flow_result[0]*0.15) + (exec_result[0]*0.25) + (land_result[0]*0.15) - pen_result[0]  - random.randint(0,5)
                        if final_score <= 0: final_score = 0.0
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                        self.table_results.append(results)
                        pass
                    elif 'Campo a través' in self.deporte.sp_record_name:
                        final_score = 0
                        country_scores = []
                        self.nombres = ['Tiempo Base', 'Bonus técnico','Penalizaciones']
                        #Simula tiempo base
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        time_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(time_result[0], 2))
                        #Simula bonus
                        bonus_range = rules['disciplines']['ski_cross']['scoring_rules']['variables']['TB']['range']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(bonus_range[0]), float(bonus_range[1]), 'T', self.sport.team_sport_name)
                        bonus_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(bonus_result[0], 2))
                        #Simula penalizaciones
                        penalty_range = rules['disciplines']['ski_cross']['scoring_rules']['variables']['P']['range']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(pen_result[0], 2))
                        #Puntaje final
                        final_score = (time_result[0] - bonus_result[0]) + pen_result[0] + random.randint(0,5)
                        if final_score <= 0: final_score = 0.0
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                        self.table_results.append(results)
                        pass
                pass

            elif self.sport.team_sport_name == 'Snowboard Acrobatico':
                best_possible = 100.0
                last_possible = 0.0
                final_score = 0
                country_scores = []
                for r in self.ranks:
                    if 'Slopestyle' in self.deporte.sp_record_name:
                        final_score = 0
                        country_scores = []
                        self.nombres = ['Tricks','Ejecucion','Amplitud','Rieles','Aterrizaje','Estilo','Penalizaciones']
                        #Simula dificultad
                        tricks_range = rules['disciplines']['slopestyle']['scoring_rules']['variables']['T']['range']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(tricks_range[1]), float(tricks_range[0]), 'T', self.sport.team_sport_name)
                        trick_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(trick_result[0], 2))
                        #Simula ejecución
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(exec_result[0], 2))
                        #Simula amplitud
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        amp_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(amp_result[0], 2))
                        #Simula rieles
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        rail_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(rail_result[0], 2))
                        #Simula aterrizaje
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        land_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(land_result[0], 2))
                        #Simula estilo
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        style_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(style_result[0], 2))
                        #Simula penalizaciones
                        penalty_range = rules['disciplines']['slopestyle']['scoring_rules']['variables']['P']['range_per_penalty']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(pen_result[0], 2))
                        #Puntaje final
                        final_score = (trick_result[0]*0.3) + (exec_result[0]*0.25) + (amp_result[0]*0.15) + (rail_result[0]*0.1) + (land_result[0]*0.1) + (style_result[0]*0.1)- pen_result[0]  - random.randint(0,5)
                        if final_score <= 0: final_score = 0.0
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                        self.table_results.append(results)
                        pass
                    elif 'Halfpipe' in self.deporte.sp_record_name:
                        final_score = 0
                        country_scores = []
                        self.nombres = ['Tricks','Ejecucion','Amplitud','Flow','Aterrizaje','Estilo','Penalizaciones']
                        #Simula dificultad
                        tricks_range = rules['disciplines']['halfpipe']['scoring_rules']['variables']['T']['range']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(tricks_range[1]), float(tricks_range[0]), 'T', self.sport.team_sport_name)
                        trick_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(trick_result[0], 2))
                        #Simula ejecución
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(exec_result[0], 2))
                        #Simula amplitud
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        amp_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(amp_result[0], 2))
                        #Simula flow
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        flow_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(flow_result[0], 2))
                        #Simula aterrizaje
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        land_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(land_result[0], 2))
                        #Simula estilo
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        style_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(style_result[0], 2))
                        #Simula penalizaciones
                        penalty_range = rules['disciplines']['halfpipe']['scoring_rules']['variables']['P']['range_per_penalty']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(pen_result[0], 2))
                        #Puntaje final
                        final_score = (trick_result[0]*0.28) + (exec_result[0]*0.25) + (amp_result[0]*0.2) + (flow_result[0]*0.1) + (land_result[0]*0.1) + (style_result[0]*0.07)- pen_result[0]  - random.randint(0,5)
                        if final_score <= 0: final_score = 0.0
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                        self.table_results.append(results)
                        pass
                    elif 'Big Air' in self.deporte.sp_record_name:
                        final_score = 0
                        country_scores = []
                        self.nombres = ['Tricks','Ejecucion','Amplitud','Grab','Aterrizaje','Estilo','Penalizaciones']
                        #Simula dificultad
                        tricks_range = rules['disciplines']['halfpipe']['scoring_rules']['variables']['T']['range']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(tricks_range[1]), float(tricks_range[0]), 'T', self.sport.team_sport_name)
                        trick_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(trick_result[0], 2))
                        #Simula ejecución
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(exec_result[0], 2))
                        #Simula amplitud
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        amp_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(amp_result[0], 2))
                        #Simula grab
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        grab_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(grab_result[0], 2))
                        #Simula aterrizaje
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        land_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(land_result[0], 2))
                        #Simula estilo
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        style_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(style_result[0], 2))
                        #Simula penalizaciones
                        penalty_range = rules['disciplines']['halfpipe']['scoring_rules']['variables']['P']['range_per_penalty']
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(pen_result[0], 2))
                        #Puntaje final
                        final_score = (trick_result[0]*0.35) + (exec_result[0]*0.15) + (amp_result[0]*0.25) + (grab_result[0]*0.05) + (land_result[0]*0.15) + (style_result[0]*0.05)- pen_result[0]  - random.randint(0,5)
                        if final_score <= 0: final_score = 0.0
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                        self.table_results.append(results)
                        pass
                pass

            elif self.sport.team_sport_name == 'Patinaje Artistico sobre Hielo':
                final_score = 0
                country_scores = []
                if 'Individual' in self.deporte.sp_record_name:
                    specific_rules = rules['disciplines']['individual']
                    #Rangos Componente Técnico
                    if 'masculino' in self.deporte.sp_record_name:
                        base_value = specific_rules['technical_element_score']['variables']['BV']['ranges']['male']
                    else:
                        base_value = specific_rules['technical_element_score']['variables']['BV']['ranges']['female']

                    grade_of_exec = specific_rules['technical_element_score']['variables']['GOE']['range']

                    #Rangos Puntaje Programa
                    skills_range = specific_rules['program_component_score']['variables']['SS']['range']
                    cor_range = specific_rules['program_component_score']['variables']['C']['range']
                    int_range = specific_rules['program_component_score']['variables']['I']['range']
                    trans_range = specific_rules['program_component_score']['variables']['T']['range']
                    sync_range = specific_rules['program_component_score']['variables']['S']['range']

                    #Rango penalizaciones
                    penalty_range = [0, 15]
                    self.nombres = ['Componente técnico','Puntaje programa','Penalizaciones']

                    for r in self.ranks:
                        final_score = 0
                        country_scores = []
                        #Simula BV
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(base_value[1]), float(base_value[0]), 'T', self.sport.team_sport_name)
                        base_value_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula GOE
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(grade_of_exec[1]), float(grade_of_exec[0]), 'T', self.sport.team_sport_name)
                        exec_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula Skating Skills
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(skills_range[1]), float(skills_range[0]), 'T', self.sport.team_sport_name)
                        skills_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula Coreografía
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(cor_range[1]), float(cor_range[0]), 'T', self.sport.team_sport_name)
                        cor_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula Interpretación
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(int_range[1]), float(int_range[0]), 'T', self.sport.team_sport_name)
                        int_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula Trancisiones
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(trans_range[1]), float(trans_range[0]), 'T', self.sport.team_sport_name)
                        trans_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula Sincronización
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(sync_range[1]), float(sync_range[0]), 'T', self.sport.team_sport_name)
                        sync_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula Penalizaciones
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Calcula TES
                        TES = base_value_result[0] + exec_result[0] - random.randint(0,5)
                        country_scores.append(round(TES,2))
                        #Calcula PCS
                        PCS = skills_result[0] + cor_result[0] + int_result[0] + trans_result[0] + sync_result[0] - random.randint(0,5)
                        country_scores.append(round(PCS,2))
                        country_scores.append(round(pen_result[0],2))
                        #Puntaje final
                        final_score = PCS + TES - pen_result[0]
                        if final_score <= 0: final_score = 0.0
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                        self.table_results.append(results)
                    pass
                else:
                    specific_rules = rules['disciplines']['pairs_ice_dance']
                    #Rangos Componente Técnico
                    base_value = specific_rules['technical_element_score']['variables']['BV']['range']
                    grade_of_exec = specific_rules['technical_element_score']['variables']['GOE']['range']
                    liftings = specific_rules['technical_element_score']['variables']['L']['range']

                    #Rangos Puntaje Programa
                    cor_range = specific_rules['program_component_score']['variables']['C']['range']
                    int_range = specific_rules['program_component_score']['variables']['I']['range']
                    sync_range = specific_rules['program_component_score']['variables']['S']['range']

                    #Rango penalizaciones
                    penalty_range = [0, 15]
                    self.nombres = ['Componente técnico','Puntaje programa','Penalizaciones']

                    for r in self.ranks:
                        final_score = 0
                        country_scores = []
                        #Simula BV
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(base_value[1]), float(base_value[0]), 'T', self.sport.team_sport_name)
                        base_value_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula GOE
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(grade_of_exec[1]), float(grade_of_exec[0]), 'T', self.sport.team_sport_name)
                        exec_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula Liftings
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(liftings[1]), float(liftings[0]), 'T', self.sport.team_sport_name)
                        liftings_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula Coreografía
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(cor_range[1]), float(cor_range[0]), 'T', self.sport.team_sport_name)
                        cor_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula Interpretación
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(int_range[1]), float(int_range[0]), 'T', self.sport.team_sport_name)
                        int_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula Sincronización
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(sync_range[1]), float(sync_range[0]), 'T', self.sport.team_sport_name)
                        sync_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Simula Penalizaciones
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)

                        #Calcula TES
                        TES = base_value_result[0] + exec_result[0] + liftings_result[0]  - random.randint(0,5)
                        country_scores.append(round(TES,2))
                        #Calcula PCS
                        PCS = cor_result[0] + int_result[0] + sync_result[0] - random.randint(0,5)
                        country_scores.append(round(PCS,2))
                        country_scores.append(round(pen_result[0],2))
                        #Puntaje final
                        final_score = PCS + TES - pen_result[0]
                        if final_score <= 0: final_score = 0.0
                        results = (r[0] ,r[1] , [country_scores ,round(final_score, 2)])
                        self.table_results.append(results)
                    pass
                pass
                
            elif self.sport.team_sport_name == 'Esqui Nordico':
                final_score = 0
                country_scores = []
                specific_rules = rules['scoring_rules']
                if 'Trampolín' in self.deporte.sp_record_name:
                    #Primera parte
                    base_points = specific_rules['variables']['BP']['range']
                    if 'normal' in self.deporte.sp_record_name:
                        k_value = specific_rules['variables']['K']['values']['normal_hill']
                    else:
                        k_value = specific_rules['variables']['K']['values']['large_hill']
                    distance_meters = specific_rules['variables']['MV']['range']

                    #Segunda parte
                    style_points = specific_rules['variables']['SP']['range']
                    wind_comp = specific_rules['variables']['WC']['range']
                    ground_comp = specific_rules['variables']['GC']['range']
                    penalty_range = specific_rules['variables']['P']['range']
                    if 'individual' in self.deporte.sp_record_name:
                        self.nombres = ['Ronda ' +str(i) for i in range(2)]
                    else:
                        self.nombres = ['Puntaje ' +str(i) for i in range(4)]
                    for r in self.ranks:
                        final_score = 0
                        country_scores = []
                        for _ in range(len(self.nombres)):                    
                            #Simula puntos base
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(base_points[1]), float(base_points[0]), 'T', self.sport.team_sport_name)
                            base_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula valor k
                            k_result = float(k_value)
                            #Simula metros
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(distance_meters[1]), float(distance_meters[0]), 'T', self.sport.team_sport_name)
                            meters_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula puntos de estilo
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(style_points[1]), float(style_points[0]), 'T', self.sport.team_sport_name)
                            style_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula viento
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(wind_comp[1]), float(wind_comp[0]), 'T', self.sport.team_sport_name)
                            wind_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula compensación
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(ground_comp[1]), float(ground_comp[0]), 'T', self.sport.team_sport_name)
                            comp_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Simula penalizacion
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                            pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                            #Puntaje final
                            dp_value = base_result[0] + (k_result + meters_result[0])
                            final_score = dp_value + style_result[0] + wind_result[0] + comp_result[0] - pen_result[0] - random.randint(0,5)
                            country_scores.append(round(final_score,2))
                            

                        results = (r[0] ,r[1] , [country_scores ,round(sum(country_scores), 2)])
                        self.table_results.append(results)
               
                    pass
                elif 'TN' in self.deporte.sp_record_name or 'TG' in self.deporte.sp_record_name:
                    #Primera parte
                    base_points = specific_rules['variables']['BP']['range']
                    if 'TN' in self.deporte.sp_record_name:
                        k_value = specific_rules['variables']['K']['values']['normal_hill']
                    else:
                        k_value = specific_rules['variables']['K']['values']['large_hill']
                    distance_meters = specific_rules['variables']['MV']['range']

                    #Segunda parte
                    style_points = specific_rules['variables']['SP']['range']
                    wind_comp = specific_rules['variables']['WC']['range']
                    ground_comp = specific_rules['variables']['GC']['range']
                    penalty_range = specific_rules['variables']['P']['range']
                    self.nombres = ['Puntaje Salto', 'Tiempo Sprint']
                    for r in self.ranks:
                        final_score = 0
                        country_scores = []               
                        #Simula puntos base
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(base_points[1]), float(base_points[0]), 'T', self.sport.team_sport_name)
                        base_result = olympic_sim.select_type_game(r[1], 1, 0)
                        #Simula valor k
                        k_result = float(k_value)
                        #Simula metros
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(distance_meters[1]), float(distance_meters[0]), 'T', self.sport.team_sport_name)
                        meters_result = olympic_sim.select_type_game(r[1], 1, 0)
                        #Simula puntos de estilo
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(style_points[1]), float(style_points[0]), 'T', self.sport.team_sport_name)
                        style_result = olympic_sim.select_type_game(r[1], 1, 0)
                        #Simula viento
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(wind_comp[1]), float(wind_comp[0]), 'T', self.sport.team_sport_name)
                        wind_result = olympic_sim.select_type_game(r[1], 1, 0)
                        #Simula compensación
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(ground_comp[1]), float(ground_comp[0]), 'T', self.sport.team_sport_name)
                        comp_result = olympic_sim.select_type_game(r[1], 1, 0)
                        #Simula penalizacion
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(penalty_range[0]), float(penalty_range[1]), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        #Puntaje final
                        dp_value = base_result[0] + (k_result + meters_result[0])
                        final_score = dp_value + style_result[0] + wind_result[0] + comp_result[0] - pen_result[0] - random.randint(0,5)

                        if 'TN' in self.deporte.sp_record_name:
                            country_scores.append(round(405 - final_score,2))
                        else:
                            country_scores.append(round(460 - final_score,2))

                        #Segundo puntaje
                        if '10km' in self.deporte.sp_record_name:
                            current_sport = Sportsrecords.objects.get(sp_record_name__contains = 'Esquí de fondo 10km', team_sport = self.sport.team_sport_id)
                        elif '4x5km' in self.deporte.sp_record_name:
                            current_sport = Sportsrecords.objects.get(sp_record_name__contains = 'Esquí de fondo 4x5km', team_sport = self.sport.team_sport_id)
                        
                        best_possible = current_sport.sp_record_best
                        last_possible = current_sport.sp_record_last
                        olympic_sim = sports_by_individual.SportsByIndividual(current_sport.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        sprint_result = olympic_sim.select_type_game(r[1], 1, 0)
                        country_scores.append(round(sprint_result[0],2))

                        results = (r[0] ,r[1] , [country_scores ,round(sum(country_scores), 2)])
                        self.table_results.append(results)
                    pass
                pass

            elif self.sport.team_sport_name == 'Ciclismo de Pista':
                if 'Madison' in self.deporte.sp_record_name:
                    final_score = 0
                    country_scores = []
                    self.nombres = ['Check '+str(i) for i in range(20)]
                    current_results = []
                    best_possible = self.deporte.sp_record_best
                    last_possible = self.deporte.sp_record_last
                    country_points_list = []

                    for r in self.ranks:
                        country_points_list.append([r[0],r[1],[]])
                    
                    for _ in range(len(self.nombres)):
                        current_results = []
                        for r in self.ranks:
                            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                            sprint_res = olympic_sim.select_type_game(r[1], 1, 0)
                            sprint_results = (r[0] ,r[1] , sprint_res[0])
                            current_results.append(sprint_results)
                        
                        sorted_results = sorted(current_results, key=lambda x: x[2])

                        first_four = sorted_results[:4]
                        
                        for c in country_points_list:
                            if first_four[0][0] == c[0]:
                                c[2].append(5)
                            elif first_four[1][0] == c[0]:
                                c[2].append(3)
                            elif first_four[2][0] == c[0]:
                                c[2].append(2)
                            elif first_four[3][0] == c[0]:
                                c[2].append(1)
                            else:
                                c[2].append(0)
                                                         
                    for k in country_points_list:
                        results = (k[0] ,k[1] , [k[2] ,round(sum(k[2]), 2)])
                        self.table_results.append(results)
                    pass
                elif 'Ómnium' in self.deporte.sp_record_name:
                    final_score = 0
                    country_scores = []
                    self.nombres = ['Keirin','Velocidad','Puntos','Eliminación']
                    current_results = []
                    best_possible = self.deporte.sp_record_best
                    last_possible = self.deporte.sp_record_last
                    country_points_list = []

                    for r in self.ranks:
                        country_points_list.append([r[0],r[1],[]])
                          
                    
                    for n in self.nombres:
                        current_sport = None
                        current_results = []
                        if n == 'Keirin':
                            if 'masculino' in self.deporte.sp_record_name:
                                current_sport = Sportsrecords.objects.get(sp_record_name = 'Keirin masculino', team_sport = self.sport.team_sport_id)
                            else:
                                current_sport = Sportsrecords.objects.get(sp_record_name = 'Keirin femenino', team_sport = self.sport.team_sport_id)
                        elif n == 'Velocidad' or n == 'Eliminación':
                            if 'masculino' in self.deporte.sp_record_name:
                                current_sport = Sportsrecords.objects.get(sp_record_name = 'Velocidad masculino', team_sport = self.sport.team_sport_id)
                            else:
                                current_sport = Sportsrecords.objects.get(sp_record_name = 'Velocidad femenino', team_sport = self.sport.team_sport_id)
                        if current_sport != None:
                            best_possible = current_sport.sp_record_best
                            last_possible = current_sport.sp_record_last
                            olympic_sim = sports_by_individual.SportsByIndividual(current_sport.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        else:
                            best_possible = 50.0
                            last_possible = 0.0
                            olympic_sim = sports_by_individual.SportsByIndividual('Ciclismo Pista Puntos', float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        for r in self.ranks:  
                            sprint_res = olympic_sim.select_type_game(r[1], 1, 0)
                            sprint_results = (r[0] ,r[1] , sprint_res[0])
                            current_results.append(sprint_results)
                        
                        if best_possible < last_possible:
                            sorted_results = sorted(current_results, key=lambda x: x[2])
                        else:
                            sorted_results = sorted(current_results, key=lambda x: x[2], reverse=True)

                        actual_points = 40
                        for s in sorted_results:
                            for c in country_points_list:
                                if c[0] == s[0]:
                                    c[2].append(actual_points)
                                    if actual_points > 0: actual_points -= 2
                                                                               
                    for k in country_points_list:
                        results = (k[0] ,k[1] , [k[2] ,round(sum(k[2]), 2)])
                        self.table_results.append(results)
                    pass
                pass
                
            elif self.sport.team_sport_name == 'Ciclismo Urbano':
                best_possible = self.deporte.sp_record_best
                last_possible = self.deporte.sp_record_last
                self.nombres = ['Ronda '+str(i) for i in range(2)]
                for r in self.ranks:
                    country_scores = []
                    for _ in range(len(self.nombres)):
                        final_score = 0 
                        #Simula Dificultad
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        dif_result = olympic_sim.select_type_game(r[1], 1, 0)    
                        #Simula Ejecución
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        exec_result = olympic_sim.select_type_game(r[1], 1, 0)
                        #Simula amplitud    
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        amp_result = olympic_sim.select_type_game(r[1], 1, 0)
                        #Simula flow    
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        flow_result = olympic_sim.select_type_game(r[1], 1, 0)    
                        #Simula Creatividad
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(best_possible), float(last_possible), 'T', self.sport.team_sport_name)
                        cre_result = olympic_sim.select_type_game(r[1], 1, 0)
                        #Simula Penalización
                        olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(0.0), float(20.0), 'T', self.sport.team_sport_name)
                        pen_result = olympic_sim.select_type_game(r[1], 1, 0)
                        #Puntaje final
                        final_score = (dif_result[0]*0.3)+(exec_result[0]*0.25)+(amp_result[0]*0.2)+(flow_result[0]*0.15)+(cre_result[0]*0.1)-(pen_result[0]) - random.randint(0,5)
                        if final_score <= 0: final_score = 0.0 
                        country_scores.append(round(final_score,2))
                    results = (r[0] ,r[1] , [country_scores ,round(max(country_scores), 2)])
                    self.table_results.append(results)

        else:
            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(self.deporte.sp_record_best), float(self.deporte.sp_record_last), self.deporte.sport_class, self.sport.team_sport_name)
            for r in self.ranks:
                results = (r[0] ,r[1] ,olympic_sim.select_type_game(r[1], 1, 0))
                self.table_results.append(results)


        if float(self.deporte.sp_record_best) < float(self.deporte.sp_record_last):
            if 'Madison' in self.deporte.sp_record_name:
                try:
                    self.table_results = sorted(self.table_results, key=lambda x: x[2][1], reverse=True)
                except:
                    self.table_results = sorted(self.table_results, key=lambda x: x[2], reverse = True)
            else:
                try:
                    self.table_results = sorted(self.table_results, key=lambda x: x[2][1])
                except:
                    self.table_results = sorted(self.table_results, key=lambda x: x[2]) 

        elif float(self.deporte.sp_record_best) > float(self.deporte.sp_record_last):
            try:
                self.table_results = sorted(self.table_results, key=lambda x: x[2][1], reverse=True)
            except:
                self.table_results = sorted(self.table_results, key=lambda x: x[2], reverse=True)
        elif float(self.deporte.sp_record_best) == float(self.deporte.sp_record_last):
            if 'obstáculos' in self.deporte.sp_record_name: 
                try: 
                    self.table_results = sorted(self.table_results, key=lambda x: x[2][1])
                except:
                    self.table_results = sorted(self.table_results, key=lambda x: x[2])
            else:
                try: 
                    self.table_results = sorted(self.table_results, key=lambda x: x[2][1], reverse=True)
                except:
                    self.table_results = sorted(self.table_results, key=lambda x: x[2], reverse=True)
            
            if 'TN +' in self.deporte.sp_record_name or 'TG +' in self.deporte.sp_record_name:
                try: 
                    self.table_results = sorted(self.table_results, key=lambda x: x[2][1])
                except:
                    self.table_results = sorted(self.table_results, key=lambda x: x[2])



    def get_table_results(self):
        return self.table_results

    def get_nombres(self):
        return self.nombres
    
    def get_heats(self):
        return self.num_heats
    


