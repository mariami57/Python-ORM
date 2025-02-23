import os
from decimal import Decimal

import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character, ClassChoices


# from helpers import populate_model_with_data


def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(name=name, species=species)
    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool)  -> str:
    artifact = Artifact.objects.create(name=name, origin=origin, age=age,description = description, is_magical=is_magical)
    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str) -> None:
    if artifact.age > 250 and artifact.is_magical:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()

def show_all_locations() ->str:
    locations = Location.objects.all().order_by('-id')
    return '\n'.join(f"{l.name} has a population of {l.population}!" for l in locations)

def new_capital() -> None:
    capital = Location.objects.first()
    capital.is_capital = True
    capital.save()

def get_capitals() -> QuerySet[dict]:
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location() -> None:
    first_location = Location.objects.first()
    first_location.delete()

def apply_discount() -> None:
    cars = Car.objects.all()
    for car in cars:
        discount = Decimal(str(sum(int(d) for d in str(car.year))/ 100))
        new_price = car.price -  car.price * discount
        car.price_with_discount = new_price
        car.save()


def get_recent_cars() -> QuerySet[dict]:
    return Car.objects.filter(year__gt=2020).values('model', 'price')

def delete_last_car() -> None:
    Car.objects.last().delete()


def show_unfinished_tasks() -> str:
    unfinished_tasks = Task.objects.filter(is_finished=False)
    return '\n'.join(f"Task - {t.title} needs to be done until {t.due_date}!" for t in unfinished_tasks)

def complete_odd_tasks()-> None:
   tasks = Task.objects.all()
   for task in tasks:
       if task.id % 2 != 0:
           task.is_finished = True
           task.save()

def encode_and_replace(text: str, task_title: str)-> None:
    encoded_text = ''.join(chr(ord(c)-3) for c in text)
    Task.objects.filter(title=task_title).update(description=encoded_text)


def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    result = []
    for room in deluxe_rooms:
        if room.id % 2 == 0:
          result.append(f"Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!")

    return '\n'.join(result)

def increase_room_capacity() -> None:
    rooms = HotelRoom.objects.filter(is_reserved=True).order_by('id')
    previous_room : HotelRoom = None
    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room:
            room.capacity += previous_room.capacity
        else:
            room.capacity += room.id

        previous_room = room
        room.save()

def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()

def delete_last_room() -> None:
    last_room = HotelRoom.objects.last()
    if  not last_room.is_reserved:
        last_room.delete()

def update_characters() -> None:
    characters = Character.objects.all()
    for character in characters:
        if character.class_name == ClassChoices.MAGE:
            character.level += 3
            character.intelligence -= 7
        elif character.class_name == ClassChoices.WARRIOR:
            character.hit_points /=2
            character.dexterity += 4
        elif character.class_name == ClassChoices.ASSASSIN or character.class_name == ClassChoices.SCOUT:
            character.inventory = "The inventory is empty"


def fuse_characters(first_character: Character, second_character: Character)-> None:
    fusion_inventory = None

    if first_character.class_name in [ClassChoices.MAGE, ClassChoices.SCOUT]:
        fusion_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in [ClassChoices.WARRIOR, ClassChoices.ASSASSIN]:
        fusion_inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name = first_character.name + ' ' + second_character.name,
        class_name = ClassChoices.FUSION,
        level = (first_character.level + second_character.level) // 2,
        strength = (first_character.strength + second_character.strength) * 1.2,
        dexterity = (first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence = (first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points = (first_character.hit_points + second_character.hit_points),
        inventory = fusion_inventory,

    )

    first_character.delete()
    second_character.delete()

def grand_dexterity() -> None:
    Character.objects.update(dexterity = 30)

def grand_intelligence()-> None:
    Character.objects.update(intelligence=40)

def grand_strength() -> None:
    Character.objects.update(strength=50)

def delete_characters() -> None:
    Character.objects.filter(inventory="The inventory is empty").delete()



