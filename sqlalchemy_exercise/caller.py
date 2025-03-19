from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from helpers import handle_session
from models import Recipe, Chef

engine = create_engine('postgresql+psycopg2://postgres-user:password@localhost/sqlalchemy_db')
Session = sessionmaker(bind=engine)

session = Session()

@handle_session(session)
def create_recipe(name: str, ingredients: str, instructions: str):
    new_recipe = Recipe(name=name, ingredients=ingredients, instructions=instructions)
    session.add(new_recipe)


@handle_session(session)
def update_recipe_by_name(name: str, new_name: str,  new_ingredients: str, new_instructions: str):
    session.query(Recipe).filter_by(name=name).update({Recipe.name: new_name, Recipe.ingredients: new_ingredients,
                   Recipe.instructions: new_instructions})


@handle_session(session)
def delete_recipe_by_name(name: str):
    session.query(Recipe).filter_by(name=name).delete()


@handle_session(session)
def get_recipes_by_ingredient(ingredient_name: str):
    return session.query(Recipe).filter(Recipe.ingredients.ilike(f"%{ingredient_name}%")).all()

@handle_session(session)
def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name: str):
        first_recipe = session.query(Recipe).filter_by(name=first_recipe_name).with_for_update().one()
        second_recipe = session.query(Recipe).filter_by(name=second_recipe_name).with_for_update().one()

        first_recipe.ingredients, second_recipe.ingredients = second_recipe.ingredients, first_recipe.ingredients



@handle_session(session)
def relate_recipe_with_chef_by_name(recipe_name: str, chef_name: str):
    recipe = session.query(Recipe).filter_by(name=recipe_name).one()

    if recipe.chef:
        raise Exception(f"Recipe: {recipe.name} already has a related chef")

    chef = session.query(Chef).filter_by(name=chef_name).one()
    recipe.chef = chef

    return f"Related recipe {recipe.name} with chef {chef.name}"

@handle_session(session)
def get_recipes_with_chef():
    recipes_with_chef = session.query(Recipe.name, Chef.name).join(Chef, Recipe.chef).all()

    return  '\n'.join(
        f"Recipe: {recipe_name} made by chef: {chef_name}" for recipe_name, chef_name in recipes_with_chef
    )


