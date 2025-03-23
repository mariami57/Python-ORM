import os
import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    if search_name is not None and search_email is not None:
        authors = Author.objects.filter(full_name__icontains=search_name, email__icontains=search_email).order_by(
            '-full_name')

    elif search_name is not None:
        authors = Author.objects.filter(full_name__icontains=search_name).order_by('-full_name')

    else:
        authors = Author.objects.filter(email__icontains=search_email).order_by('-full_name')

    result = []
    [result.append(f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}") for
     a in authors if authors]

    return '\n'.join(result) if result else ''


def get_top_publisher():
    top_author = Author.objects.get_authors_by_article_count().first()

    if top_author is None or top_author.article_count == 0:
        return ''
    return f"Top Author: {top_author.full_name} with {top_author.article_count} published articles."


def get_top_reviewer():
    top_reviewer = Author.objects.annotate(num_reviews=Count('review_author')).order_by('-num_reviews', 'email').first()

    if top_reviewer is None or top_reviewer.num_reviews == 0:
        return ""
    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_reviews} published reviews."

def get_latest_article():
    latest_article = Article.objects.all().order_by('-published_on').first()

    if latest_article is None:
        return ''

    authors = ', '.join(latest_article.authors.order_by('full_name').values_list('full_name', flat=True))
    reviews = latest_article.review_article.count()
    avg_rating = latest_article.review_article.aggregate(Avg('rating'))['rating__avg'] or 0.0

    return (f"The latest article is: {latest_article.title}. "
            f"Authors: {authors}."
            f" Reviewed: {reviews} times. Average Rating: {avg_rating:.2f}.")

def get_top_rated_article():
    top_rated_article = Article.objects.annotate(avg_rating=Avg('review_article__rating')).order_by('-avg_rating', 'title').first()


    num_reviews = top_rated_article.review_article.count() if top_rated_article else 0

    if top_rated_article is None or num_reviews == 0:
        return ''

    avg_rating = top_rated_article.avg_rating or 0.0
    return f"The top-rated article is: {top_rated_article.title}, with an average rating of {avg_rating:.2f}, reviewed {num_reviews} times."

def ban_author(email=None):
    author = Author.objects.filter(email__exact=email).first()

    if author is None or email is None:
        return "No authors banned."

    num_reviews = author.review_author.count()


    author.is_banned=True
    author.save()
    author.review_author.all().delete()

    return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."

