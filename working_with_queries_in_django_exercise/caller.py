import os
from typing import List

import django
from django.db.models import Case, When, Value


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# from helpers import populate_model_with_data
from main_app.models import ArtworkGallery, Laptop, OpSystemsChoices, ChessPlayer, Meal, MealTypeChoices


# Create and check models
# Run and print your queries

def show_highest_rated_art()-> str:
    highest_rating = ArtworkGallery.objects.order_by('-rating','id').first()
    return f"{highest_rating.art_name} is the highest-rated art with a {highest_rating.rating} rating!"

def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery)-> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])

def delete_negative_rated_arts() -> None:
    ArtworkGallery.objects.filter(rating__lt=0).delete()

def show_the_most_expensive_laptop()->str:
    most_expensive_laptop = Laptop.objects.order_by('-price','-id').first()
    return (f"{most_expensive_laptop.brand} is the most expensive laptop available for {most_expensive_laptop.price}$!")

def bulk_create_laptops(args: List[Laptop])-> None:
    Laptop.objects.bulk_create(args)

def update_to_512_GB_storage()-> None:
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)

def update_to_16_GB_memory()-> None:
    Laptop.objects.filter(brand__in=['Apple', 'Dell', 'Acer']).update(memory=16)

def update_operation_systems() -> None:
    Laptop.objects.update(
        operation_system=Case(
            When(brand="Asus", then=Value(OpSystemsChoices.WINDOWS)),
            When(brand="Apple", then=Value(OpSystemsChoices.MACOS)),
            When(brand__in=["Dell", "Acer"], then=Value(OpSystemsChoices.LINUX)),
            When(brand="Lenovo", then=Value(OpSystemsChoices.CHROMEOS))

        )
    )


def delete_inexpensive_laptops()-> None:
    Laptop.objects.filter(price__lt=1200).delete()

def bulk_create_chess_players(args: List[ChessPlayer])-> None:
    ChessPlayer.objects.bulk_create(args)

def delete_chess_players()-> None:
    ChessPlayer.objects.filter(title="no title").delete()

def change_chess_games_won()-> None:
    ChessPlayer.objects.filter(title="GM").update(games_won=30)

def change_chess_games_lost()-> None:
    ChessPlayer.objects.filter(title="no title").update(games_lost=25)

def change_chess_games_drawn()-> None:
    ChessPlayer.objects.update(games_drawn=10)

def grand_chess_title_GM()-> None:
    ChessPlayer.objects.filter(rating__gte=2400).update(title="GM")

def grand_chess_title_IM()-> None:
    ChessPlayer.objects.filter(rating__range=[2300, 2399]).update(title="IM")

def grand_chess_title_FM()-> None:
    ChessPlayer.objects.filter(rating__range=[2200, 2299]).update(title="FM")

def grand_chess_title_regular_player() -> None:
    ChessPlayer.objects.filter(rating__range=[0, 2199]).update(title="regular player")

def set_new_chefs() -> None:
    Meal.objects.update(
        chef=Case(
            When(meal_type=MealTypeChoices.BREAKFAST, then=Value("Gordon Ramsay")),
            When(meal_type=MealTypeChoices.LUNCH, then=Value("Julia Child")),
            When(meal_type=MealTypeChoices.DINNER, then=Value("Jamie Oliver")),
            When(meal_type=MealTypeChoices.SNACK, then=Value("Thomas Keller")),

        )
    )

def set_new_preparation_times()-> None:
    Meal.objects.update(
        preparation_time=Case(
            When(meal_type=MealTypeChoices.BREAKFAST, then=Value("10 minutes")),
            When(meal_type=MealTypeChoices.LUNCH, then=Value("12 minutes")),
            When(meal_type=MealTypeChoices.DINNER, then=Value("15 minutes")),
            When(meal_type=MealTypeChoices.SNACK, then=Value("5 minutes")),

        )
    )

def update_low_calorie_meals()-> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoices.BREAKFAST, MealTypeChoices.DINNER]).update(calories=400)

def update_high_calorie_meals()-> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoices.LUNCH, MealTypeChoices.SNACK]).update(calories=700)

def delete_lunch_and_snack_meals()-> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoices.LUNCH, MealTypeChoices.SNACK]).delete()

