from django.urls import path, include
from .views import pagina_principal, pagina_partido_individual, cargar_equipos, mostrar_equipo, generar_partido, pagina_partidos_liga, generar_liga, insertar_equipo
from .views import pagina_partidos_torneo, generar_torneo, pagina_simulacion_completa, generar_simulacion_completa, generar_simulacion_completa_clubes, pagina_simulacion_completa_clubes
from .views import pagina_competencia, cargar_pruebas, generar_simulacion

urlpatterns = [
    path('', pagina_principal , name='pagina_principal'),
    #URLs Simulación de partidos#
    path('functions/matches/<int:match_class>/', pagina_partido_individual, name='pagina_partido_individual'), 
    path('functions/matches/load/<int:match_class>/', cargar_equipos, name='cargar_equipos'),
    path('functions/matches/load_team/<int:match_class>/', mostrar_equipo, name='mostrar_equipo'),
    path('functions/matches/simulate_match/<int:match_class>/', generar_partido, name='generar_partido'),
    #URLs Simulación de ligas#
    path('functions/leagues/<int:match_class>/', pagina_partidos_liga, name='pagina_partidos_liga'),
    path('functions/leagues/simulate_league/<int:match_class>/', generar_liga, name='generar_liga'),
    path('functions/leagues/load_team/<int:match_class>/', insertar_equipo, name='insertar_equipo'),
    #URLs Simulación de Torneos#
    path('functions/tournaments/<int:match_class>/', pagina_partidos_torneo, name='pagina_partidos_torneo'),
    path('functions/tournaments/simulate_tournament/<int:match_class>/', generar_torneo, name='generar_torneo'),
    #URLs Simulación de Competencias#
    path('functions/simulated_olympic/<int:match_class>/', pagina_competencia, name='pagina_competencia'),
    path('functions/simulated_olympic/load_sports/<int:match_class>/', cargar_pruebas, name='cargar_pruebas'),
    path('functions/simulated_olympic/simulate_sport/<int:match_class>/', generar_simulacion, name='generar_simulacion'),
    #URLS Simulación Completa#
    path('functions/full_simulation/<int:match_class>/', pagina_simulacion_completa, name='pagina_simulacion_completa'),
    path('functions/full_simulation_clubs/<int:match_class>/', pagina_simulacion_completa_clubes, name='pagina_simulacion_completa_clubes'),
    path('functions/full_simulation/simulate_tournament/<int:match_class>/', generar_simulacion_completa, name='generar_simulacion_completa'),
    path('functions/full_simulation_clubs/simulate_tournament/<int:match_class>/', generar_simulacion_completa_clubes, name='generar_simulacion_completa_clubes'),
    ]