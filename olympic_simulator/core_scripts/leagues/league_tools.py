
class LeagueTools():
    def __init__(self, teams):
        self.teams = teams

    def round_robin_fixture(self):
        teams = self.teams[:]
        if len(teams)%2 != 0:
            teams.append('dummy')   
        n = len(teams)
        fixture = []
        for round in range(n-1):
            matchweek = []
            for i in range(n // 2):
                local = teams[i]
                away = teams[n - 1 - i]

                if local != 'dummy' and away != 'dummy':
                    matchweek.append((local, away))
            fixture.append(matchweek)
            #Rotate
            teams = [teams[0]] + [teams[-1]] + teams[1:-1]
        return fixture
    
    def subdivide_teams(self, num_groups=8):
        total = len(self.teams)
        base_length = total // num_groups
        remainder = total % num_groups

        groups = []
        index = 0
        
        for i in range(num_groups):
            length = base_length + 1 if i < remainder else base_length
            groups.append(self.teams[index:index+length])
            index += length

        return groups

    def get_team_rank_by_list(self, team_name, ranks):
        for r in ranks:
            if r[0] == team_name:
                return r[1]
        return 7        
