from collections import defaultdict
import itertools
from core_scripts.leagues import league_tools
from core_scripts.interfaces.games_interfaces import supersmash_interface, goldeneye_interface
from core_scripts.interfaces.sports_interfaces import sports_by_ends, sports_by_sets, sports_by_special_sets, sports_by_time, sports_by_timed_points

class Group():
    def __init__(self, group_name, teams, has_double_leg, sport_name, match_class, ranks):
        self.group_name = group_name
        self.teams = teams
        self.fixture = []
        self.has_double_leg = has_double_leg
        self.sport_name = sport_name
        self.ranks = ranks
        self.match_class = match_class
        self.matches = []
        self.table = defaultdict(lambda: {
            "pts":0,
            "w":0,
            "l":0,
            "d":0,
            "gf":0,
            "gc":0,
            "gd":0
        })

    def generate_calendar(self):
        tools = league_tools.LeagueTools(self.teams)
        first_leg = tools.round_robin_fixture()
        second_leg = []
        if self.has_double_leg: 
            second_leg = [
            [(away, local) for local, away in fixture]
            for fixture in first_leg
            ]

        self.fixture = first_leg + second_leg

    def simulate_league(self):

        if self.match_class in [1,5]:
            if self.sport_name in ['Futbol Masculino', 'Futbol Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 2, 45, False, False)

            elif self.sport_name in ['Basketball Masculino', 'Basketball Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 4, 200, False, False)

            elif self.sport_name in ['Balonmano Masculino', 'Balonmano Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 2, 30, False, False)

            elif self.sport_name in ['Rugby Masculino', 'Rugby Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 2, 40, False, False)

            elif self.sport_name in ['Futsal Masculino', 'Futsal Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 2, 20, False, False)

            elif self.sport_name in ['Hockey Masculino', 'Hockey Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 3, 20, False, False)

            elif self.sport_name in ['Volleyball Masculino', 'Volleyball Femenino']:
                sport_object = sports_by_sets.SetsSport(self.sport_name, 3, 25, 15, False, False)

            elif self.sport_name in ['Voley Playa Masculino', 'Voley Playa Femenino']:
                sport_object = sports_by_sets.SetsSport(self.sport_name, 3, 21, 15, False, False)

            elif self.sport_name in ['Squash Masculino', 'Squash Femenino']:
                sport_object = sports_by_sets.SetsSport(self.sport_name, 3, 11, 0, True, self.has_double_leg)

            elif self.sport_name in ['Tenis de Mesa Masculino', 'Tenis de Mesa Femenino']:
                sport_object = sports_by_sets.SetsSport(self.sport_name, 3, 11, 0, False, False)

            elif self.sport_name in ['Tenis Masculino', 'Tenis Femenino']:
                sport_object = sports_by_sets.SetsSport(self.sport_name, 3, 60, 0, False, False)

            elif self.sport_name in ['Badminton Masculino', 'Badminton Femenino']:
                sport_object = sports_by_sets.SetsSport(self.sport_name, 3, 21, 21, False, False)

            elif self.sport_name in ['Beisbol Masculino', 'Beisbol Femenino']:
                sport_object = sports_by_ends.EndsSport(self.sport_name, 9, False, False)

            elif self.sport_name in ['Tiro con Arco Masculino', 'Tiro con Arco Femenino']:
                sport_object = sports_by_special_sets.SpecialSetsSport(self.sport_name, 6, False, False)

            elif self.sport_name in ['Curling Masculino', 'Curling Femenino']:
                sport_object = sports_by_ends.EndsSport(self.sport_name, 10, False, False)

            elif self.sport_name in ['Esgrima Masculino', 'Esgrima Femenino']:
                sport_object = sports_by_timed_points.TimedPointsSport(self.sport_name, 3, 15, False, False)

        elif self.match_class == 3:
            if self.sport_name in ['Futbol Masculino', 'Futbol Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 2, 45, False, False) 

        elif self.match_class == 2:
            if self.sport_name == 'SSB-Time':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Tiempo', 3, 0)

            elif self.sport_name == 'SSB-Lives':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Vidas Reversa', 0, 5)

            elif self.sport_name == 'SSB-Coins':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Cumulativo', 3, 0)

            elif self.sport_name == 'SSB-Stamina':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Stamina', 0, 150)

            elif self.sport_name == 'SSB-Lightning':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Tiempo', 2, 0)

            elif self.sport_name == 'SSB-Single':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Tiempo', 3, 0)

            elif self.sport_name == 'SSB-Sudden':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Tiempo', 1, 0)

            elif self.sport_name == 'GE-Time':
                sport_object = goldeneye_interface.GoldeneyeInterface(self.sport_name ,'Tiempo', 3, 0)
            elif self.sport_name  == 'GE-Kills':
                sport_object = goldeneye_interface.GoldeneyeInterface(self.sport_name ,'Vidas', 0, 10)
            elif self.sport_name  == 'GE-SSDV':
                sport_object = goldeneye_interface.GoldeneyeInterface(self.sport_name ,'Vidas Reversa', 0, 2)
            elif self.sport_name  == 'GE-License to Kill':
                sport_object = goldeneye_interface.GoldeneyeInterface(self.sport_name ,'Vidas', 0, 20)
            elif self.sport_name  == 'GE-Teams':
                sport_object = goldeneye_interface.GoldeneyeInterface(self.sport_name ,'Vidas', 0, 15)
        
        tools = league_tools.LeagueTools(self.teams)
        matches_element = []

        for matchweek in self.fixture:
            for local, away in matchweek:
                if self.match_class in [1,3,5]:
                    sport_object.get_probability_list()
                    results = sport_object.simulate_match(tools.get_team_rank_by_list(local, self.ranks), tools.get_team_rank_by_list(away, self.ranks))
                    matches_element = [(local, results[0], away, results[1])]
                    self.matches.append(matches_element)
                    
                    self.table[local]["gf"] += results[0]
                    self.table[local]["gc"] += results[1]
                    self.table[away]["gf"] += results[1]
                    self.table[away]["gc"] += results[0]

                    if results[0] > results [1]:
                        self.table[local]["w"] += 1
                        self.table[local]["pts"] += 3
                        self.table[away]["l"] += 1
                    elif results[1] > results[0]:
                        self.table[away]["w"] += 1
                        self.table[away]["pts"] += 3
                        self.table[local]["l"] += 1
                    else:
                        self.table[local]["d"] += 1
                        self.table[away]["d"] += 1
                        self.table[local]["pts"] += 1
                        self.table[away]["pts"] += 1

                elif self.match_class == 2:
                    results = sport_object.simulate_game(sport_object.game_type)
                    matches_element = [(local, results[0], away, results[1])]
                    self.matches.append(matches_element)
                    self.table[local]["gf"] += results[0]
                    self.table[local]["gc"] += results[1]
                    self.table[away]["gf"] += results[1]
                    self.table[away]["gc"] += results[0]

                    if results[0] > results [1]:
                        self.table[local]["w"] += 1
                        self.table[local]["pts"] += 3
                        self.table[away]["l"] += 1
                    elif results[1] > results[0]:
                        self.table[away]["w"] += 1
                        self.table[away]["pts"] += 3
                        self.table[local]["l"] += 1
                    else:
                        self.table[local]["d"] += 1
                        self.table[away]["d"] += 1
                        self.table[local]["pts"] += 1
                        self.table[away]["pts"] += 1

            for team in self.teams:
                self.table[team]["gd"] = (
                    self.table[team]["gf"] - self.table[team]["gc"]
                )


        pass

    def get_qualified_teams(self, quantity):
        ordered = sorted(
            self.teams,
            key=lambda e:(
                self.table[e]["pts"],
                self.table[e]["gd"],
                self.table[e]["gf"]
            ),
            reverse=True
        )
        return ordered[:quantity]
    
    def get_league_table(self):
        return self.table
    
    def get_league_matches(self):
        if isinstance(self.matches[0], list):
            matches = list(itertools.chain.from_iterable(self.matches))
            matches_dict = [
            dict(zip(["team1","score1","team2","score2"], m))
            for m in matches
            ]
            return matches_dict
        else:
            matches = self.matches
            return matches


    
    def get_group_name(self):
        return self.group_name

