from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q, Sum, F, Case, When, IntegerField, Max, Min
from django.db.models.functions import Coalesce
from .models import Teamregion, Nationalteams, Olympicplayers, Teamsports, Clubleague, Clubs, Playercountry, Playertournamentsports, Teamranks, Sportsrecords, Clubmatchesregister, Teamtournamentregister
from .models import Teammatchesregister, Teamtitleregister, Playertitleregister, Clubtitleregister, Playertournamentregister, Clubtournamentregister
import base64
from core_scripts.interfaces.sports_interfaces import sports_by_time, sports_by_sets, sports_by_ends, sports_by_special_sets, sports_by_timed_points
from core_scripts.interfaces.games_interfaces import goldeneye_interface, mariokart_interface, supersmash_interface, muns_interface
from core_scripts.leagues import league_group
from core_scripts.tournaments import tournament_group
from core_scripts.tournaments import full_tournament, full_tournament_clubs
from core_scripts.interfaces.olympic_sports_interfaces import sports_by_heats, sports_by_individual, sports_by_rounds
from core_scripts.clubs_leagues import club_league_season
import itertools
from openpyxl import Workbook
import os
from django.conf import settings
import random
import pandas as pd
import re
import json
<<<<<<< HEAD
from django.core.exceptions import ObjectDoesNotExist
=======
>>>>>>> cbb3fcc64d501702e72cc1b74cb854126a66434c

def pagina_principal(request):
    return render(request, 'main/simulator_page.html')

def pagina_partido_individual(request, match_class):
    page_groups = []
    page_teams = []
    page_sports = []
    name_mun = 'Munecos'
    list_games = ['Super Smash', 'Goldeneye', 'Mario Kart']
    id_munecos = Teamsports.objects.get(team_sport_name = name_mun).team_sport_id
    id_games_query = Teamsports.objects.filter(team_sport_name__in = list_games)
    id_games = []
    for id_game in id_games_query:
        id_games.append(id_game)
    #1: Paises, 2: Juegos, 3: Clubes, 4: Muñecos, 5: Paises(Femenino)#
    if match_class == 1:
        page_groups = Teamregion.objects.all()
        page_teams = Nationalteams.objects.exclude(team_name__icontains='Fem')
        page_sports = Teamsports.objects.filter(Q(team_sport_name__icontains='Masculino'))
    elif match_class == 2:
        page_groups = id_games_query
        page_teams = Olympicplayers.objects.filter(team_sport_id__in = id_games)
        page_sports = Playertournamentsports.objects.filter(Q(player_trn_sport_id__lt = 11) | Q(player_trn_sport_id__gt = 19))
    elif match_class == 3:
        page_groups = Clubleague.objects.all()
        page_teams = Clubs.objects.all()
        page_sports.append('Clubes')
    elif match_class == 4:
        page_groups = Playercountry.objects.all()
        page_teams = Olympicplayers.objects.filter(team_sport_id = id_munecos)
        page_sports = Playertournamentsports.objects.filter(player_trn_sport_id__gt = 10, player_trn_sport_id__lt = 20)
    elif match_class == 5:
        page_groups = Teamregion.objects.all()
        page_teams = Nationalteams.objects.filter(team_name__icontains='Fem')
        page_sports = Teamsports.objects.filter(Q(team_sport_name__icontains='Femenino'))
    else:
        page_groups = Teamregion.objects.all()
        page_teams = Nationalteams.objects.all()
        page_sports = Teamsports.objects.filter(Q(team_sport_name__icontains='Masculino') | Q(team_sport_name__icontains='Femenino'))

    return render(request, 'match/sports_match_page.html', 
                  {'equipos': page_teams, 'agrupaciones': page_groups, 'deportes': page_sports, 'clase': match_class, 'genero': 'M'})

def pagina_partidos_liga(request, match_class):
    request.session.flush()
    page_groups = []
    page_teams = []
    page_sports = []
    list_games = ['Super Smash']
    id_games_query = Teamsports.objects.filter(team_sport_name__in = list_games)
    id_games = []
    for id_game in id_games_query:
        id_games.append(id_game)
    #1: Paises, 2: Juegos, 3: Clubes, 4: Muñecos, 5: Paises(Femenino)#
    if match_class == 1:
        page_groups = Teamregion.objects.all()
        page_teams = Nationalteams.objects.exclude(team_name__icontains='Fem')
        page_sports = Teamsports.objects.filter(Q(team_sport_name__icontains='Masculino'))
    elif match_class == 2:
        page_groups = id_games_query
        page_teams = Olympicplayers.objects.filter(team_sport_id__in = id_games)
        page_sports = Playertournamentsports.objects.filter(player_trn_sport_id__in = [7,8,9,10,20,21,22])
    elif match_class == 3:
        page_groups = Clubleague.objects.all()
        page_teams = Clubs.objects.all()
        page_sports.append('Clubes')
    elif match_class == 5:
        page_groups = Teamregion.objects.all()
        page_teams = Nationalteams.objects.filter(team_name__icontains='Fem')
        page_sports = Teamsports.objects.filter(Q(team_sport_name__icontains='Femenino'))
    else:
        page_groups = Teamregion.objects.all()
        page_teams = Nationalteams.objects.all()
        page_sports = Teamsports.objects.filter(Q(team_sport_name__icontains='Masculino') | Q(team_sport_name__icontains='Femenino'))

    return render(request, 'league/sports_league_page.html', 
                  {'equipos': page_teams, 'agrupaciones': page_groups, 'deportes': page_sports, 'clase': match_class, 'genero': 'M'})

def pagina_partidos_torneo(request, match_class):
    request.session.flush()
    page_groups = []
    page_teams = []
    page_sports = []
    name_mun = 'Munecos'
    list_games = ['Super Smash', 'Goldeneye', 'Mario Kart']
    id_munecos = Teamsports.objects.get(team_sport_name = name_mun).team_sport_id
    id_games_query = Teamsports.objects.filter(team_sport_name__in = list_games)
    id_games = []
    for id_game in id_games_query:
        id_games.append(id_game)
    #1: Paises, 2: Juegos, 3: Clubes, 4: Muñecos, 5: Paises(Femenino)#
    if match_class == 1:
        page_groups = Teamregion.objects.all()
        page_teams = Nationalteams.objects.exclude(team_name__icontains='Fem')
        page_sports = Teamsports.objects.filter(Q(team_sport_name__icontains='Masculino'))
    elif match_class == 2:
        page_groups = id_games_query
        page_teams = Olympicplayers.objects.filter(team_sport_id__in = id_games)
        page_sports = Playertournamentsports.objects.filter(Q(player_trn_sport_id__lt = 11) | Q(player_trn_sport_id__gt = 19))
    elif match_class == 3:
        page_groups = Clubleague.objects.all()
        page_teams = Clubs.objects.all()
        page_sports.append('Clubes')
    elif match_class == 4:
        page_groups = Playercountry.objects.all()
        page_teams = Olympicplayers.objects.filter(team_sport_id = id_munecos)
        page_sports = Playertournamentsports.objects.filter(player_trn_sport_id__gt = 10, player_trn_sport_id__lt = 20)
    elif match_class == 5:
        page_groups = Teamregion.objects.all()
        page_teams = Nationalteams.objects.filter(team_name__icontains='Fem')
        page_sports = Teamsports.objects.filter(Q(team_sport_name__icontains='Femenino'))
    else:
        page_groups = Teamregion.objects.all()
        page_teams = Nationalteams.objects.all()
        page_sports = Teamsports.objects.filter(Q(team_sport_name__icontains='Masculino') | Q(team_sport_name__icontains='Femenino'))

    return render(request, 'tournament/sports_tournament_page.html', 
                  {'equipos': page_teams, 'agrupaciones': page_groups, 'deportes': page_sports, 'clase': match_class, 'genero': 'M'})

def pagina_competencia(request, match_class):
    sports_categories = []
    sports = []
    list_of_ex = list(range(39,47))
    list_of_ids = list(range(39,46))
    if match_class == 1:
        sports_categories = Teamsports.objects.filter(~Q(team_sport_id__in = list_of_ex ), team_sport_class = 'L')
    elif match_class == 2:
        sports_categories = Teamsports.objects.filter(team_sport_id__in = list_of_ids)
    elif match_class == 4:
        sports_categories = Teamsports.objects.filter(team_sport_id = 46)
    else:
        sports_categories = Teamsports.objects.filter(~Q(team_sport_id__in = list_of_ex ), team_sport_class = 'L')
    
    sports_elements = Sportsrecords.objects.all()
    for sp in sports_elements:
        sports.append(sp.sp_record_name)

    print(sports_categories)

    return render(request, 'olympic/sports_simulation_page.html', {'categorias': sports_categories, 'deportes': sports, 'clase': match_class})

def cargar_pruebas(request, match_class):
    categoria = request.GET.get('categoria')
    sport = Teamsports.objects.get(team_sport_name = categoria)
    page_sports = Sportsrecords.objects.filter(team_sport_id = sport.team_sport_id)
    return render(request, 'general/change_sports_template.html', {'deportes': page_sports})

def cargar_equipos(request, match_class):
    agrupacion = request.GET.get('agrupacion')
    name_mun = 'Munecos'
    id_munecos = Teamsports.objects.get(team_sport_name = name_mun).team_sport_id
    #1: Paises, 2: Juegos, 3: Clubes, 4: Muñecos #
    if match_class == 1:
        page_teams = Nationalteams.objects.filter(team_region_id = agrupacion).exclude(team_name__icontains='Fem')
    elif match_class == 2:
        page_teams = Olympicplayers.objects.filter(team_sport_id = agrupacion)
    elif match_class == 3:
        page_teams = Clubs.objects.filter(club_league_id = agrupacion)
    elif match_class == 4:
        page_teams = Olympicplayers.objects.filter(team_sport_id = id_munecos).filter(ol_country_id = agrupacion)
    elif match_class == 5:
        page_teams = Nationalteams.objects.filter(team_region_id = agrupacion).filter(team_name__icontains='Fem')
    else:
        page_teams = Nationalteams.objects.filter(team_region_id = agrupacion)

    print(page_teams.count())

    return render(request, 'general/change_teams_template.html', {'equipos': page_teams, 'clase': match_class})

def mostrar_equipo(request, match_class):
    equipo_id = request.GET.get('equipo_id')
    page_team = []
    img = None
    orientacion = request.GET.get("orientacion")

    if match_class == 1:
        page_team = Nationalteams.objects.get(team_id = equipo_id)
        img = page_team.team_shield
    elif match_class == 2:
        page_team = Olympicplayers.objects.get(ol_player_id = equipo_id)
        img = page_team.ol_player_image
    elif match_class == 3:
        page_team = Clubs.objects.get(club_id = equipo_id)
        img = page_team.club_shield
    elif match_class == 4:
        page_team = Olympicplayers.objects.get(ol_player_id = equipo_id)
        img = page_team.ol_player_image
    elif match_class == 5:
        page_team = Nationalteams.objects.get(team_id = equipo_id)
        img = page_team.team_shield
    else:
        page_team = Nationalteams.objects.get(team_id = equipo_id)
    
    img_base64 = base64.b64encode(bytes(img)).decode('utf-8')
    
    return render(request, 'general/insert_team_template.html',{'equipo': page_team, 'imagen': img_base64, 'class': match_class, 'orientacion': orientacion})

def generar_partido(request, match_class):
    valor_local = request.GET.get('equipolocal')
    valor_visitante = request.GET.get('equipovisitante')
    equipo_local = None
    equipo_visitante = None
    rank_local = None
    rank_visitante = None
    deporte = None
    hay_tiempo_extra = request.GET.get('tiempoextra')
    hay_doble_ronda = request.GET.get('dobleronda')
    sport_object = None
    sport_class = ''
    results = None

    print(valor_local)
    print(valor_visitante)

    if match_class == 1 or match_class == 5:
        equipo_local = Nationalteams.objects.get(team_name = valor_local)
        equipo_visitante = Nationalteams.objects.get(team_name = valor_visitante)
        deporte = Teamsports.objects.get(team_sport_name = request.GET.get('deporte'))
        rank_local = Teamranks.objects.get(team_id = equipo_local.team_id, team_sport_id = deporte.team_sport_id)
        rank_local = rank_local.team_rank
        rank_visitante = Teamranks.objects.get(team_id = equipo_visitante.team_id, team_sport_id = deporte.team_sport_id)
        rank_visitante = rank_visitante.team_rank

    elif match_class == 2:
        equipo_local = Olympicplayers.objects.get(ol_player_name = valor_local)
        equipo_visitante = Olympicplayers.objects.get(ol_player_name = valor_visitante)
        deporte = Playertournamentsports.objects.get(player_trn_sport_name = request.GET.get('deporte'))
        rank_local = equipo_local.ol_player_value
        rank_visitante = equipo_visitante.ol_player_value

    elif match_class == 3:
        equipo_local = Clubs.objects.get(club_name = valor_local)
        equipo_visitante = Clubs.objects.get(club_name = valor_visitante)
        deporte = Teamsports.objects.get(team_sport_name = 'Futbol Masculino')
        rank_local = equipo_local.club_value
        rank_visitante = equipo_visitante.club_value

    elif match_class == 4:
        equipo_local = Olympicplayers.objects.get(ol_player_name = valor_local)
        equipo_visitante = Olympicplayers.objects.get(ol_player_name = valor_visitante)
        deporte = Playertournamentsports.objects.get(player_trn_sport_name = request.GET.get('deporte'))
        rank_local = equipo_local.ol_player_value
        rank_visitante = equipo_visitante.ol_player_value

    else:
        equipo_local = Nationalteams.objects.get(team_name = valor_local)
        equipo_visitante = Nationalteams.objects.get(team_name = valor_visitante)
        deporte = Teamsports.objects.get(team_sport_name = request.GET.get('deporte'))
        rank_local = Teamranks.objects.get(team_id = equipo_local.team_id, team_sport_id = deporte.team_sport_id)
        rank_local = rank_local.team_rank
        rank_visitante = Teamranks.objects.get(team_id = equipo_visitante.team_id, team_sport_id = deporte.team_sport_id)
        rank_visitante = rank_visitante.team_rank

    #print(deporte.team_sport_name)
    print(hay_doble_ronda)
    print(hay_tiempo_extra)
    print(rank_local, rank_visitante)

    if match_class in [1,3,5]:
        print('sport')
        if deporte.team_sport_name in ['Futbol Masculino', 'Futbol Femenino']:
            sport_object = sports_by_time.TimeSport(deporte.team_sport_name, 2, 45, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'tiempo'
        elif deporte.team_sport_name in ['Basketball Masculino', 'Basketball Femenino']:
            sport_object = sports_by_time.TimeSport(deporte.team_sport_name, 4, 200, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'tiempo'
        elif deporte.team_sport_name in ['Balonmano Masculino', 'Balonmano Femenino']:
            sport_object = sports_by_time.TimeSport(deporte.team_sport_name, 2, 30, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'tiempo'
        elif deporte.team_sport_name in ['Rugby Masculino', 'Rugby Femenino']:
            sport_object = sports_by_time.TimeSport(deporte.team_sport_name, 2, 40, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'tiempo'
        elif deporte.team_sport_name in ['Futsal Masculino', 'Futsal Femenino']:
            sport_object = sports_by_time.TimeSport(deporte.team_sport_name, 2, 20, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'tiempo'
        elif deporte.team_sport_name in ['Hockey Masculino', 'Hockey Femenino']:
            sport_object = sports_by_time.TimeSport(deporte.team_sport_name, 3, 20, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'tiempo'
        elif deporte.team_sport_name in ['Volleyball Masculino', 'Volleyball Femenino']:
            sport_object = sports_by_sets.SetsSport(deporte.team_sport_name, 3, 25, 15, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'sets'
        elif deporte.team_sport_name in ['Voley Playa Masculino', 'Voley Playa Femenino']:
            sport_object = sports_by_sets.SetsSport(deporte.team_sport_name, 3, 21, 15, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'sets'
        elif deporte.team_sport_name in ['Squash Masculino', 'Squash Femenino']:
            sport_object = sports_by_sets.SetsSport(deporte.team_sport_name, 3, 11, 0, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'sets'
        elif deporte.team_sport_name in ['Tenis de Mesa Masculino', 'Tenis de Mesa Femenino']:
            sport_object = sports_by_sets.SetsSport(deporte.team_sport_name, 3, 11, 0, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'sets'
        elif deporte.team_sport_name in ['Tenis Masculino', 'Tenis Femenino']:
            sport_object = sports_by_sets.SetsSport(deporte.team_sport_name, 3, 60, 0, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'sets'
        elif deporte.team_sport_name in ['Badminton Masculino', 'Badminton Femenino']:
            sport_object = sports_by_sets.SetsSport(deporte.team_sport_name, 3, 21, 21, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'sets'
        elif deporte.team_sport_name in ['Beisbol Masculino', 'Beisbol Femenino']:
            sport_object = sports_by_ends.EndsSport(deporte.team_sport_name, 9, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'ends'
        elif deporte.team_sport_name in ['Tiro con Arco Masculino', 'Tiro con Arco Femenino']:
            sport_object = sports_by_special_sets.SpecialSetsSport(deporte.team_sport_name, 6, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'sets'
        elif deporte.team_sport_name in ['Curling Masculino', 'Curling Femenino']:
            sport_object = sports_by_ends.EndsSport(deporte.team_sport_name, 10, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'ends'
        elif deporte.team_sport_name in ['Esgrima Masculino', 'Esgrima Femenino']:
            sport_object = sports_by_timed_points.TimedPointsSport(deporte.team_sport_name, 3, 15, hay_tiempo_extra, hay_doble_ronda)
            sport_class = 'sets'

        sport_object.get_probability_list()
        results = sport_object.simulate_match(rank_local, rank_visitante)

    elif match_class in [2,4]:
        if deporte.player_trn_sport_name == 'GE-Time':
            sport_object = goldeneye_interface.GoldeneyeInterface(deporte.player_trn_sport_name,'Tiempo', 3, 0)
            sport_class = 'tiempo'
        elif deporte.player_trn_sport_name == 'GE-Kills':
            sport_object = goldeneye_interface.GoldeneyeInterface(deporte.player_trn_sport_name,'Vidas', 0, 10)
            sport_class = 'sets'
        elif deporte.player_trn_sport_name == 'GE-SSDV':
            sport_object = goldeneye_interface.GoldeneyeInterface(deporte.player_trn_sport_name,'Vidas Reversa', 0, 2)
            sport_class = 'sets'
        elif deporte.player_trn_sport_name == 'GE-License to Kill':
            sport_object = goldeneye_interface.GoldeneyeInterface(deporte.player_trn_sport_name,'Vidas', 0, 20)
            sport_class = 'sets'
        elif deporte.player_trn_sport_name == 'GE-Teams':
            sport_object = goldeneye_interface.GoldeneyeInterface(deporte.player_trn_sport_name,'Vidas', 0, 15)
            sport_class = 'sets'
        elif deporte.player_trn_sport_name == 'MK-Battles':
            sport_object = mariokart_interface.MarioKartInterface(deporte.player_trn_sport_name,'Vidas Reversa', 0, 3)
            sport_class = 'sets'
        elif deporte.player_trn_sport_name == 'SSB-Time':
            sport_object = supersmash_interface.SuperSmashInterface(deporte.player_trn_sport_name, 'Tiempo', 3, 0)
            sport_class = 'time'
        elif deporte.player_trn_sport_name == 'SSB-Lives':
            sport_object = supersmash_interface.SuperSmashInterface(deporte.player_trn_sport_name, 'Vidas Reversa', 0, 5)
            sport_class = 'sets'
        elif deporte.player_trn_sport_name == 'SSB-Coins':
            sport_object = supersmash_interface.SuperSmashInterface(deporte.player_trn_sport_name, 'Cumulativo', 3, 0)
            sport_class = 'time'
        elif deporte.player_trn_sport_name == 'SSB-Stamina':
            sport_object = supersmash_interface.SuperSmashInterface(deporte.player_trn_sport_name, 'Stamina', 0, 150)
            sport_class = 'time'
        elif deporte.player_trn_sport_name == 'SSB-Lightning':
            sport_object = supersmash_interface.SuperSmashInterface(deporte.player_trn_sport_name, 'Tiempo', 2, 0)
            sport_class = 'time'
        elif deporte.player_trn_sport_name == 'SSB-Single':
            sport_object = supersmash_interface.SuperSmashInterface(deporte.player_trn_sport_name, 'Tiempo', 3, 0)
            sport_class = 'time'
        elif deporte.player_trn_sport_name == 'SSB-Sudden':
            sport_object = supersmash_interface.SuperSmashInterface(deporte.player_trn_sport_name, 'Tiempo', 1, 0)
            sport_class = 'time'
        
        elif deporte.player_trn_sport_name in ['Futbol', 'Hockey en Piso']:
            sport_object = muns_interface.MunsInterface(deporte.player_trn_sport_name, 'Tiempo', 2, 0)
        elif deporte.player_trn_sport_name in 'Baloncesto':
            sport_object = muns_interface.MunsInterface(deporte.player_trn_sport_name, 'Tiempo', 8, 0)
        elif deporte.player_trn_sport_name in ['Jenga','Ajedrez','Domino','Parques','Horripicasa','Lucha']:
            sport_object = muns_interface.MunsInterface(deporte.player_trn_sport_name, 'Vidas Reversa', 0, 3)

        print(sport_object.game_type)
        results = sport_object.simulate_game(sport_object.game_type)
        print(results)
    
    return render(request, 'match/match_results_template.html',{'resultado': results, 'clase_deporte': sport_class})

def insertar_equipo(request, match_class):
    equipo_id = request.GET.get('equipo_id')
    print('este es el equipo_id: ' + equipo_id)
    if "equipos_actuales" not in request.session:
        print('sesion vacia')
        request.session["equipos_actuales"] = []
    
    if equipo_id in request.session["equipos_actuales"]:
        print('duplicado')
        return HttpResponse("")

    request.session["equipos_actuales"].append(equipo_id)
    request.session.modified = True

    print(request.session["equipos_actuales"])

    if equipo_id == '':
        return HttpResponse("")

    if match_class == 1:
        page_team = Nationalteams.objects.get(team_id = equipo_id)
    elif match_class == 2:
        page_team = Olympicplayers.objects.get(ol_player_id = equipo_id)
    elif match_class == 3:
        page_team = Clubs.objects.get(club_id = equipo_id)
    elif match_class == 4:
        page_team = Olympicplayers.objects.get(ol_player_id = equipo_id)
    elif match_class == 5:
        page_team = Nationalteams.objects.get(team_id = equipo_id)
    else:
        page_team = Nationalteams.objects.get(team_id = equipo_id)
    return render(request, 'general/insert_league_team_template.html',{'equipo': page_team, 'clase': match_class})

def eliminar_equipo(request, match_class):
    if request.method == 'POST':
        data = json.loads(request.body)
        team_id = data.get('team_id')  # ⚠️ string

        equipos = request.session.get("equipos_actuales", [])

        if team_id in equipos:
            equipos.remove(team_id)
            request.session["equipos_actuales"] = equipos
            request.session.modified = True

            return JsonResponse({'status': 'ok'})

        return JsonResponse({'status': 'error', 'mensaje': 'No estaba en sesión'})
    return HttpResponse("")

def generar_liga(request, match_class):
    equipos_seleccionados = request.GET.getlist("equipos")
    valor_ida_vuelta = request.GET.get('idayvuelta')
    ranks = []
    teams = []
    groups = None
    sport_type = ''

    if match_class == 1 or match_class == 5:
        equipos = Nationalteams.objects.filter(team_id__in = equipos_seleccionados)
        deporte = Teamsports.objects.get(team_sport_name = request.GET.get('deporte'))
        for eq in equipos:
            rank = Teamranks.objects.get(team_id = eq.team_id, team_sport_id = deporte.team_sport_id)
            teams.append(eq.team_name)
            rank_tuple = (eq.team_name, rank.team_rank)
            ranks.append(rank_tuple)

    elif match_class == 2:
        equipos = Olympicplayers.objects.filter(ol_player_id__in = equipos_seleccionados)
        deporte = Playertournamentsports.objects.get(player_trn_sport_name = request.GET.get('deporte'))
        for eq in equipos:
            rank = eq.ol_player_value
            teams.append(eq.ol_player_name)
            rank_tuple = (eq.ol_player_name, rank)
            ranks.append(rank_tuple)

    elif match_class == 3:
        equipos = Clubs.objects.filter(club_id__in = equipos_seleccionados)
        deporte = Teamsports.objects.get(team_sport_name = 'Futbol Masculino')
        for eq in equipos:
            rank = eq.club_value
            teams.append(eq.club_name)
            rank_tuple = (eq.club_name, rank)
            ranks.append(rank_tuple)

    else:
        equipos = Nationalteams.objects.filter(team_id__in = equipos_seleccionados)
        deporte = Teamsports.objects.get(team_sport_name = request.GET.get('deporte'))
        for eq in equipos:
            rank = Teamranks.objects.get(team_id = eq.team_id, team_sport_id = deporte.team_sport_id)
            teams.append(eq.team_name)
            rank_tuple = (eq.team_name, rank.team_rank)
            ranks.append(rank_tuple)

    if match_class != 2:
        groups = league_group.Group('Grupo Liga '+deporte.team_sport_name, teams, valor_ida_vuelta, deporte.team_sport_name, 
                                    match_class, ranks)
    else:
        groups = league_group.Group('Grupo Liga '+deporte.player_trn_sport_name, teams, valor_ida_vuelta, deporte.player_trn_sport_name, 
                                    match_class, ranks)
    
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

    print(sorted_table)
    print(matches)

    for m in matches:
        print(type(m), m)
        for k in m:
            print(k)

    return render(request, 'league/league_table_template.html',{'table': sorted_table, 'clase': match_class, 'matches': matches})
    
def generar_torneo(request, match_class):
    equipos_seleccionados = request.GET.getlist("equipos")
    print(equipos_seleccionados)
    valor_ida_vuelta = request.GET.get('idayvuelta')
    valor_tercer_lugar = request.GET.get('tercerlugar')
    ranks = []
    teams = []
    groups = None
    sport_type = ''

    if len(equipos_seleccionados) not in [4,8,16,32,64]:
        return HttpResponse("")

    if match_class == 1 or match_class == 5:
        equipos = Nationalteams.objects.filter(team_id__in = equipos_seleccionados)
        deporte = Teamsports.objects.get(team_sport_name = request.GET.get('deporte'))
        for eq in equipos:
            rank = Teamranks.objects.get(team_id = eq.team_id, team_sport_id = deporte.team_sport_id)
            teams.append(eq.team_name)
            rank_tuple = (eq.team_name, rank.team_rank)
            ranks.append(rank_tuple)

    elif match_class == 2 or match_class == 4:
        equipos = Olympicplayers.objects.filter(ol_player_id__in = equipos_seleccionados)
        deporte = Playertournamentsports.objects.get(player_trn_sport_name = request.GET.get('deporte'))
        for eq in equipos:
            rank = eq.ol_player_value
            teams.append(eq.ol_player_name)
            rank_tuple = (eq.ol_player_name, rank)
            ranks.append(rank_tuple)

    elif match_class == 3:
        equipos = Clubs.objects.filter(club_id__in = equipos_seleccionados)
        deporte = Teamsports.objects.get(team_sport_name = 'Futbol Masculino')
        for eq in equipos:
            rank = eq.club_value
            teams.append(eq.club_name)
            rank_tuple = (eq.club_name, rank)
            ranks.append(rank_tuple)

    else:
        equipos = Nationalteams.objects.filter(team_id__in = equipos_seleccionados)
        deporte = Teamsports.objects.get(team_sport_name = request.GET.get('deporte'))
        for eq in equipos:
            rank = Teamranks.objects.get(team_id = eq.team_id, team_sport_id = deporte.team_sport_id)
            teams.append(eq.team_name)
            rank_tuple = (eq.team_name, rank.team_rank)
            ranks.append(rank_tuple)

    if match_class not in [2,4]:
        tournament = tournament_group.Tournament('Torneo de '+ deporte.team_sport_name, deporte.team_sport_name, teams, ranks,
                                                  valor_ida_vuelta, valor_tercer_lugar, match_class)
    else:
        tournament = tournament_group.Tournament('Torneo de '+ deporte.player_trn_sport_name, deporte.player_trn_sport_name, teams, ranks,
                                                  valor_ida_vuelta, valor_tercer_lugar, match_class)
    
    print(tournament)
    trn_result = tournament.simulate_tournament()
    table = tournament.get_tournament_table()
    matches = tournament.get_tournament_matches()
    
    table_names = []
    table_values = []
    info_trn = trn_result['bracket'].get('Third Place')
    print(info_trn)
    print(trn_result)
    trn_result['bracket'].pop("Third Place")

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
    for m in matches:
        print(type(m), m)
        for k in m:
            print(k)

    return render(request, 'tournament/tournament_results_template.html',{'table': sorted_table, 'clase': match_class, 'matches': matches,
                                                        "bracket": trn_result["bracket"],
                                                        "champion": trn_result["champion"],
                                                        "runner_up": trn_result["runner_up"],
                                                        "third_place": trn_result["third_place"],
                                                        "third_match": info_trn})

def pagina_simulacion_completa(request, match_class):
    request.session.flush()
    years = itertools.chain(range(1880,2016,4), range(2013,2101))
    page_groups = []
    page_teams = []
    page_sports = []
    name_mun = 'Munecos'
    list_games = ['Super Smash', 'Goldeneye', 'Mario Kart']
    id_munecos = Teamsports.objects.get(team_sport_name = name_mun).team_sport_id
    id_games_query = Teamsports.objects.filter(team_sport_name__in = list_games)
    id_games = []
    for id_game in id_games_query:
        id_games.append(id_game)
    #1: Paises, 2: Juegos, 3: Clubes, 4: Muñecos, 5: Paises(Femenino)#
    if match_class == 1:
        page_groups = Teamregion.objects.all()
        page_teams = Nationalteams.objects.exclude(team_name__icontains='Fem')
        page_sports = Teamsports.objects.filter(Q(team_sport_name__icontains='Masculino'))
    elif match_class == 2:
        page_groups = id_games_query
        page_teams = Olympicplayers.objects.filter(team_sport_id__in = id_games)
        page_sports = Playertournamentsports.objects.filter(Q(player_trn_sport_id__lt = 11) | Q(player_trn_sport_id__gt = 19))
    elif match_class == 4:
        page_groups = Playercountry.objects.all()
        page_teams = Olympicplayers.objects.filter(team_sport_id = id_munecos)
        page_sports = Playertournamentsports.objects.filter(player_trn_sport_id__gt = 10, player_trn_sport_id__lt = 20)
    elif match_class == 5:
        page_groups = Teamregion.objects.all()
        page_teams = Nationalteams.objects.filter(team_name__icontains='Fem')
        page_sports = Teamsports.objects.filter(Q(team_sport_name__icontains='Femenino'))
    else:
        page_groups = Teamregion.objects.all()
        page_teams = Nationalteams.objects.all()
        page_sports = Teamsports.objects.filter(Q(team_sport_name__icontains='Masculino') | Q(team_sport_name__icontains='Femenino'))

    return render(request, 'full_simulation/complete_simulation_page.html', 
                  {'equipos': page_teams, 'agrupaciones': page_groups, 'deportes': page_sports, 'clase': match_class, 'years': years})

def generar_simulacion_completa(request, match_class):
    ranks = []
    teams = []
    teams_by_cn = []
    full_trn = None
    valor_año = request.GET.get('valoryear')
    hay_guardado = request.GET.get('registrarres')
    file_name = ''

    if match_class == 1:
        equipos = Nationalteams.objects.exclude(team_name__icontains='Fem')
        continentes = Teamregion.objects.all()
        deporte = Teamsports.objects.get(team_sport_name = request.GET.get('deporte'))
        for eq in equipos:
            rank = Teamranks.objects.get(team_id = eq.team_id, team_sport_id = deporte.team_sport_id)
            teams.append(eq.team_name)
            rank_tuple = (eq.team_name, rank.team_rank)
            ranks.append(rank_tuple)  
        for cn in continentes:
            temp_team_list = []
            for eq in teams:
                try:
                    team = Nationalteams.objects.get(team_name = eq, team_region_id = cn.team_region_id)
                    temp_team_list.append(team.team_name)
                except:
                    print('', end='')

            teams_by_cn.append(temp_team_list)
        full_trn = full_tournament.FullTournament(teams_by_cn, [cn.team_region_name for cn in continentes], ranks, deporte.team_sport_name, 8, match_class, valor_año, hay_guardado)
        file_name = f"simulacion_{deporte.team_sport_name}_{valor_año}.xlsx"
    elif match_class == 5:
        equipos = Nationalteams.objects.filter(team_name__icontains='Fem')
        continentes = Teamregion.objects.all()
        deporte = Teamsports.objects.get(team_sport_name = request.GET.get('deporte'))

        for eq in equipos:
            rank = Teamranks.objects.get(team_id = eq.team_id, team_sport_id = deporte.team_sport_id)
            teams.append(eq.team_name)
            rank_tuple = (eq.team_name, rank.team_rank)
            ranks.append(rank_tuple)        

        for cn in continentes:
            temp_team_list = []
            for eq in teams:
                try:
                    team = Nationalteams.objects.get(team_name = eq, team_region_id = cn.team_region_id)
                    temp_team_list.append(team.team_name)
                except:
                    print('', end='')

            teams_by_cn.append(temp_team_list)

        full_trn = full_tournament.FullTournament(teams_by_cn, [cn.team_region_name for cn in continentes], ranks, deporte.team_sport_name, 8, match_class,valor_año,hay_guardado)
        file_name = f"simulacion_{deporte.team_sport_name}_{valor_año}.xlsx"
    elif match_class == 2 or match_class == 4:      
        deporte = Playertournamentsports.objects.get(player_trn_sport_name = request.GET.get('deporte'))
        equipos = Olympicplayers.objects.all()
        list_games = ['Goldeneye', 'Super Smash', 'Mario Kart']
        name_mun = 'Munecos'
        id_munecos = Teamsports.objects.get(team_sport_name = name_mun).team_sport_id

        if "GE" in deporte.player_trn_sport_name:
            id_games_query = Teamsports.objects.get(team_sport_name = list_games[0])
            equipos = equipos.filter(team_sport_id = id_games_query)
            num_groups = 2
        elif "SSB" in deporte.player_trn_sport_name:
            id_games_query = Teamsports.objects.get(team_sport_name = list_games[1])
            equipos = equipos.filter(team_sport_id = id_games_query)
            num_groups = 8
        elif "MK" in deporte.player_trn_sport_name:
            id_games_query = Teamsports.objects.get(team_sport_name = list_games[2])
            equipos = equipos.filter(team_sport_id = id_games_query)
            num_groups = 1
        else:
            if deporte.player_trn_sport_name not in ['Futbol', 'Baloncesto', 'Hockey en Piso']:
                countries = Playercountry.objects.all()
                selected_players = []
                temp_equipos = None
                for c in countries:
                    temp_equipos = equipos.filter(ol_country = c.ol_country_id, team_sport = id_munecos)
                    player_list = []
                    for e in temp_equipos:
                        if not '_MN' in e.ol_player_name:
                            player_list.append(e.ol_player_name)
                    rand = random.randint(0, len(player_list))
                    selected_players.append(player_list[rand])
                equipos = equipos.filter(ol_player_name__in = selected_players)
                num_groups = 1
            else:
                equipos = equipos.filter(ol_player_name__contains = '_MN')
                num_groups = 1

        for eq in equipos:
            rank = eq.ol_player_value
            teams.append(eq.ol_player_name)
            rank_tuple = (eq.ol_player_name, rank)
            ranks.append(rank_tuple)

        full_trn = full_tournament.FullTournament(teams, deporte.player_trn_sport_name, ranks, deporte.player_trn_sport_name, num_groups, match_class, valor_año, hay_guardado)
        file_name = f"simulacion_{deporte.player_trn_sport_name}_{valor_año}.xlsx"
    else:
        equipos = Nationalteams.objects.all()
        deporte = Teamsports.objects.get(team_sport_name = request.GET.get('deporte'))
        file_name = f"simulacion_{deporte.team_sport_name}_{valor_año}.xlsx"
        for eq in equipos:
            rank = Teamranks.objects.get(team_id = eq.team_id, team_sport_id = deporte.team_sport_id)
            teams.append(eq.team_name)
            rank_tuple = (eq.team_name, rank.team_rank)
            ranks.append(rank_tuple)

    full_trn.simulate_tournament()
    
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        # Crear carpeta media si no existe
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    full_trn.generate_tournament_excel(file_path)

    download_url = settings.MEDIA_URL + file_name

    return render(request, "general/generate_download_excel.html", {
        "download_url": download_url
    })

def pagina_simulacion_completa_clubes(request, match_class):
    request.session.flush()

    years = itertools.chain(range(1880,2016,4), range(2013,2101))
    page_groups = []
    page_teams = []
    page_sports = []
    page_groups = Clubleague.objects.all()
    page_teams = Clubs.objects.all()
    page_sports.append('Clubes')

    return render(request, 'full_simulation/complete_simulation_page.html', 
                  {'equipos': page_teams, 'agrupaciones': page_groups, 'deportes': page_sports, 'clase': match_class, 'years': years})

def generar_simulacion_completa_clubes(request, match_class):
    ranks = []
    teams = []
    teams_by_lg = []
    full_trn = None
    valor_año = request.GET.get('valoryear')
    hay_guardado = request.GET.get('registrarres')
    file_name = ''
    download_links = []


    Clubmatchesregister.objects.filter(match_year = str(valor_año)).delete()
    equipos = Clubs.objects.all()
    ligas = Clubleague.objects.all()
    deporte = Teamsports.objects.get(team_sport_name = 'Futbol Masculino')
    continentes = Teamregion.objects.all()
    lista_continentes = [cont.team_region_name for cont in continentes]

    for eq in equipos:
        rank = eq.club_value
        teams.append(eq.club_name)
        rank_tuple = (eq.club_name, rank)
        ranks.append(rank_tuple)
    
    for lg in ligas:
        temp_team_list = []
        lg_country = Nationalteams.objects.get(team_id = lg.club_country.team_id)
        lg_region = Teamregion.objects.get(team_region_id = lg.team_region_id)
        lg_teams = Clubs.objects.filter(club_league = lg)
        for eq in lg_teams:
            temp_team_list.append(eq.club_name)
        new_tuple = (temp_team_list, lg_country.team_name, lg.club_league_name, lg.club_division,
                      lg.club_first_qual, lg.club_second_qual, lg.club_third_qual, lg.clas_direct, lg_region.team_region_name)  
        print(new_tuple[1], new_tuple[2])
        teams_by_lg.append(new_tuple)
    
    from collections import defaultdict

    agrupado = defaultdict(list)

    for t in teams_by_lg:
        agrupado[t[1]].append(t)

    resultado = dict(agrupado)
    total_results = []
    archivos = []
    rutas = []
    
    for pais,tuplas in resultado.items():
        print(pais)    
        for tp in tuplas:
            qualifier_list = [tp[4], tp[5], tp[6]]  
            if tp[1] == 'Inglaterra':
                print('Este es Inglaterra')
            has_promotion = False
            promotions = 0
            if len(tuplas) >= 2:
                has_promotion = True
                promotions = 2
            else:
                has_promotion = False
                promotions = 0
            season = club_league_season.ClubLeagueSeason(tp, tp[1], has_promotion, valor_año, promotions, qualifier_list, tp[8], hay_guardado, ranks)
            season.simulate_league()
            file_name = f"simulacion_liga_{tp[2]}_{valor_año}.xlsx"
            archivos.append(file_name)       
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            rutas.append(file_path)
                    # Crear carpeta media si no existe
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            season.generate_tournament_excel(file_path)
            if tp[3] == '1D': 
                results = season.get_full_results()
                total_results.append(results)

    exito = True
    try:
        with pd.ExcelWriter("media/fase_ligas_"+valor_año+".xlsx") as writer:
            for f in rutas:
                hojas = pd.read_excel(f, sheet_name=None)
                f = os.path.basename(f)
                f = f.replace("simulacion_liga_", "").replace(".xlsx","")       
                for nombre_hoja, df in hojas.items():
                    nombre_final = limpiar_nombre(f"{f}_{nombre_hoja}")[:31]
                    df.to_excel(writer, sheet_name=nombre_final[:31], index=False)
    except Exception as e:
        exito = False
        print("Error:", e)

    if exito:
        for f in rutas:
            os.remove(f)

    download_url = settings.MEDIA_URL + "fase_ligas_"+valor_año+".xlsx"
    download_links.append(download_url)   
    # inicializar 6 listas por continente
    agrupado = {
        c: [[] for _ in range(6)]
        for c in lista_continentes
    }

    for t in total_results:
        continente = t[1]

        if continente in agrupado:
            for i, bloque in enumerate(t[0]):   # i = posición (0 a 5)
                for sub in bloque:
                    agrupado[continente][i].extend(sub)

    ultimos = {
    continente: listas[-3:]
    for continente, listas in agrupado.items()
    }

    temp_qual_list = []
    for cont, lists in ultimos.items():
        for el in range(len(lists)):
            if len(lists[el]) > 0:
                groups = league_group.Group('Grupo Liga ', lists[el], True, 'Futbol Masculino', 
                                    match_class, ranks)
                groups.generate_calendar()
                groups.simulate_league()
                if cont == 'Europa':
                    if el == 0:
                        temp_qual_list.append(groups.get_qualified_teams(6))
                    else:
                        temp_qual_list.append(groups.get_qualified_teams(8))
                elif cont == 'America':
                    if el == 0:
                        temp_qual_list.append(groups.get_qualified_teams(2))
                    else:
                        temp_qual_list.append(groups.get_qualified_teams(2)) 
                table = groups.get_league_table()
                matches = groups.get_league_matches()
    

    print('Clasificados: ', temp_qual_list)
    print("")

    for cont, lists in agrupado.items():
        for el in range(len(lists)):
            if cont == 'America':
                if el == 0:
                    lists[el].extend(temp_qual_list[0])
                elif el == 1:
                    lists[el].extend(temp_qual_list[1])
                else:
                    pass
            elif cont == 'Europa':
                if el == 0:
                    lists[el].extend(temp_qual_list[2])
                elif el == 1:
                    lists[el].extend(temp_qual_list[3])
                elif el == 2:
                    lists[el].extend(temp_qual_list[4])
                else:
                    pass

        
    for k, l in agrupado.items():
        print(k, l)
        for i in l:
            print(len(i))      

    equipos_copas = {
        continente: listas[:3]
        for continente, listas in agrupado.items()
    }

    sublista_nombres = ['UEFA Champions League', 'UEFA Europa League', 'UEFA Conference League', 'Copa Libertadores', 'Copa Sudamericana',
                        'AFC Champions League Elite','AFC Champions League Two', 'AFC Challenge League', 'CAF Champions League', 'CAF Conference League']
    nombre_liga = ""
    num_grupos = 0
    world_qualified_total = []
    for cont, listas in equipos_copas.items():
        for el in range(len(listas)):
            if len(listas[el])> 0:
                if cont == 'Europa':
                    num_grupos = 1
                    if el == 0:
                        nombre_liga = sublista_nombres[0]
                    elif el == 1:
                        nombre_liga = sublista_nombres[1]
                    elif el == 2:
                        nombre_liga = sublista_nombres[2]
                elif cont == 'America':
                    num_grupos = 8
                    if el == 0:
                        nombre_liga = sublista_nombres[3]
                    elif el == 1:
                        nombre_liga = sublista_nombres[4]
                elif cont == 'Asia/Oceania':
                    if el == 0:
                        num_grupos = 8
                        nombre_liga = sublista_nombres[5]
                    elif el == 1:
                        num_grupos = 8
                        nombre_liga = sublista_nombres[6]
                    elif el == 2:
                        num_grupos = 4
                        nombre_liga = sublista_nombres[7]
                elif cont == 'Africa':
                    num_grupos = 8
                    if el == 0:
                        nombre_liga = sublista_nombres[8]
                    elif el == 1:
                        nombre_liga = sublista_nombres[9]

                full_trn = full_tournament_clubs.FullTournamentClubs(listas[el], nombre_liga, ranks, 'Futbol Masculino', num_grupos, match_class, valor_año, hay_guardado)
                full_trn.simulate_tournament()
                world_qualified_total.extend(full_trn.get_world_qualified())
                file_name = f"simulacion_{nombre_liga}_{valor_año}.xlsx"       
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    # Crear carpeta media si no existe
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                download_url = settings.MEDIA_URL + file_name
                download_links.append(download_url)
                full_trn.generate_tournament_excel(file_path)  

            else:
                pass
    world_qualified_total = list(itertools.chain.from_iterable(world_qualified_total))
    print('Clasificados mundial de clubes')
    print(world_qualified_total)
    full_trn = full_tournament_clubs.FullTournamentClubs(world_qualified_total, 'Mundial de Clubes', ranks, 'Futbol Masculino', 8, match_class, valor_año, hay_guardado)
    full_trn.simulate_tournament()
    file_name = f"simulacion_Mundial de Clubes_{valor_año}.xlsx"       
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        # Crear carpeta media si no existe
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    full_trn.generate_tournament_excel(file_path)  
    
    download_url = settings.MEDIA_URL + file_name
    download_links.append(download_url)

    download_links = [s.replace("/media/","") for s in download_links]

    return render(request, "general/generate_download_excel_clubs.html", {
        "download_links": download_links
    })
    
def limpiar_nombre(nombre):
    return re.sub(r'[:\\/*?\[\]]', '', nombre)    

def generar_simulacion(request, match_class):
    ranks = []
    teams = []
    groups = None
    sport = Teamsports.objects.get(team_sport_name = request.GET.get('categoria'))
    contest = request.GET.get('prueba')
    print(sport.team_sport_name)

    if match_class == 1 or match_class == 5:
        equipos = Nationalteams.objects.exclude(team_name__icontains='Fem')
        deporte = Sportsrecords.objects.get(sp_record_name = contest)
        for eq in equipos:
            rank = Teamranks.objects.get(team_id = eq.team_id, team_sport_id = sport.team_sport_id)
            teams.append(eq.team_name)
            rank_tuple = (eq.team_name, rank.team_rank)
            ranks.append(rank_tuple)

    elif match_class in [2,4]:
        if sport.team_sport_name != 'Goldeneye':
            equipos = Olympicplayers.objects.filter(~Q(ol_player_name__contains='/'), team_sport_id = sport.team_sport_id)
        else:
            equipos = Olympicplayers.objects.filter(ol_player_name__contains='_GE')

        deporte = Sportsrecords.objects.get(sp_record_name = contest)
        for eq in equipos:
            rank = eq.ol_player_value
            teams.append(eq.ol_player_name)
            rank_tuple = (eq.ol_player_name, rank)
            ranks.append(rank_tuple)
    else:
        equipos = Nationalteams.objects.exclude(team_name__icontains='Fem')
        deporte = Sportsrecords.objects.get(sp_record_name = contest)
        for eq in equipos:
            rank = Teamranks.objects.get(team_id = eq.team_id, team_sport_id = sport.team_sport_id)
            teams.append(eq.team_name)
            rank_tuple = (eq.team_name, rank.team_rank)
            ranks.append(rank_tuple)

    table_results = []
    if deporte.sport_class == 'H':    
        olympic_sim = sports_by_heats.SportsByHeats(deporte.sp_record_name, float(deporte.sp_record_best), float(deporte.sp_record_last), deporte.sport_class)
        for r in ranks:
            results = (r[0] ,r[1] ,olympic_sim.select_type_game(r[1], 4, 0))
            table_results.append(results)
    elif deporte.sport_class == 'I':
        olympic_sim = sports_by_individual.SportsByIndividual(deporte.sp_record_name, float(deporte.sp_record_best), float(deporte.sp_record_last), deporte.sport_class)
        for r in ranks:
            results = (r[0] ,r[1] ,olympic_sim.select_type_game(r[1], 1, 0))
            table_results.append(results)
    elif deporte.sport_class == 'R':
        olympic_sim = sports_by_rounds.SportsByRounds(deporte.sp_record_name, float(deporte.sp_record_best), float(deporte.sp_record_last), deporte.sport_class)
        for r in ranks:
            results = (r[0] ,r[1] ,olympic_sim.select_type_game(r[1], 4, 7))
            table_results.append(results)
    else:
        olympic_sim = sports_by_individual.SportsByIndividual(deporte.sp_record_name, float(deporte.sp_record_best), float(deporte.sp_record_last), deporte.sport_class)
        for r in ranks:
            results = (r[0] ,r[1] ,olympic_sim.select_type_game(r[1], 1, 0))
            table_results.append(results)

    if float(deporte.sp_record_best) < float(deporte.sp_record_last):
        table_results = sorted(table_results, key=lambda x: x[2])
    else:
        table_results = sorted(table_results, key=lambda x: x[2], reverse=True)

    return render(request, 'olympic/simulation_table_template.html',{'resultados': table_results, 'clase': match_class})

def pagina_registro_por_pais(request):
    sports = Teamsports.objects.filter(~Q(team_sport_name__icontains = 'Mario'), team_sport_class = 'T')
    countries = Nationalteams.objects.all()
    return render(request, 'logs/country_register_page.html', {'deportes': sports, 'paises': countries})

def pagina_registro_por_pais_olimpico(request):
    return render(request, 'logs/country_register_page_olympic.html')

def pagina_registro_por_jugador_individual(request):
    list_games = ['Super Smash', 'Goldeneye', 'Mario Kart']
    id_games_query = Teamsports.objects.filter(team_sport_name__in = list_games)
    id_games = []
    for id_game in id_games_query:
        id_games.append(id_game)

    players = Olympicplayers.objects.filter(team_sport_id__in = id_games)
    sports = Playertournamentsports.objects.filter(Q(player_trn_sport_id__lt = 11) | Q(player_trn_sport_id__gt = 19))
    return render(request, 'logs/player_register_page.html', {'deportes': sports, 'jugadores': players})

def pagina_registro_por_jugador_individual_olimpico(request):
    return render(request, 'logs/player_register_page_olympic.html')

def pagina_registro_por_pais_mayor(request):
    countries = Playercountry.objects.all()
    return render(request, 'logs/major_country_register_page.html', {'paises_mayores': countries})

def pagina_registro_por_pais_mayor_olimpico(request):
    return render(request, 'logs/major_country_register_page_olympic.html')

def pagina_registro_por_torneo(request):
    sports = Teamsports.objects.filter(~Q(team_sport_name__icontains = 'Mario'), team_sport_class = 'T')
    sports_players = Playertournamentsports.objects.all()
    years = itertools.chain(range(1880,2016,4), range(2013,2101))
    return render(request, 'logs/tournament_register_page.html', {'years': years, 'deportes': sports, 'deportes_jug': sports_players})

def pagina_registro_por_club(request):
    clubs = Clubs.objects.all()
    return render(request, 'logs/club_register_page.html', {'clubes': clubs})

def consultar_por_pais(request):
    pais = request.GET.get('pais')
    deporte = request.GET.get('deporte')

    print(deporte, pais)
    sport = Teamsports.objects.get(team_sport_name = deporte)
    country = Nationalteams.objects.get(team_name = pais)

    #Busqueda del pais Mayor
    major_country = Playercountry.objects.get(ol_country_id = country.ol_country.ol_country_id)

    #Busqueda del continente
    major_region = Teamregion.objects.get(team_region_id = country.team_region.team_region_id)

    #Victorias, derrotas y empates históricos
    historic_values = Teamtournamentregister.objects.filter(
        team_id=country.team_id,
        team_sport_id=sport.team_sport_id
    ).aggregate(
        total_wins=Coalesce(Sum('team_wins'), 0),
        total_draws=Coalesce(Sum('team_draws'), 0),
        total_loses=Coalesce(Sum('team_loses'), 0),
        total_scored=Coalesce(Sum('team_sc_points'), 0),
        total_against=Coalesce(Sum('team_ag_points'), 0)
    )

    qs = Teammatchesregister.objects.filter(
        Q(team_local_id=country.team_id) | Q(team_away_id=country.team_id),
        team_sport_id=sport.team_sport_id
    ).annotate(
        goles_favor=Case(
            When(team_local_id=country.team_id, then=F('team_local_score')),
            When(team_away_id=country.team_id, then=F('team_away_score')),
            output_field=IntegerField()
        ),
        goles_contra=Case(
            When(team_local_id=country.team_id, then=F('team_away_score')),
            When(team_away_id=country.team_id, then=F('team_local_score')),
            output_field=IntegerField()
        ),
        rival=Case(
        When(team_local_id=country.team_id, then=F('team_away')),
        When(team_away_id=country.team_id, then=F('team_local')),
        ),
        diferencia=F('goles_favor') - F('goles_contra')
    )

    mejor = qs.order_by('-diferencia').first()
    rival_mejor = []
    rival_peor = []
    if mejor == None:
        rival_mejor = []
    else:
        rival_mejor = Nationalteams.objects.get(team_id = mejor.rival)
    peor = qs.order_by('diferencia').first()
    if peor == None:
        rival_peor = []
    else:
        rival_peor = Nationalteams.objects.get(team_id = peor.rival)

    titulos = None
    try:
        titulos = Teamtitleregister.objects.filter(team_id = country.team_id, team_sport_id = sport.team_sport_id)
    except Teamtitleregister.DoesNotExist:
        titulos = []

    print(titulos)



    return render(request, 'logs/country_search_results.html', {'pais_mayor': major_country, 'continente': major_region, 
                                                                'valores_historicos': historic_values, 'mejor_partido': mejor,
                                                                'peor_partido': peor, 'rival_mejor': rival_mejor, 'rival_peor': rival_peor,
                                                                'titulos':titulos})


def consultar_por_jugador(request):
    deporte = request.GET.get('deporte')
    jugador = request.GET.get('jugador')

    print(deporte, jugador)

    sport = Playertournamentsports.objects.get(player_trn_sport_name = deporte)
    player = Olympicplayers.objects.get(ol_player_name = jugador)

    #Busqueda del pais Mayor
    major_country = Playercountry.objects.get(ol_country_id = player.ol_country.ol_country_id)

    #Victorias, derrotas y empates históricos
    historic_values = Playertournamentregister.objects.filter(
        ol_player_id=player.ol_player_id,
        player_trn_sport_id=sport.player_trn_sport_id
    ).aggregate(
        total_wins=Coalesce(Sum('ol_player_wins'), 0),
        total_draws=Coalesce(Sum('ol_player_draws'), 0),
        total_loses=Coalesce(Sum('ol_player_loses'), 0),
        total_scored=Coalesce(Sum('ol_player_sc_points'), 0),
        total_against=Coalesce(Sum('ol_player_ag_points'), 0)
    )

    titulos = None
    try:
        titulos = Playertitleregister.objects.filter(ol_player_id = player.ol_player_id, player_trn_sport_id = sport.player_trn_sport_id)
    except Playertitleregister.DoesNotExist:
        titulos = []

    print(titulos)

    return render(request, 'logs/player_search_results.html', {'pais_mayor': major_country, 
                                                                'valores_historicos': historic_values,
                                                                'titulos':titulos})

def consultar_por_clubes(request):
    deporte = request.GET.get('deporte')
    club = request.GET.get('club')

    print(deporte, club)

    sport = Teamsports.objects.get(team_sport_name = deporte)
    clubs = Clubs.objects.get(club_name = club)

    #Busqueda del pais
    country = Nationalteams.objects.get(team_id = clubs.club_country.team_id)

    #Busqueda del pais Mayor
    major_country = Playercountry.objects.get(ol_country_id = country.ol_country.ol_country_id)

    #Busqueda de la liga
    club_league = Clubleague.objects.get(club_league_id = clubs.club_league.club_league_id)

    #Victorias, derrotas y empates históricos
    historic_values = Clubtournamentregister.objects.filter(
        club_id=clubs.club_id
    ).aggregate(
        total_wins=Coalesce(Sum('club_wins'), 0),
        total_draws=Coalesce(Sum('club_draws'), 0),
        total_loses=Coalesce(Sum('club_loses'), 0),
        total_scored=Coalesce(Sum('club_sc_points'), 0),
        total_against=Coalesce(Sum('club_ag_points'), 0)
    )

    qs = Clubmatchesregister.objects.filter(
        Q(club_local_id=clubs.club_id) | Q(club_away_id=clubs.club_id)
    ).annotate(
        goles_favor=Case(
            When(club_local_id=clubs.club_id, then=F('club_local_score')),
            When(club_away_id=clubs.club_id, then=F('club_away_score')),
            output_field=IntegerField()
        ),
        goles_contra=Case(
            When(club_local_id=clubs.club_id, then=F('club_away_score')),
            When(club_away_id=clubs.club_id, then=F('club_local_score')),
            output_field=IntegerField()
        ),
        rival=Case(
        When(club_local_id=clubs.club_id, then=F('club_away')),
        When(club_away_id=clubs.club_id, then=F('club_local')),
        ),
        diferencia=F('goles_favor') - F('goles_contra')
    )

    mejor = qs.order_by('-diferencia').first()
    rival_mejor = []
    rival_peor = []
    if mejor == None:
        rival_mejor = []
    else:
        rival_mejor = Clubs.objects.get(club_id = mejor.rival)
    peor = qs.order_by('diferencia').first()
    if peor == None:
        rival_peor = []
    else:
        rival_peor = Clubs.objects.get(club_id = peor.rival)

    titulos = None
    try:
        titulos = Clubtitleregister.objects.filter(club_id = clubs.club_id)
    except Clubtitleregister.DoesNotExist:
        titulos = []

    print(titulos)



    return render(request, 'logs/club_search_results.html', {'pais_mayor': major_country, 'liga': club_league, 'pais': country, 
                                                                'valores_historicos': historic_values, 'mejor_partido': mejor,
                                                                'peor_partido': peor, 'rival_mejor': rival_mejor, 'rival_peor': rival_peor,
                                                                'titulos':titulos})


def consultar_por_pais_mayor(request):

    pais = request.GET.get('pais')

    print(pais)
    sports = Teamsports.objects.filter(~Q(team_sport_name__icontains = 'Mario'), team_sport_class = 'T')
    sports_players = Playertournamentsports.objects.all()

    list_historic_values_countries = []
    list_historic_values_players = []

    major_country = Playercountry.objects.get(ol_country_name = pais)

    #Paises
    countries = Nationalteams.objects.filter(ol_country = major_country.ol_country_id)
    id_countries = [country.team_id for country in countries]

    #Jugadores
    players = Olympicplayers.objects.filter(ol_country = major_country.ol_country_id)
    id_players = [player.ol_player_id for player in players]

    #Clubes
    clubs = Clubs.objects.filter(club_country__in = id_countries)
    id_clubs = [club.club_id for club in clubs]

    #Victorias, derrotas y empates históricos por países
    for sport in sports:
        historic_values_countries = Teamtournamentregister.objects.filter(
            team_id__in=id_countries,
            team_sport_id=sport.team_sport_id
        ).aggregate(
            total_wins=Coalesce(Sum('team_wins'), 0),
            total_draws=Coalesce(Sum('team_draws'), 0),
            total_loses=Coalesce(Sum('team_loses'), 0),
            total_scored=Coalesce(Sum('team_sc_points'), 0),
            total_against=Coalesce(Sum('team_ag_points'), 0)
        )

        historic_values_countries["sport_name"] = sport.team_sport_name
        list_historic_values_countries.append(historic_values_countries)

    #Victorias, derrotas y empates históricos por jugadores
    for sport_pl in sports_players:
        historic_values_players = Playertournamentregister.objects.filter(
            ol_player_id__in = id_players,
            player_trn_sport_id=sport_pl.player_trn_sport_id
        ).aggregate(
            total_wins=Coalesce(Sum('ol_player_wins'), 0),
            total_draws=Coalesce(Sum('ol_player_draws'), 0),
            total_loses=Coalesce(Sum('ol_player_loses'), 0),
            total_scored=Coalesce(Sum('ol_player_sc_points'), 0),
            total_against=Coalesce(Sum('ol_player_ag_points'), 0)
        )
        historic_values_players["sport_name"] = sport_pl.player_trn_sport_name
        list_historic_values_players.append(historic_values_players)


    #Victorias, derrotas y empates históricos por clubes
    historic_values_clubs = Clubtournamentregister.objects.filter(
        club_id__in = id_clubs
    ).aggregate(
        total_wins=Coalesce(Sum('club_wins'), 0),
        total_draws=Coalesce(Sum('club_draws'), 0),
        total_loses=Coalesce(Sum('club_loses'), 0),
        total_scored=Coalesce(Sum('club_sc_points'), 0),
        total_against=Coalesce(Sum('club_ag_points'), 0)
    )


    titulos_paises = None
    titulos_jugadores = None
    titulos_clubes = None

    #titulos por pais
    try:
        titulos_paises = Teamtitleregister.objects.filter(team_id__in = id_countries).annotate(
            country_name=F('team__team_name')
            )
    except Teamtitleregister.DoesNotExist:
        titulos_paises = []

    print(titulos_paises)
    for p in titulos_paises:
        print(p.country_name)

    #titulos por jugador
    titulos_jugadores = None
    try:
        titulos_jugadores = Playertitleregister.objects.filter(ol_player_id__in = id_players).annotate(
            player_name=F('ol_player__ol_player_name')
        )
    except Playertitleregister.DoesNotExist:
        titulos_jugadores = []

    
    #titulos por club
    titulos_clubes = None
    try:
        titulos_clubes = Clubtitleregister.objects.filter(club_id__in = id_clubs).annotate(
            club_name=F('club__club_name')
        )
    except Clubtitleregister.DoesNotExist:
        titulos_clubes = []



    return render(request, 'logs/major_country_search_results.html', {'valores_historicos_paises': list_historic_values_countries,
                                                                      'valores_historicos_jugadores': list_historic_values_players,
                                                                      'valores_historicos_clubes': historic_values_clubs,
                                                                      'titulos_paises':titulos_paises,
                                                                      'titulos_jugadores':titulos_jugadores,
                                                                      'titulos_clubes':titulos_clubes})

def consultar_por_torneo(request):
    deporte = request.GET.get('deporte')
    año = request.GET.get('valoryear')
    print(deporte, año)
<<<<<<< HEAD
    tournament_data = []
    tournament_teams = []
=======
>>>>>>> cbb3fcc64d501702e72cc1b74cb854126a66434c

    if deporte != 'Clubes':
        #Archivo Excel con el torneo
        try:
            hojas = pd.read_excel(
            "media/simulacion_"+str(deporte)+"_"+str(año)+".xlsx",
            sheet_name=None
            )

            for elementos, df in hojas.items():
                print("Hoja: ", elementos)
<<<<<<< HEAD
                # Buscar inicio de partidos
                fila_partidos = df[
                    df.iloc[:,0] == "Partidos"
                ].index[0]

                # --------------------
                # TABLA DE POSICIONES
                # --------------------

                tabla = df.iloc[0:fila_partidos-2].copy()

                tabla.columns = tabla.iloc[0]
                tabla = tabla[1:].reset_index(drop=True)

                tabla = tabla.dropna(axis=1, how='all')
                # --------------------
                # PARTIDOS
                # --------------------

                partidos = df.iloc[fila_partidos+1:].copy()

                partidos.columns = partidos.iloc[0]
                partidos = partidos[1:].reset_index(drop=True)

                partidos = partidos.dropna(axis=1, how='all')
                partidos = partidos.rename(columns={
                    "Team 1": "team1",
                    "Team 2": "team2",
                    "Score 1": "score1",
                    "Score 2": "score2"
                })

                tournament_data.append((elementos, tabla.columns.to_list(), tabla.to_dict(orient="records"), partidos.columns.to_list(), partidos.to_dict(orient="records")))

            #print(tournament_data)
=======
                print(df.head())

>>>>>>> cbb3fcc64d501702e72cc1b74cb854126a66434c
            tourament_info = None
            #Imagen y bracket del torneo#
            try:
                sport = Teamsports.objects.get(team_sport_name = deporte)
                tourament_info = Teamtitleregister.objects.filter(team_sport_id = sport.team_sport_id, title_year = str(año))
<<<<<<< HEAD
                for ti in tourament_info:
                    champion = ''
                    not_champion = ''
                    element = ti.title_bracket['Final'][0]
                    print(element)
                    if element['winner'] == element['team1']:
                        champion = element['team1']
                        not_champion = element['team2']
                    else:
                        champion = element['team2']
                        not_champion = element['team1']
                    third_place = ti.title_bracket['Third Place'][0]['winner']
                    tournament_teams.append((ti.title_label, champion, not_champion, third_place, ti.title_image))
            except ObjectDoesNotExist as e:
                sport = Playertournamentsports.objects.get(player_trn_sport_name = deporte)
                tourament_info = Playertitleregister.objects.filter(player_trn_sport_id = sport.player_trn_sport_id, title_year = str(año))
                for ti in tourament_info:
                    champion = ''
                    not_champion = ''
                    element = ti.title_bracket['Final'][0]
                    print(element)
                    if element['winner'] == element['team1']:
                        champion = element['team1']
                        not_champion = element['team2']
                    else:
                        champion = element['team2']
                        not_champion = element['team1']
                    third_place = ti.title_bracket['Third Place'][0]['winner']
                    tournament_teams.append((ti.title_label, champion, not_champion, third_place, ti.title_image))
        except FileNotFoundError as e:
            print(e)
=======
                print(tourament_info)
                pass
            except Teamtitleregister.DoesNotExist:
                sport = Playertournamentsports.objects.get(player_trn_sport_name = deporte)
                tourament_info = Playertitleregister.objects.filter(player_trn_sport_id = sport.player_trn_sport_id, title_year = str(año))
        except:
            print('No existe')
>>>>>>> cbb3fcc64d501702e72cc1b74cb854126a66434c
    else:
        sublista_nombres = ['fase_ligas', 'UEFA Champions League', 'UEFA Europa League', 'UEFA Conference League', 'Copa Libertadores', 'Copa Sudamericana',
                'AFC Champions League Elite','AFC Champions League Two', 'AFC Challenge League', 'CAF Champions League', 'CAF Conference League', 'Mundial de Clubes']
        lista_excel = []
        try:
            for sub in sublista_nombres:
                print(sub)
                hojas = None
                if sub == 'fase_ligas':
                    hojas = pd.read_excel(
                    "media/"+str(sub)+"_"+str(año)+".xlsx",
                    sheet_name=None
                    )
                else:
                    hojas = pd.read_excel(
                    "media/simulacion_"+str(sub)+"_"+str(año)+".xlsx",
                    sheet_name=None
                    )
                lista_excel.append(hojas)
                for elementos, df in hojas.items():
                    print("Hoja: ", elementos)
<<<<<<< HEAD
                    # Buscar inicio de partidos
                    fila_partidos = df[
                        df.iloc[:,0] == "Partidos"
                    ].index[0]

                    # --------------------
                    # TABLA DE POSICIONES
                    # --------------------

                    tabla = df.iloc[0:fila_partidos-2].copy()

                    tabla.columns = tabla.iloc[0]
                    tabla = tabla[1:].reset_index(drop=True)

                    tabla = tabla.dropna(axis=1, how='all')
                    # --------------------
                    # PARTIDOS
                    # --------------------

                    partidos = df.iloc[fila_partidos+1:].copy()

                    partidos.columns = partidos.iloc[0]
                    partidos = partidos[1:].reset_index(drop=True)

                    partidos = partidos.dropna(axis=1, how='all')
                    partidos = partidos.rename(columns={
                        "Team 1": "team1",
                        "Team 2": "team2",
                        "Score 1": "score1",
                        "Score 2": "score2"
                    })

                    tournament_data.append((elementos, tabla.columns.to_list(), tabla.to_dict(orient="records"), partidos.columns.to_list(), partidos.to_dict(orient="records")))

            tourament_info = None
            #Imagen y bracket del torneo#
            tourament_info = Clubtitleregister.objects.filter(title_year = str(año), title_bracket__isnull = False, title_image__isnull = False)
            for ti in tourament_info:
                champion = ''
                not_champion = ''
                element = ti.title_bracket['Final'][0]
                if element['winner'] == element['team1']:
                    champion = element['team1']
                    not_champion = element['team2']
                else:
                    champion = element['team2']
                    not_champion = element['team1']
                third_place = ti.title_bracket['Third Place'][0]['winner']
                tournament_teams.append((ti.title_label, champion, not_champion, third_place, ti.title_image))
        except FileNotFoundError as e:
            print(e)
    
    return render(request, 'logs/tournament_search_results.html', {'resultados_torneo': tournament_data, 'campeones_torneo': tournament_teams})
=======
                    print(df.head())

            tourament_info = None
            #Imagen y bracket del torneo#
            tourament_info = Clubtitleregister.objects.filter(title_year = str(año))
            print(tourament_info)
        except:
            print('No existe')
    

    return HttpResponse("")
>>>>>>> cbb3fcc64d501702e72cc1b74cb854126a66434c
