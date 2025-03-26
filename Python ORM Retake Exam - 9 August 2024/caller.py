import os
import django
from django.db.models import Q, F, Min, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import House, Dragon, Quest


# Create queries within functions


def get_houses(search_string=None):
    if not search_string:
        return "No houses match your search."

    houses = ((House.objects
              .filter(Q(name__istartswith=search_string)
                      |
                      Q(motto__istartswith=search_string)))
              .order_by('-wins','name'))

    if not houses:
        return "No houses match your search."

    result = []
    [result.append(f"House: {house.name}, wins: {house.wins}, "
                   f"motto: {house.motto if house.motto else 'N/A'}") for house in houses]

    return "\n".join(result)

def get_most_dangerous_house():
    house = House.objects.get_houses_by_dragons_count().first()

    if house is None or house.num_dragons==0:
        return "No relevant data."

    return (f"The most dangerous house is the House of {house.name}"
            f" with {house.num_dragons} dragons. "
            f"Currently {'ruling' if house.is_ruling else 'not ruling'} the kingdom.")


def get_most_powerful_dragon():
    dragon = Dragon.objects.filter(is_healthy=True).order_by('-power', 'name').first()

    if not dragon:
        return "No relevant data."

    num_quests = dragon.quests.count()

    return (f"The most powerful healthy dragon is {dragon.name} "
            f"with a power level of {dragon.power:.1f},"
            f" breath type {dragon.breath}, "
            f"and {dragon.wins} wins, "
            f"coming from the house of {dragon.house.name}. "
            f"Currently participating in {num_quests} quests.")


def update_dragons_data():
    injured_dragons = Dragon.objects.filter(is_healthy=False, power__gt=1.0)
    dragons = injured_dragons.update(power= F('power') - 0.1,is_healthy=True)

    if dragons == 0:
        return "No changes in dragons data."

    min_power = Dragon.objects.aggregate(min_power=Min('power'))['min_power']

    return (f"The data for {dragons} dragon/s has been changed. "
            f"The minimum power level among all dragons is {min_power:.1f}")


def get_earliest_quest():
    quest=Quest.objects.order_by('start_time').first()

    if quest is None:
        return "No relevant data."

    start_time=quest.start_time
    day=start_time.day
    month=start_time.month
    year=start_time.year

    host = quest.host
    dragons = quest.dragons.order_by('-power', 'name')
    dragon_names = '*'.join([d.name for d in dragons])
    avg_power_level = dragons.aggregate(avg_power=Avg('power'))['avg_power']
    avg_power_level = f"{avg_power_level:.2f}" if avg_power_level else "0.00"



    return (f"The earliest quest is: {quest.name}, "
            f"code: {quest.code},"
            f" start date: {day}.{month}.{year},"
            f" host: {host.name}. Dragons: {dragon_names}."
            f" Average dragons power level: {avg_power_level}")


def announce_quest_winner(quest_code):
    quest = Quest.objects.filter(code=quest_code).first()

    if quest is None:
        return "No such quest."

    dragon = quest.dragons.order_by('-power', 'name').first()

    dragon.wins += 1
    dragon.save()

    winner_house = dragon.house
    winner_house.wins += 1
    winner_house.save()

    quest_name = quest.name
    quest_reward = quest.reward

    quest.delete()

    return (f"The quest: {quest_name} has been won by dragon {dragon.name}"
            f" from house {winner_house.name}. The number of wins has been updated"
            f" as follows: {dragon.wins} total wins for the dragon and"
            f" {winner_house.wins} total wins for the house. "
            f"The house was awarded with {quest_reward:.2f} coins.")

