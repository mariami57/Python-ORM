import os
import django
from django.db.models import Q, Count, Sum, F, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Status, Spacecraft


# Create queries within functions
def get_astronauts(search_string=None):
    if search_string is None:
        return ''

    astrounauts = (Astronaut.objects
                   .filter(Q(name__icontains=search_string)
                            |
                            Q(phone_number__icontains=search_string))).order_by('name')


    result = []

    [result.append(f"Astronaut: {a.name}, phone number: {a.phone_number}, status: "
               f"{'Active' if a.is_active else 'Inactive'}") for a in astrounauts if astrounauts]

    return '\n'.join(result) if result else ''

def get_top_astronaut():
    top_astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if  top_astronaut is None or top_astronaut.num_missions == 0:
        return "No data."

    return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.num_missions} missions."

def get_top_commander():
    top_commander = Astronaut.objects.annotate(num_commanded_missions=Count('commanded_missions')).order_by('-num_commanded_missions', 'phone_number').first()

    if top_commander and top_commander.num_commanded_missions > 0:
        return f"Top Commander: {top_commander.name} with {top_commander.num_commanded_missions} commanded missions."
    else:
        return "No data."


def get_last_completed_mission():
    mission = Mission.objects\
        .filter(status='Completed')\
        .select_related('spacecraft', 'commander')\
        .prefetch_related('astronauts').order_by('launch_date').last()

    commander_name = mission.commander.name if mission.commander else "TBA"
    astronauts = mission.astronauts.all().order_by('name')
    astronaut_names = ', '.join(a.name for a in astronauts)
    total_spacewalks = mission.astronauts.aggregate(total=Sum('spacewalks'))['total']
    spacecraft_name = mission.spacecraft.name

    if not mission:
        return "No data."

    return (f"The last completed mission is: {mission.name}."
            f" Commander: {commander_name}. Astronauts: {astronaut_names}. "
            f"Spacecraft: {spacecraft_name}. Total spacewalks: {total_spacewalks}.")



def get_most_used_spacecraft():
    spacecraft= (((Spacecraft.objects
                 .annotate(missions_spacecraft=Count('used_in_missions', distinct=True)))
                 .annotate(num_astronauts=Count('used_in_missions__astronauts', distinct=True)))
                 .order_by('-missions_spacecraft', 'name').first())


    if not spacecraft or spacecraft.missions_spacecraft == 0:
        return "No data."

    return (f"The most used spacecraft is: {spacecraft.name}, manufactured by {spacecraft.manufacturer},"
            f" used in {spacecraft.missions_spacecraft} missions, astronauts on missions: {spacecraft.num_astronauts}.")

def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects.filter(
        used_in_missions__status='Planned',
        weight__gte=200.0
    ).distinct()

    if not spacecrafts:
        return "No changes in weight."

    num_of_spacecrafts_affected = spacecrafts.update(weight=F('weight') - 200.0)
    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']

    return (f"The weight of {num_of_spacecrafts_affected} spacecrafts has been decreased."
            f" The new average weight of all spacecrafts is {avg_weight}kg")


