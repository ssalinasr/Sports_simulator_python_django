import random
import math
from collections import defaultdict
from core_scripts.interfaces.games_interfaces import supersmash_interface, goldeneye_interface, muns_interface, mariokart_interface
from core_scripts.interfaces.sports_interfaces import sports_by_ends, sports_by_sets, sports_by_special_sets, sports_by_time, sports_by_timed_points
from core_scripts.leagues import league_tools
from PIL import Image, ImageDraw, ImageFont
import itertools

class Tournament():
    def __init__(self, trn_name,sport_name ,teams, ranks, has_double_leg, has_third_place, match_class):
        self.trn_name = trn_name
        self.teams = teams
        self.has_double_leg = has_double_leg
        self.has_third_place = has_third_place
        self.match_class = match_class
        self.sport_name = sport_name
        self.matches = []
        self.ranks = ranks
        self.table = defaultdict(lambda: {
            "pts":0,
            "w":0,
            "l":0,
            "d":0,
            "gf":0,
            "gc":0,
            "gd":0
        })

    def round_name(self, n):
        names = {
            2:"Final",
            4:"Semifinal",
            8:"Cuartos de Final",
            16:"Octavos de Final",
            32:"16avos de Final",
            64:"32avos de Final"
        }

        return names.get(n, f"Ronda de {n}")

    def next_power_2(self, n):
        return 2 ** math.ceil(math.log2(n))

    def generate_bracket(self, teams):
        random.shuffle(teams)
        n=len(teams)
        bracket_size = self.next_power_2(n)
        byes = bracket_size - n
        teams.extend(["BYE"] * byes)
        return teams

    def simulate_tournament_match(self, local, away):
        winner = None
        if self.match_class in [1,3,5]:
            if self.sport_name in ['Futbol Masculino', 'Futbol Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 2, 45, True, self.has_double_leg)

            elif self.sport_name in ['Basketball Masculino', 'Basketball Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 4, 200, True, self.has_double_leg)

            elif self.sport_name in ['Balonmano Masculino', 'Balonmano Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 2, 30, True, self.has_double_leg)

            elif self.sport_name in ['Rugby Masculino', 'Rugby Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 2, 40, True, self.has_double_leg)

            elif self.sport_name in ['Futsal Masculino', 'Futsal Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 2, 20, True, self.has_double_leg)

            elif self.sport_name in ['Hockey Masculino', 'Hockey Femenino']:
                sport_object = sports_by_time.TimeSport(self.sport_name, 3, 20, True, self.has_double_leg)

            elif self.sport_name in ['Volleyball Masculino', 'Volleyball Femenino']:
                sport_object = sports_by_sets.SetsSport(self.sport_name, 3, 25, 15, True, self.has_double_leg)

            elif self.sport_name in ['Voley Playa Masculino', 'Voley Playa Femenino']:
                sport_object = sports_by_sets.SetsSport(self.sport_name, 3, 21, 15, True, self.has_double_leg)

            elif self.sport_name in ['Squash Masculino', 'Squash Femenino']:
                sport_object = sports_by_sets.SetsSport(self.sport_name, 3, 11, 0, True, self.has_double_leg)

            elif self.sport_name in ['Tenis de Mesa Masculino', 'Tenis de Mesa Femenino']:
                sport_object = sports_by_sets.SetsSport(self.sport_name, 3, 11, 0, True, self.has_double_leg)

            elif self.sport_name in ['Tenis Masculino', 'Tenis Femenino']:
                sport_object = sports_by_sets.SetsSport(self.sport_name, 3, 60, 0, True, self.has_double_leg)

            elif self.sport_name in ['Badminton Masculino', 'Badminton Femenino']:
                sport_object = sports_by_sets.SetsSport(self.sport_name, 3, 21, 21, True, self.has_double_leg)

            elif self.sport_name in ['Beisbol Masculino', 'Beisbol Femenino']:
                sport_object = sports_by_ends.EndsSport(self.sport_name, 9, True, self.has_double_leg)

            elif self.sport_name in ['Tiro con Arco Masculino', 'Tiro con Arco Femenino']:
                sport_object = sports_by_special_sets.SpecialSetsSport(self.sport_name, 6, True, self.has_double_leg)

            elif self.sport_name in ['Curling Masculino', 'Curling Femenino']:
                sport_object = sports_by_ends.EndsSport(self.sport_name, 10, True, self.has_double_leg)

            elif self.sport_name in ['Esgrima Masculino', 'Esgrima Femenino']:
                sport_object = sports_by_timed_points.TimedPointsSport(self.sport_name, 3, 15, True, self.has_double_leg)

            tools = league_tools.LeagueTools(self.teams)
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
                winner = local
                return winner, {
                "team1": local,
                "team2": away,
                "score1": results[0],
                "score2": results[1],
                "pen1": -1,
                "pen2": -1,
                "winner": winner
                }

            elif results[1] > results[0]:
                self.table[away]["w"] += 1
                self.table[away]["pts"] += 3
                self.table[local]["l"] += 1
                winner = away
                return winner, {
                "team1": local,
                "team2": away,
                "score1": results[0],
                "score2": results[1],
                "pen1": -1,
                "pen2": -1,
                "winner": winner
                }

            else:
                self.table[local]["d"] += 1
                self.table[away]["d"] += 1
                self.table[local]["pts"] += 1
                self.table[away]["pts"] += 1
                if results[2] > results[3]:
                    winner = local
                else:
                    winner = away
                return winner, {
                "team1": local,
                "team2": away,
                "score1": results[0],
                "score2": results[1],
                "pen1": results[2],
                "pen2": results[3],
                "winner": winner
                }


        elif self.match_class in [2,4]:
            if self.sport_name == 'GE-Time':
                sport_object = goldeneye_interface.GoldeneyeInterface(self.sport_name,'Tiempo', 3, 0)
                sport_class = 'tiempo'
            elif self.sport_name == 'GE-Kills':
                sport_object = goldeneye_interface.GoldeneyeInterface(self.sport_name,'Vidas', 0, 10)
                sport_class = 'sets'
            elif self.sport_name == 'GE-SSDV':
                sport_object = goldeneye_interface.GoldeneyeInterface(self.sport_name,'Vidas Reversa', 0, 2)
                sport_class = 'sets'
            elif self.sport_name == 'GE-License to Kill':
                sport_object = goldeneye_interface.GoldeneyeInterface(self.sport_name,'Vidas', 0, 20)
                sport_class = 'sets'
            elif self.sport_name == 'GE-Teams':
                sport_object = goldeneye_interface.GoldeneyeInterface(self.sport_name,'Vidas', 0, 15)
                sport_class = 'sets'
            elif self.sport_name == 'MK-Battles':
                sport_object = mariokart_interface.MarioKartInterface(self.sport_name,'Vidas Reversa', 0, 3)
                sport_class = 'sets'
            elif self.sport_name == 'SSB-Time':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Tiempo', 3, 0)
                sport_class = 'time'
            elif self.sport_name == 'SSB-Lives':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Vidas Reversa', 0, 5)
                sport_class = 'sets'
            elif self.sport_name == 'SSB-Coins':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Cumulativo', 3, 0)
                sport_class = 'time'
            elif self.sport_name == 'SSB-Stamina':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Stamina', 0, 150)
                sport_class = 'time'
            elif self.sport_name == 'SSB-Lightning':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Tiempo', 2, 0)
                sport_class = 'time'
            elif self.sport_name == 'SSB-Single':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Tiempo', 3, 0)
                sport_class = 'time'
            elif self.sport_name == 'SSB-Sudden':
                sport_object = supersmash_interface.SuperSmashInterface(self.sport_name, 'Tiempo', 1, 0)
                sport_class = 'time'
            
            elif self.sport_name in ['Futbol', 'Hockey en Piso']:
                sport_object = muns_interface.MunsInterface(self.sport_name, 'Tiempo', 2, 0)
            elif self.sport_name in 'Baloncesto':
                sport_object = muns_interface.MunsInterface(self.sport_name, 'Tiempo', 8, 0)
            elif self.sport_name in ['Jenga','Ajedrez','Domino','Parques','Horripicasa','Lucha']:
                sport_object = muns_interface.MunsInterface(self.sport_name, 'Vidas Reversa', 0, 3)

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
                winner = local

            elif results[1] > results[0]:
                self.table[away]["w"] += 1
                self.table[away]["pts"] += 3
                self.table[local]["l"] += 1
                winner = away

            else:
                self.table[local]["d"] += 1
                self.table[away]["d"] += 1
                self.table[local]["pts"] += 1
                self.table[away]["pts"] += 1

            return winner, {
                "team1": local,
                "team2": away,
                "score1": results[0],
                "score2": results[1],
                "winner": winner
            }
        
    def simulate_tournament(self):
        teams = self.generate_bracket(self.teams)
        bracket = {}
        semifinal_losers = []

        while len(teams) > 1:
            round = []
            winners = []
            round_name = self.round_name(len(teams))

            for i in range(0, len(teams), 2):
                w, match = self.simulate_tournament_match(teams[i], teams[i+1])
                round.append(match)
                winners.append(w)
            
            bracket[round_name] = round
            if len(teams) == 4:
                semifinal_losers = [
                    m["team1"] if m["winner"] == m["team2"] else m["team2"]
                    for m in round
                ]

            teams = winners


            
        final = bracket["Final"][0]
        champion = final["winner"]
        runnerup = final["team1"] if final["winner"] == final["team2"] else final["team2"]

        if self.has_third_place:
            third_winner, third_match = self.simulate_tournament_match(semifinal_losers[0], semifinal_losers[1])
            bracket["Third Place"] = [third_match]
        else:
            third_winner = "N/A"
            third_match = {
                "team1": "N/A",
                "team2": "N/A",
                "score1": 0,
                "score2": 0,
                "pen1": -1,
                "pen2": -1,
                "winner": "N/A"
                }

            bracket["Third Place"] = [third_match]
        for team in self.teams:
            self.table[team]["gd"] = (
                self.table[team]["gf"] - self.table[team]["gc"]
             )

        return {
            "tournament_name": self.trn_name,
            "bracket": bracket,
            "champion": champion,
            "runner_up": runnerup,
            "third_place": third_winner
        }
    
    def get_tournament_table(self):
        return self.table
    
    def get_tournament_matches(self):

        if isinstance(self.matches[0], list):
            matches = list(itertools.chain.from_iterable(self.matches))
        else:
            matches = self.matches

        matches_dict = [
            dict(zip(["team1","score1","team2","score2"], m))
            for m in matches
        ]

        return matches_dict
    
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
    

    def generate_tournament_bracket(self, data):

        WIDTH = 5760
        HEIGHT = 3240

        BOX_W = 640
        BOX_H = 160

        LEFT_START = 240
        RIGHT_START = WIDTH - 240 - BOX_W

        X_SPACING = 840
        BASE_Y = 240

        BG = (16,18,30)
        BOX = (40,42,65)
        LINE = (200,210,255)
        WIN = (80,220,120)
        TEXT = (240,240,255)
        GOLD = (255,215,0)

        img = Image.new("RGBA",(WIDTH,HEIGHT),BG)
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("arial.ttf",56)
        font_title = ImageFont.truetype("arial.ttf",80)

        rounds = list(data.keys())
        main_rounds = rounds[:-2]

        left_positions = {}
        right_positions = {}

        # ---------- NUEVA FUNCIÓN DE SCORE ----------
        def format_score(match, team):

            if team == match["team1"]:
                base = match["score1"]
                pen = match.get("pen1")
                if pen == -1:
                    pen = None
            else:
                base = match["score2"]
                pen = match.get("pen2")
                if pen == -1:
                    pen = None

            # Si hay penales, mostrarlos
            if pen is not None:
                return f"{base} ({pen})"

            return str(base)

        # ---------- LADO IZQUIERDO ----------
        for r_index, round_name in enumerate(main_rounds):

            matches = data[round_name]
            x = LEFT_START + r_index * X_SPACING
            spacing = BASE_Y * (2**r_index)

            left_positions[round_name] = []

            for i in range(len(matches)//2):

                match = matches[i]
                y = HEIGHT/2 - (spacing * len(matches)/4) + i * spacing

                draw.rectangle((x,y,x+BOX_W,y+BOX_H), fill=BOX, outline=LINE, width=6)

                t1, t2 = match["team1"], match["team2"]
                s1, s2 = format_score(match,t1), format_score(match,t2)
                winner = match["winner"]

                c1 = WIN if winner == t1 else TEXT
                c2 = WIN if winner == t2 else TEXT

                draw.text((x+40,y+25),f"{t1}  {s1}",font=font,fill=c1)
                draw.text((x+40,y+90),f"{t2}  {s2}",font=font,fill=c2)

                left_positions[round_name].append((x,y))

        # ---------- LADO DERECHO ----------
        for r_index, round_name in enumerate(main_rounds):

            matches = data[round_name]
            x = RIGHT_START - r_index * X_SPACING
            spacing = BASE_Y * (2**r_index)

            right_positions[round_name] = []

            for i in range(len(matches)//2, len(matches)):

                match = matches[i]
                idx = i - len(matches)//2

                y = HEIGHT/2 - (spacing * len(matches)/4) + idx * spacing

                draw.rectangle((x,y,x+BOX_W,y+BOX_H), fill=BOX, outline=LINE, width=6)

                t1, t2 = match["team1"], match["team2"]
                s1, s2 = format_score(match,t1), format_score(match,t2)
                winner = match["winner"]

                c1 = WIN if winner == t1 else TEXT
                c2 = WIN if winner == t2 else TEXT

                draw.text((x+40,y+25),f"{t1}  {s1}",font=font,fill=c1)
                draw.text((x+40,y+90),f"{t2}  {s2}",font=font,fill=c2)

                right_positions[round_name].append((x,y))

        # ---------- LÍNEAS ----------
        def draw_connections(positions, direction="right"):

            for r in range(len(main_rounds)-1):

                current = main_rounds[r]
                nxt = main_rounds[r+1]

                for i,(x,y) in enumerate(positions[current]):

                    target = i // 2
                    nx,ny = positions[nxt][target]

                    if direction == "right":
                        start_x = x + BOX_W
                        mid_x = start_x + 120
                    else:
                        start_x = x
                        mid_x = start_x - 120

                    start_y = y + BOX_H/2
                    end_x = nx + (0 if direction=="right" else BOX_W)
                    end_y = ny + BOX_H/2

                    draw.line((start_x,start_y,mid_x,start_y), fill=LINE, width=6)
                    draw.line((mid_x,start_y,mid_x,end_y), fill=LINE, width=6)
                    draw.line((mid_x,end_y,end_x,end_y), fill=LINE, width=6)

        draw_connections(left_positions, "right")
        draw_connections(right_positions, "left")

        # ---------- FINAL ----------
        final = data["Final"][0]

        cx = WIDTH/2 - BOX_W/2
        cy = HEIGHT/2 - BOX_H/2

        draw.rectangle((cx,cy,cx+(BOX_W*2),cy+(BOX_H)*2),
                    fill=(60,60,90),
                    outline=GOLD,
                    width=8)

        t1, t2 = final["team1"], final["team2"]
        s1, s2 = format_score(final,t1), format_score(final,t2)
        winner = final["winner"]

        c1 = WIN if winner == t1 else TEXT
        c2 = WIN if winner == t2 else TEXT

        draw.text((cx+40,cy+25),f"{t1}  {s1}",font=font,fill=c1)
        draw.text((cx+40,cy+90),f"{t2}  {s2}",font=font,fill=c2)

        draw.text((WIDTH/2-200,cy-120),"FINAL",font=font_title,fill=GOLD)

        draw.text((WIDTH/2-200,cy+220),
                f"Campeón: {winner}",
                font=font_title,
                fill=GOLD)

        path = "media/bracket_"+self.trn_name+".png"
        img.save(path)

        return path