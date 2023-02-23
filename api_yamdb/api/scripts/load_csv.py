import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category, Genre, Title, Review, Comments, GenreTitle
from users.models import User


# class Command(BaseCommand):

def run(*args, **options):
    with open(f'{settings.BASE_DIR}/static/data/category.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            db = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            db.save()

    with open(f'{settings.BASE_DIR}/static/data/users.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            db = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            db.save()

    with open(f'{settings.BASE_DIR}/static/data/genre.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            db = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            db.save()

    with open(f'{settings.BASE_DIR}/static/data/titles.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            category = Category.objects.get(id=row['category'])
            db = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=category,
            )
            db.save()

    with open(f'{settings.BASE_DIR}/static/data/genre_title.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            title_id = Title.objects.get(id=row['title_id'])
            genre_id = Genre.objects.get(id=row['genre_id'])
            db = GenreTitle(
                id=row['id'],
                title=title_id,
                genre=genre_id
            )
            db.save()

    with open(f'{settings.BASE_DIR}/static/data/review.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            author = User.objects.get(id=row['author'])
            db = Review(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author=author,
                score=row['score'],
                pub_date=row['pub_date'],
            )
            db.save()

    with open(f'{settings.BASE_DIR}/static/data/comments.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            author = User.objects.get(id=row['author'])
            db = Comments(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author=author,
                pub_date=row['pub_date'],
            )
            db.save()
