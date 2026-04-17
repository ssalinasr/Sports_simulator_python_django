from appolympics.models import Clubs, Clubleague
from core_scripts.leagues import league_group

class ClubLeagueSeason:
    def __init__(self, teams_tuple, country, has_promotion, year, promotions, qualifiers, region, has_save, ranks):
        self.teams_tuple = teams_tuple
        self.country = country
        self.has_promotion = has_promotion
        self.year = year
        self.has_save = has_save
        self.ranks = ranks
        self.promotions = promotions
        self.qualifiers = qualifiers
        self.region = region
        self.first_cup_qualified = []
        self.first_cup_prev_qualified = []
        self.second_cup_qualified = []
        self.second_cup_prev_qualified = []
        self.third_cup_qualified = []
        self.third_cup_prev_qualified = []
        self.promoted_teams = []
        self.relegated_teams = []
        self.general_matches = []
        self.general_tables = []


    def simulate_league(self):
        groups = league_group.Group(self.teams_tuple[2], self.teams_tuple[0], True, 'Futbol Masculino', 3, self.ranks)  
        groups.generate_calendar()
        groups.simulate_league()
        table = groups.get_league_table()
        matches = groups.get_league_matches()
        
        table_names = []
        table_values = []

        for k in table.items():
            table_names.append(k[0])
            table_values.append(k[1])

        table_dict = dict(zip(table_names, table_values))
        sorted_table = sorted(
            table_dict.items(),
            key= lambda item:(
                item[1]['pts'],
                item[1]['gd'],
                item[1]['gf']
            ),
            reverse=True
        )
    
        self.general_matches.append(matches)
        self.general_tables.append(sorted_table)

        if self.teams_tuple[3] == '1D':
            if self.has_promotion:
                self.relegated_teams.append(groups.get_qualified_reversed_teams(self.promotions))
            else:
                pass

            if self.teams_tuple[7] == 'Y':
                self.first_cup_qualified.append(groups.get_qualified_specified_teams(0, self.qualifiers[0]))
                self.second_cup_qualified.append(groups.get_qualified_specified_teams(self.qualifiers[0], self.qualifiers[0]+self.qualifiers[1]))
                self.third_cup_qualified.append(groups.get_qualified_specified_teams(self.qualifiers[0]+self.qualifiers[1], self.qualifiers[0]+self.qualifiers[1]+self.qualifiers[2]))
            else:
                self.first_cup_prev_qualified.append(groups.get_qualified_specified_teams(0, self.qualifiers[0]))
                self.second_cup_prev_qualified.append(groups.get_qualified_specified_teams(self.qualifiers[0], self.qualifiers[0]+self.qualifiers[1]))
                self.third_cup_prev_qualified.append(groups.get_qualified_specified_teams(self.qualifiers[0]+self.qualifiers[1], self.qualifiers[0]+self.qualifiers[1]+self.qualifiers[2]))
        elif self.teams_tuple[3] == '2D':
            self.promoted_teams.append(groups.get_qualified_specified_teams(0, self.promotions))

    def update_promotions_relegations(self):
        pass

    def get_full_results(self):
        first_cup = self.get_first_cup_qualified_teams()
        first_cup_prev = self.get_first_cup_prev_qualified_teams()
        second_cup = self.get_second_cup_qualified_teams()
        second_cup_prev = self.get_second_cup_prev_qualified_teams()
        third_cup = self.get_third_cup_qualified_teams()
        third_cup_prev = self.get_third_cup_prev_qualified_teams()
        return ([first_cup, second_cup, third_cup, first_cup_prev, second_cup_prev, third_cup_prev], self.region)

    def get_first_cup_qualified_teams(self):
        return self.first_cup_qualified
    
    def get_second_cup_qualified_teams(self):
        return self.second_cup_qualified
    
    def get_third_cup_qualified_teams(self):
        return self.third_cup_qualified
    
    def get_first_cup_prev_qualified_teams(self):
        return self.first_cup_prev_qualified
    
    def get_second_cup_prev_qualified_teams(self):
        return self.second_cup_prev_qualified
    
    def get_third_cup_prev_qualified_teams(self):
        return self.third_cup_prev_qualified
    

    

