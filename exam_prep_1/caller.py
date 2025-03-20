import os
import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Actor, Movie


# Create queries within functions
def populate_db():
    # Creating Directors
    director1 = Director.objects.create(
        full_name="Martin Scorseze",
        birth_date="1988-02-25",
        nationality="US",
        years_of_experience=3
    )

    director2 = Director.objects.create(
        full_name="Steven Spielberg",
        birth_date="1998-03-25",
        nationality="UK",
        years_of_experience=10
    )

    director3 = Director.objects.create(
        full_name="Alfred Hitchcock",
        birth_date="1998-04-25",
        nationality="AL",
        years_of_experience=20
    )

    # Creating Actors
    actor1 = Actor.objects.create(
        full_name="Brad Pitt",
        birth_date="1998-04-25",
        nationality="US",
        is_awarded=True

    )

    actor2 = Actor.objects.create(
        full_name="Angelina Jolie",
        birth_date="1997-04-25",
        nationality="US",
        is_awarded=True

    )

    actor3 = Actor.objects.create(
        full_name="Leona Lewis",
        birth_date="1908-04-25",
        nationality="UK",
        is_awarded=True

    )

    # Create Movies

    movie1 = Movie.objects.create(
        title="Inception",
        release_date="1999-04-25",
        storyline="Interesting",
        genre= "Other",
        rating=5,
        is_classic=False,
        is_awarded=True,
        director=director1,
        starring_actor=actor1,
    )
    movie1.actors.add(actor2, actor1)

    movie2 = Movie.objects.create(
        title="Titanic",
        release_date="2000-04-25",
        storyline="Sad",
        genre= "Drama",
        rating=9,
        is_classic=True,
        is_awarded=False,
        director=director2,
        starring_actor=actor3,
    )
    movie2.actors.add(actor3, actor2)

    movie3 = Movie.objects.create(
        title="No No",
        release_date="2020-04-25",
        storyline="Funny",
        genre= "Comedy",
        rating=3,
        is_classic=False,
        is_awarded=False,
        director=director3,
        starring_actor=actor2,
    )

    movie3.actors.add(actor1, actor3)


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is not None:
        query = Q(query_name)
    else:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    return '\n'.join(f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}" for d in directors)

def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ''

    return f"Top Director: {top_director.full_name}, movies: {top_director.movies_count}."

def get_top_actor():
    top_actor = Actor.objects.prefetch_related('starring_movies').annotate(
        movies_count=Count('starring_movies'),
        avg_movies_rating= Avg('starring_movies__rating')
    ).order_by('-movies_count', 'full_name').first()

    if not top_actor or not top_actor.movies_count:
        return ''

    movies = ', '.join(m.title for m in top_actor.starring_movies.all() if m)

    return (f"Top Actor: {top_actor.full_name}, starring in movies: {movies},"
            f" movies average rating: {top_actor.avg_movies_rating:.1f}")

def get_actors_by_movies_count():
    top_actors = Actor.objects.annotate(movies_count=Count('actor_movies')).order_by('-movies_count', 'full_name')[:3]
    if not top_actors or not top_actors[0].movies_count:
            return ''
    return '\n'.join(f"{a.full_name}, participated in {a.movies_count} movies" for a in top_actors)


def get_top_rated_awarded_movie():
    top_rated_movie = (Movie.objects.select_related('starring_actor')
                       .prefetch_related('actors').filter(is_awarded=True)
                       .order_by('-rating', 'title').first())
    if not top_rated_movie:
        return ''

    starring_actor = top_rated_movie.starring_actor.full_name if top_rated_movie.starring_actor else 'N/A'
    cast =', '.join(top_rated_movie.actors.order_by('full_name').values_list('full_name', flat=True))

    return (f"Top rated awarded movie: {top_rated_movie.title}, "
            f"rating: {top_rated_movie.rating:.1f}. "
            f"Starring actor: {starring_actor}. "
            f"Cast: {cast}.")


def increase_rating():
    movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)
    if not movies:
        return "No ratings increased."

    movies_count = movies.count()
    movies.update(rating= F('rating') + 0.1)

    return f"Rating increased for {movies_count} movies."
