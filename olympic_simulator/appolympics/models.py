# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Clubleague(models.Model):
    club_league_id = models.BigAutoField(primary_key=True)
    club_league_name = models.CharField(max_length=150)
    club_country = models.ForeignKey('Nationalteams', models.DO_NOTHING, db_column='club_country')
    club_division = models.CharField(max_length=2)
    club_prom_reg = models.IntegerField()
    club_first_qual = models.IntegerField()
    club_second_qual = models.IntegerField()
    club_third_qual = models.IntegerField()
    clas_direct = models.CharField(max_length=2)
    team_region = models.ForeignKey('Teamregion', models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'ClubLeague'


class Clubmatchesregister(models.Model):
    club_match_id = models.BigAutoField(primary_key=True)
    club_local = models.ForeignKey('Clubs', models.DO_NOTHING)
    club_local_score = models.IntegerField()
    club_away = models.ForeignKey('Clubs', models.DO_NOTHING, related_name='clubmatchesregister_club_away_set')
    club_away_score = models.IntegerField()
    result_label = models.CharField(max_length=30)
    match_year = models.CharField(max_length=4)
    class Meta:
        managed = False
        db_table = 'ClubMatchesRegister'


class Clubtournamentregister(models.Model):
    club_tourn_id = models.BigAutoField(primary_key=True)
    club = models.ForeignKey('Clubs', models.DO_NOTHING)
    club_wins = models.IntegerField()
    club_draws = models.IntegerField()
    club_loses = models.IntegerField()
    club_sc_points = models.IntegerField()
    club_ag_points = models.IntegerField()
    club_position = models.IntegerField()
    club_year = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'ClubTournamentRegister'


class Clubs(models.Model):
    club_id = models.BigAutoField(primary_key=True)
    club_name = models.CharField(max_length=200)
    club_league = models.ForeignKey(Clubleague, models.DO_NOTHING)
    club_value = models.IntegerField()
    club_shield = models.BinaryField()
    club_country = models.ForeignKey('Nationalteams', models.DO_NOTHING, db_column='club_country')

    class Meta:
        managed = False
        db_table = 'Clubs'


class Nationalteams(models.Model):
    team_id = models.BigAutoField(primary_key=True)
    team_name = models.CharField(max_length=100)
    team_type = models.CharField(max_length=2)
    team_region = models.ForeignKey('Teamregion', models.DO_NOTHING)
    team_flag = models.BinaryField()
    team_shield = models.BinaryField()
    ol_country = models.ForeignKey('Playercountry', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'NationalTeams'


class Olympicplayers(models.Model):
    ol_player_id = models.BigAutoField(primary_key=True)
    ol_player_name = models.CharField(max_length=200)
    ol_player_value = models.IntegerField()
    ol_player_image = models.BinaryField()
    ol_country = models.ForeignKey('Playercountry', models.DO_NOTHING)
    team_sport = models.ForeignKey('Teamsports', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'OlympicPlayers'


class Playercountry(models.Model):
    ol_country_id = models.BigAutoField(primary_key=True)
    ol_country_name = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'PlayerCountry'


class Playersimulationregister(models.Model):
    sim_ol_reg_id = models.BigAutoField(primary_key=True)
    ol_player = models.ForeignKey(Olympicplayers, models.DO_NOTHING)
    ol_player_result = models.DecimalField(max_digits=50, decimal_places=3)
    ol_player_year = models.CharField(max_length=4)
    sp_record = models.ForeignKey('Sportsrecords', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'PlayerSimulationRegister'


class Playertournamentregister(models.Model):
    player_tourn_id = models.BigAutoField(primary_key=True)
    ol_player = models.ForeignKey(Olympicplayers, models.DO_NOTHING)
    ol_player_wins = models.IntegerField()
    ol_player_draws = models.IntegerField()
    ol_player_loses = models.IntegerField()
    ol_player_sc_points = models.IntegerField()
    ol_player_ag_points = models.IntegerField()
    ol_player_position = models.IntegerField()
    ol_player_year = models.CharField(max_length=4)
    player_trn_sport = models.ForeignKey('Playertournamentsports', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'PlayerTournamentRegister'


class Playertournamentsports(models.Model):
    player_trn_sport_id = models.BigAutoField(primary_key=True)
    player_trn_sport_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'PlayerTournamentSports'


class Sportplayer(models.Model):
    pk = models.CompositePrimaryKey('sp_record_id', 'ol_player_id')
    ol_player = models.ForeignKey(Olympicplayers, models.DO_NOTHING)
    sp_record = models.ForeignKey('Sportsrecords', models.DO_NOTHING)
    player_record_value = models.DecimalField(max_digits=50, decimal_places=3)
    player_record_year = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'SportPlayer'


class Sportsnationalteams(models.Model):
    pk = models.CompositePrimaryKey('team_id', 'sp_record_id')
    team = models.ForeignKey(Nationalteams, models.DO_NOTHING)
    sp_record = models.ForeignKey('Sportsrecords', models.DO_NOTHING)
    team_record_value = models.DecimalField(max_digits=50, decimal_places=3)
    team_record_year = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'SportsNationalTeams'


class Sportsrecords(models.Model):
    sp_record_id = models.CharField(primary_key=True, max_length=10)
    sp_record_name = models.CharField(max_length=100)
    sp_record_best = models.DecimalField(max_digits=50, decimal_places=3)
    sp_record_last = models.DecimalField(max_digits=50, decimal_places=3)
    sport_class = models.CharField(max_length=2)
    team_sport = models.ForeignKey('Teamsports', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'SportsRecords'


class Teammatchesregister(models.Model):
    team_match_id = models.BigAutoField(primary_key=True)
    team_local = models.ForeignKey(Nationalteams, models.DO_NOTHING)
    team_local_score = models.IntegerField()
    team_away = models.ForeignKey(Nationalteams, models.DO_NOTHING, related_name='teammatchesregister_team_away_set')
    team_away_score = models.IntegerField()
    result_label = models.CharField(max_length=300)
    match_year = models.CharField(max_length=4)
    team_sport = models.ForeignKey('Teamsports', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'TeamMatchesRegister'


class Teamranks(models.Model):
    pk = models.CompositePrimaryKey('team_id', 'team_sport_id')
    team = models.ForeignKey(Nationalteams, models.DO_NOTHING)
    team_sport = models.ForeignKey('Teamsports', models.DO_NOTHING)
    team_rank = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'TeamRanks'


class Teamregion(models.Model):
    team_region_id = models.BigAutoField(primary_key=True)
    team_region_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'TeamRegion'


class Teamsimulationregister(models.Model):
    sim_tm_reg_id = models.BigAutoField(primary_key=True)
    team = models.ForeignKey(Nationalteams, models.DO_NOTHING)
    team_result = models.DecimalField(max_digits=50, decimal_places=3)
    team_year = models.CharField(max_length=4)
    sp_record = models.ForeignKey(Sportsrecords, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'TeamSimulationRegister'


class Teamsports(models.Model):
    team_sport_id = models.BigAutoField(primary_key=True)
    team_sport_name = models.CharField(max_length=50)
    team_sport_class = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'TeamSports'


class Teamtournamentregister(models.Model):
    team_tourn_id = models.BigAutoField(primary_key=True)
    team = models.ForeignKey(Nationalteams, models.DO_NOTHING)
    team_wins = models.IntegerField()
    team_draws = models.IntegerField()
    team_loses = models.IntegerField()
    team_sc_points = models.IntegerField()
    team_ag_points = models.IntegerField()
    team_position = models.IntegerField()
    team_year = models.CharField(max_length=4)
    team_sport = models.ForeignKey(Teamsports, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'TeamTournamentRegister'


class Tournamentstage(models.Model):
    tourn_stage_id = models.BigAutoField(primary_key=True)
    tourn_stage_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'TournamentStage'
