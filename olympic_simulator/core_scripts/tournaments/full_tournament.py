from core_scripts.leagues import league_group
from core_scripts.tournaments import tournament_group
from core_scripts.leagues import league_tools
import random
import itertools
from collections import defaultdict

from openpyxl import Workbook
from openpyxl.styles import Font
from django.http import HttpResponse



class FullTournament():

    def __init__(self, teams, divisions, ranks, sport, num_groups, match_class, year):
        self.teams = teams
        self.divisions = divisions
        self.ranks = ranks
        self.sport = sport
        self.match_class = match_class
        self.year = year
        self.prev_stages = []
        self.prev_stages_tables = []
        self.prev_stages_matches = []
        self.qualified_teams = []
        self.group_finals = []
        self.group_finals_tables = []
        self.group_finals_matches = []
        self.world_groups = []
        self.world_groups_tables = []
        self.world_groups_matches = []
        self.final = []
        self.final_table = {}
        self.final_matches = []
        self.element_names = []
        self.num_groups = num_groups
        self.general_tables = []
        self.general_matches = []

    def subdivide_groups(self, num_groups, teams):
        random.shuffle(teams)
        base_length = len(teams) // num_groups
        remainder = len(teams) % num_groups

        sorted_teams = []
        index = 0

        for i in range(num_groups):
            length = base_length + 1 if i < remainder else base_length
            sorted_teams.append(teams[index:index+length])
            index += length
        
        return sorted_teams

    def simulate_tournament(self):
        if isinstance(self.divisions, list): # Simula torneos de deportes entre paises #
            region_sublist = ['Africa', 'Asia_Oceania', 'America', 'Europa']
            #Genera los grupos de la fase previa#
            for div in range(len(self.divisions)):
                self.prev_stages.append(self.subdivide_groups(self.num_groups, self.teams[div]))
            counter = 0
            #Simula los grupos de la fase previa#
            for stage_group in self.prev_stages:
                index = 1
                temp_list_of_tables = []
                temp_list_of_matches = []
                temp_qualified_teams = []
                for k in stage_group:
                    group = league_group.Group('Grupo '+str(index)+' '+str(region_sublist[counter]), k, True, self.sport, self.match_class, self.ranks)
                    index += 1
                    
                    group.generate_calendar()
                    group.simulate_league()
                    self.element_names.append(group.get_group_name())
                    table = group.get_league_table()

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
                    temp_list_of_tables.append(sorted_table)
                    self.general_tables.append(sorted_table)
                    self.general_matches.append(group.get_league_matches())
                    temp_list_of_matches.append(group.get_league_matches())
                    temp_qualified_teams.append(group.get_qualified_teams(2))
                self.prev_stages_tables.append(temp_list_of_tables)
                self.prev_stages_matches.append(temp_list_of_matches)
                self.qualified_teams.append(temp_qualified_teams)
                counter += 1
                

            temp_list = []
            for qual_subgroup in self.qualified_teams:
                merged_list = list(itertools.chain.from_iterable(qual_subgroup))
                temp_list.append(merged_list)
            self.qualified_teams = temp_list
            
            index = 0
            self.group_finals = self.qualified_teams
            self.qualified_teams = []
            #Simula los torneos continentales
            for sub_qual in self.group_finals:
                tournament = tournament_group.Tournament('Copa de '+region_sublist[index]+' '+str(self.year), self.sport, sub_qual, self.ranks, False, True, self.match_class)
                trn_result = tournament.simulate_tournament()
                table = tournament.get_tournament_table()
                matches = tournament.get_tournament_matches()
                self.general_matches.append(tournament.get_tournament_matches())
                index += 1
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
                tournament.generate_tournament_bracket(trn_result['bracket'])
                self.group_finals_tables.append(sorted_table)
                self.general_tables.append(sorted_table)
                self.group_finals_matches.append(matches)
                self.element_names.append(trn_result['tournament_name'])
                self.qualified_teams.append(tournament.get_qualified_teams(8))
            merged_list = list(itertools.chain.from_iterable(self.qualified_teams))
            self.qualified_teams = merged_list
            self.world_groups = self.subdivide_groups(8, self.qualified_teams)
            #Simula la fase de grupos mundial
            index = 1
            self.qualified_teams = []
            for w_groups in self.world_groups:
                group = league_group.Group('Grupo '+str(index)+' Mundial', w_groups, True, self.sport, self.match_class, self.ranks)
                index += 1
                group.generate_calendar()
                group.simulate_league()
                self.element_names.append(group.get_group_name())
                table = group.get_league_table()
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
                self.general_tables.append(sorted_table)
                self.world_groups_tables.append(sorted_table)
                self.world_groups_matches.append(group.get_league_matches())
                self.general_matches.append(group.get_league_matches())
                self.qualified_teams.append(group.get_qualified_teams(2))
            merged_list = list(itertools.chain.from_iterable(self.qualified_teams))
            self.qualified_teams = merged_list
            #Simula la fase final mundial
            tournament = tournament_group.Tournament('Final '+self.sport+' '+str(self.year), self.sport, self.qualified_teams, self.ranks, False, True, self.match_class)
            trn_result = tournament.simulate_tournament()
            table = tournament.get_tournament_table()
            matches = tournament.get_tournament_matches()
            self.element_names.append(trn_result['tournament_name'])
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

            tournament.generate_tournament_bracket(trn_result['bracket'])

            self.final_table = sorted_table
            self.general_tables.append(sorted_table)
            self.final_matches.append(matches)
            self.general_matches.append(matches)
            '''
            merged_list = list(itertools.chain.from_iterable(self.general_matches))
            ultra_merged = list(itertools.chain.from_iterable(merged_list))
            self.general_matches = ultra_merged

            matches_dict = [
                dict(zip(["team1","score1","team2","score2"], m))
                for m in self.general_matches
            ]
            self.general_matches = matches_dict
            '''
        else:
            if "MK" not in self.sport and "GE" in self.sport: # Simula torneos de Goldeneye #
                group_teams_sublist = []
                single_sublist = []
                for temp in self.teams:
                    if '/' in temp and 'GE' not in temp:
                        group_teams_sublist.append(temp)
                    elif 'GE' not in temp:
                        single_sublist.append(temp)
                #Individual
                if self.sport != 'GE-Teams':
                    self.prev_stages = self.subdivide_groups(self.num_groups, single_sublist)
                else:
                    self.prev_stages = self.subdivide_groups(self.num_groups, group_teams_sublist)
                print(self.prev_stages)
                #Simula los grupos de la fase previa#
                index = 1
                for stage_group in self.prev_stages:
                    group = league_group.Group('Grupo '+str(index), stage_group, True, self.sport, self.match_class, self.ranks)
                    index += 1
                    group.generate_calendar()
                    group.simulate_league()
                    self.element_names.append(group.get_group_name())
                    table = group.get_league_table()

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
                    self.general_tables.append(sorted_table)
                    self.general_matches.append(group.get_league_matches())
                    self.prev_stages_tables.append(sorted_table)
                    self.prev_stages_matches.append(group.get_league_matches())
                    self.qualified_teams.append(group.get_qualified_teams(4))

                merged_list = list(itertools.chain.from_iterable(self.qualified_teams))
                self.qualified_teams = merged_list
                print(self.qualified_teams)
                #Simula la fase final mundial
                tournament = tournament_group.Tournament('Final '+self.sport+'_'+str(self.year), self.sport, self.qualified_teams, self.ranks, False, True, self.match_class)
                trn_result = tournament.simulate_tournament()
                table = tournament.get_tournament_table()
                matches = tournament.get_tournament_matches()
                self.element_names.append(trn_result['tournament_name'])
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

                tournament.generate_tournament_bracket(trn_result['bracket'])

                self.final_table = sorted_table
                self.general_tables.append(sorted_table)
                self.final_matches.append(matches)
                self.general_matches.append(matches)

            elif "MK" not in self.sport and "SSB" in self.sport: #Simula Torneos de Super Smash#
                group_teams_sublist = []
                single_sublist = []
                for temp in self.teams:
                    if '/' in temp:
                        group_teams_sublist.append(temp)
                    else:
                        single_sublist.append(temp)
                #Individual
                self.teams = single_sublist
                self.prev_stages = self.subdivide_groups(self.num_groups, self.teams)
                print(self.prev_stages)
                #Simula los grupos de la fase previa#
                index = 1
                for stage_group in self.prev_stages:
                    group = league_group.Group('Grupo '+str(index), stage_group, True, self.sport, self.match_class, self.ranks)
                    index += 1
                    group.generate_calendar()
                    group.simulate_league()
                    self.element_names.append(group.get_group_name())
                    table = group.get_league_table()

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
                    self.general_tables.append(sorted_table)
                    self.general_matches.append(group.get_league_matches())
                    self.prev_stages_tables.append(sorted_table)
                    self.prev_stages_matches.append(group.get_league_matches())
                    self.qualified_teams.append(group.get_qualified_teams(1))

                merged_list = list(itertools.chain.from_iterable(self.qualified_teams))
                self.qualified_teams = merged_list
                print('Clasificados Individual')
                print(self.qualified_teams)
                #Simula la fase final mundial
                tournament = tournament_group.Tournament('Final '+self.sport+'_'+str(self.year), self.sport, self.qualified_teams, self.ranks, False, True, self.match_class)
                trn_result = tournament.simulate_tournament()
                table = tournament.get_tournament_table()
                matches = tournament.get_tournament_matches()
                self.element_names.append(trn_result['tournament_name'])
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

                tournament.generate_tournament_bracket(trn_result['bracket'])

                self.final_table = sorted_table
                self.general_tables.append(sorted_table)
                self.final_matches.append(matches)
                self.general_matches.append(matches) 

                #Equipos
                self.prev_stages_tables = []
                self.prev_stages_matches = []
                self.qualified_teams = []
                self.final_table = {}
                self.final_matches= []
                self.teams = group_teams_sublist
                self.num_groups = 2
                self.prev_stages = self.subdivide_groups(self.num_groups, self.teams)
                print(self.prev_stages)

                #Simula los grupos de la fase previa#
                index = 1
                print(index)
                for stage_group in self.prev_stages:
                    group = league_group.Group('Grupo '+str(index), stage_group, True, self.sport, self.match_class, self.ranks)
                    index += 1
                    group.generate_calendar()
                    group.simulate_league()
                    self.element_names.append(group.get_group_name())
                    table = group.get_league_table()

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
                    self.general_tables.append(sorted_table)
                    self.general_matches.append(group.get_league_matches())
                    self.prev_stages_tables.append(sorted_table)
                    self.prev_stages_matches.append(group.get_league_matches())
                    self.qualified_teams.append(group.get_qualified_teams(4))

                merged_list = list(itertools.chain.from_iterable(self.qualified_teams))
                self.qualified_teams = merged_list
                print('Clasificados equipos')
                print(self.qualified_teams)
                #Simula la fase final mundial
                tournament = tournament_group.Tournament('Final EQ '+self.sport+'_'+str(self.year), self.sport, self.qualified_teams, self.ranks, False, True, self.match_class)
                trn_result = tournament.simulate_tournament()
                table = tournament.get_tournament_table()
                matches = tournament.get_tournament_matches()
                self.element_names.append(trn_result['tournament_name'])
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

                tournament.generate_tournament_bracket(trn_result['bracket'])

                self.final_table = sorted_table
                self.general_tables.append(sorted_table)
                self.final_matches.append(matches)
                self.general_matches.append(matches)             
            else: # Simula torneos de Mario Kart y Muñecos #
                print(self.teams)
                #Simula la fase final mundial
                tournament = tournament_group.Tournament('Final '+self.sport+'_'+str(self.year), self.sport, self.teams, self.ranks, False, True, self.match_class)
                trn_result = tournament.simulate_tournament()
                table = tournament.get_tournament_table()
                matches = tournament.get_tournament_matches()
                self.element_names.append(trn_result['tournament_name'])
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

                tournament.generate_tournament_bracket(trn_result['bracket'])

                self.final_table = sorted_table
                self.general_tables.append(sorted_table)
                self.final_matches.append(matches)
                self.general_matches.append(matches)   


            


        pass

    def generate_tournament_excel(self, file_path="tournament_simulation.xlsx"):

        wb = Workbook()
        wb.remove(wb.active)

        for i in range(len(self.element_names)):

            sheet_name = self.element_names[i][:31]  # Excel limite nombre hoja
            ws = wb.create_sheet(title=sheet_name)

            table = self.general_tables[i]
            matches = self.general_matches[i]

            # -------- TABLA --------
            ws["A1"] = "Tabla"
            ws["A1"].font = Font(bold=True)

            headers = ["Pos", "Team", "Pts", "W", "D", "L", "GF", "GC", "GD"]

            for col, header in enumerate(headers, start=1):
                ws.cell(row=2, column=col, value=header).font = Font(bold=True)

            row = 3
            pos = 1

            for team, stats in table:

                ws.cell(row=row, column=1, value=pos)
                ws.cell(row=row, column=2, value=team)
                ws.cell(row=row, column=3, value=stats["pts"])
                ws.cell(row=row, column=4, value=stats["w"])
                ws.cell(row=row, column=5, value=stats["d"])
                ws.cell(row=row, column=6, value=stats["l"])
                ws.cell(row=row, column=7, value=stats["gf"])
                ws.cell(row=row, column=8, value=stats["gc"])
                ws.cell(row=row, column=9, value=stats["gd"])

                row += 1
                pos += 1

            # -------- PARTIDOS --------
            start_row = row + 2

            ws.cell(row=start_row, column=1, value="Partidos").font = Font(bold=True)

            match_headers = ["Team 1", "Team 2", "Score 1", "Score 2"]

            for col, header in enumerate(match_headers, start=1):
                ws.cell(row=start_row + 1, column=col, value=header).font = Font(bold=True)

            r = start_row + 2
            if isinstance(matches, dict):
                matches = [matches]
            for match in matches:

                for col, key in enumerate(["team1","team2","score1","score2"], start=1):
                    ws.cell(row=r, column=col, value=match[key])

                r += 1

        wb.save(file_path)

        return file_path

    
