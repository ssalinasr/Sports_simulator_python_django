from appolympics.models import Teamregion, Nationalteams, Olympicplayers, Teamsports, Clubleague, Clubs, Playercountry, Playertournamentsports, Teamranks, Sportsrecords, Clubmatchesregister, Teamtournamentregister
from appolympics.models import Teammatchesregister, Teamtitleregister, Playertitleregister, Clubtitleregister, Playertournamentregister, Clubtournamentregister
from core_scripts.interfaces.olympic_sports_interfaces import sports_by_heats, sports_by_individual, sports_by_rounds, sports_by_elimination
import itertools, random

class SimulatedSports():
    def __init__(self, sport, deporte, table_results, ranks):
        self.sport = sport
        self.deporte = deporte
        self.table_results = table_results
        self.ranks = ranks
        self.nombres = []
        self.num_heats = 0
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
                results = (r[0] ,r[1] ,olympic_sim.select_type_game(r[1], 1, 0))
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
            rules = dict(self.sport.team_sport_rules)

            if 'Heptatlón' in self.deporte.sp_record_name:
                current_rules = rules['disciplines']['heptathlon'] 
                print(current_rules.keys())
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
                        elif current_sport.sport.sport_class == 'R':
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
                print(current_rules.keys())
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
                        final_score = dif_result[0] + (time_result[0] + hor_result[0] + exec_result[0] + sync_result) - pen_result[0]
                    else:
                        #Puntaje final
                        final_score = dif_result[0] + (time_result[0] + hor_result[0] + exec_result[0]) - pen_result[0]

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
                            final_score = (dif_result[0]*0.35) + (exec_result[0]*0.25) + (art_result[0]*0.3) + (sync_result[0]*0.1) - pen_result[0]
                        elif 'técnica' in self.deporte.sp_record_name:
                            final_score = (dif_result[0]*0.4) + (exec_result[0]*0.35) + (art_result[0]*0.15) + (sync_result[0]*0.1) - pen_result[0]
                        elif 'acrobática' in self.deporte.sp_record_name:
                            final_score = (dif_result[0]*0.45) + (exec_result[0]*0.2) + (art_result[0]*0.2) + (sync_result[0]*0.15) - pen_result[0]
                    else:
                        #Puntaje final
                        if 'libre' in self.deporte.sp_record_name:
                            final_score = (dif_result[0]*0.4) + (exec_result[0]*0.3) + (art_result[0]*0.3) - pen_result[0]
                        elif 'técnica' in self.deporte.sp_record_name:
                            final_score = (dif_result[0]*0.4) + (exec_result[0]*0.4) + (art_result[0]*0.2) - pen_result[0]
                        elif 'acrobática' in self.deporte.sp_record_name:
                            final_score = (dif_result[0]*0.45) + (exec_result[0]*0.28) + (art_result[0]*0.27) - pen_result[0]

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
                            final_score = (dif_result[0]*0.25)+(exec_result[0]*0.25)+(amp_result[0]*0.15)+(flow_result[0]*0.15)+(var_result[0]*0.1)+(og_result[0]*0.05)+(cons_result[0]*0.05)-(pen_result[0])
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
                            final_score = (dif_result[0]*0.2)+(exec_result[0]*0.3)+(flow_result[0]*0.25)+(var_result[0]*0.15)+(use_result[0]*0.1)-(pen_result[0])
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
                            final_score = (dif_result[0]*0.2)+(exec_result[0]*0.3)+(flow_result[0]*0.25)+(var_result[0]*0.15)+(use_result[0]*0.1)-(pen_result[0])
                            if final_score <= 0: final_score = 0.0 
                            tricks_scores.append(round(final_score,2))
                        trick_results = sorted(tricks_scores, reverse=True)[:2]
                        all_results = country_scores + tricks_scores
                        full_scores = []
                        full_scores.append(round_result)
                        full_scores.extend(trick_results)
                        print('Rondas ', country_scores, 'Tricks ', trick_results)
                        print('Resultados ', full_scores)
                        print(all_results)
                        results = (r[0] ,r[1] , [all_results ,round(sum(full_scores), 2)])
                        self.table_results.append(results)
                    pass
                pass

            elif self.sport.team_sport_name == 'Vela':
                
                pass

            elif self.sport.team_sport_name == 'Biatlon':
                pass

            elif self.sport.team_sport_name == 'Esqui Acrobatico':
                pass

            elif self.sport.team_sport_name == 'Snowboard Acrobatico':
                pass

            elif self.sport.team_sport_name == 'Patinaje Artistico sobre Hielo':
                pass
                
            elif self.sport.team_sport_name == 'Esqui Nordico':
                pass

            elif self.sport.team_sport_name == 'Ciclismo de Ruta':
                pass

        else:
            olympic_sim = sports_by_individual.SportsByIndividual(self.deporte.sp_record_name, float(self.deporte.sp_record_best), float(self.deporte.sp_record_last), self.deporte.sport_class, self.sport.team_sport_name)
            for r in self.ranks:
                results = (r[0] ,r[1] ,olympic_sim.select_type_game(r[1], 1, 0))
                self.table_results.append(results)

        print(self.deporte.sp_record_best, self.deporte.sp_record_last)

        if float(self.deporte.sp_record_best) < float(self.deporte.sp_record_last):
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



    def get_table_results(self):
        return self.table_results

    def get_nombres(self):
        return self.nombres
    
    def get_heats(self):
        return self.num_heats
    


