import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match


# Create queries within functions
def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''

    if search_name is not None and search_country is not None:
        query = Q(full_name__icontains=search_name, country__icontains=search_country)
    elif search_name is not None:
        query = Q(full_name__icontains=search_name)
    else:
        query = Q(country__icontains=search_country)


    players = TennisPlayer.objects.filter(query).order_by('ranking')

    return '\n'.join(f"Tennis Player: {tp.full_name}, country: {tp.country}, ranking: {tp.ranking}" for tp in players)

def get_top_tennis_player():
    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if top_player is None:
        return ''

    return f"Top Tennis Player: {top_player.full_name} with {top_player.num_wins} wins."

def get_tennis_player_by_matches_count():
    player = TennisPlayer.objects.prefetch_related('matches').annotate(num_matches=Count('matches')).order_by('-num_matches','ranking').first()

    if player is None or not player.matches.exists():
        return ''

    return f"Tennis Player: {player.full_name} with {player.num_matches} matches played."


def get_tournaments_by_surface_type(surface=None):

    if surface is None:
       return ''

    tournaments = (Tournament.objects.prefetch_related('matches')
                   .annotate(num_matches=Count('matches'))
                   .filter(Q(surface_type__icontains=surface))
                   .order_by('-start_date'))
    if tournaments is None or not tournaments.exists():
        return ''


    return '\n'.join(
        f"Tournament: {tournament_info.name}, start date: {tournament_info.start_date}, "
        f"matches: {tournament_info.num_matches}"
        for tournament_info in tournaments
    )


def get_latest_match_info():
    latest_match = Match.objects.order_by('date_played','id').last()

    if latest_match is None:
        return ''

    players = latest_match.players.order_by('full_name')
    player1_full_name = players.first().full_name
    player2_full_name = players.last().full_name
    winner_full_name = "TBA" if latest_match.winner is None else latest_match.winner.full_name

    return (f"Latest match played on: {latest_match.date_played},"
            f" tournament: {latest_match.tournament.name},"
            f" score: {latest_match.score}, players: {player1_full_name}"
            f" vs {player2_full_name}, winner: "
            f"{winner_full_name}, summary: {latest_match.summary}")


def get_matches_by_tournament(tournament_name=None):
    tournament = Match.objects.select_related('tournament', 'winner').filter(tournament__name__exact=tournament_name).order_by('-date_played')

    if tournament_name is None or tournament is None or not tournament.exists():
        return "No matches found."

    match_info = []
    [match_info.append(f"Match played on: {match.date_played}, score: {match.score}, winner: {match.winner.full_name if match.winner else 'TBA'}") for match in tournament]


    return '\n'.join(match_info)