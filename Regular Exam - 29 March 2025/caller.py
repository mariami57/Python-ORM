import os
import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Publisher, Author, Book
# Create queries within functions
def populate_db():
    publisher1 = Publisher.objects.create(
        name="Epic Reads",
        country="US",
        established_date='1923-05-15',
        rating=4.94
    )
    publisher2 = Publisher.objects.create(
        name="Global Prints",
        country="AU",
    )
    publisher3 = Publisher.objects.create(
        name="Abrams Books",
        rating=1.05,
    )


    author1 = Author.objects.create(
        name="Jack London",
        country="US",
        birth_date='1876-01-12',
        is_active=False,
    )

    author2 = Author.objects.create(
        name="Craig Richardson",
    )
    author3 = Author.objects.create(
        name="Ramsey Hamilton",
    )



    book1 = Book.objects.create(
        title="Adventures in Python",
        publication_date='2015-06-01',
        publisher=publisher1,
        main_author=author2,
        rating=4.8,
        price=49.99
    )

    book1.co_authors.add(author3)

    book2 = Book.objects.create(
        title="The Call of the Wild",
        publication_date='1903-11-23',
        publisher=publisher2,
        main_author=author1,
        rating=4.9,
        price=29.99
    )

    book3 = Book.objects.create(
        title="Django World",
        publication_date='2025-01-01',
        publisher=publisher1,
        main_author=author2,
        rating=5.0,
        price=89.99
    )

    book3.co_authors.add(author3)


def get_publishers(search_string=None):
    if search_string is None:
        return "No search criteria."

    publishers = Publisher.objects.filter(
        Q(name__icontains=search_string) | Q(country__icontains=search_string)
    ).order_by('-rating', 'name')

    if not publishers:
        return "No publishers found."

    return '\n'.join(f"Publisher: {p.name}, country: {p.country if p.country !='TBC' else 'Unknown'}, rating: {p.rating:.1f}" for p in publishers)


def get_top_publisher():
    top_publisher=Publisher.objects.get_publishers_by_books_count().first()

    if not top_publisher:
        return "No publishers found."

    return f"Top Publisher: {top_publisher.name} with {top_publisher.books_count} books."


def get_top_main_author():
    top_main_author = (Author.objects.prefetch_related('main_author').annotate(num_books=Count('main_author')).order_by('-num_books','name').first())

    if not top_main_author or not top_main_author.main_author.exists():
        return "No results."

    books = Book.objects.filter(main_author=top_main_author).values_list('title', flat=True)
    avg_rating = Book.objects.filter(main_author=top_main_author).aggregate(avg_rating=Avg('rating'))['avg_rating']


    return f"Top Author: {top_main_author.name}, own book titles: {', '.join([b for b in books.order_by('title')])}, books average rating: {avg_rating:.1f}"



def get_authors_by_books_count():
    authors = Author.objects.annotate(
        main_author_count=Count('main_author'),
        coauthor_count=Count('co_authors',distinct=True),
        total_books= Count('main_author') + Count('co_authors', distinct=True),
    ).order_by('-total_books', 'name')[:3]

    if not authors or not Book.objects.exists():
        return "No results."

    return '\n'.join(f"{a.name} authored {a.total_books} books." for a in authors)


def get_top_bestseller():
    top_bestseller = Book.objects.filter(is_bestseller=True).order_by('-rating', 'title').first()
    if not top_bestseller:
        return "No results."

    co_authors = ', '.join(ca.name for ca in top_bestseller.co_authors.all().order_by('name'))

    return f"Top bestseller: {top_bestseller.title}, rating: {top_bestseller.rating:.1f}. Main author: {top_bestseller.main_author.name}. Co-authors: {co_authors if co_authors else 'N/A'}."

def increase_price():
    books = Book.objects.filter(publication_date__year=2025, rating__gte=4.0)

    if not books:
        return "No changes in price."

    num_of_updated_books = books.update(price=F('price')*1.2)

    return f"Prices increased for {num_of_updated_books} books."

