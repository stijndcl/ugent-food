from ugent_food.api.models import Meal


def test_meal_creation(create_model):
    create_model(
        Meal, {"allergens": [], "kind": "soup", "name": "Carrot soup: 350 ml", "price": "€ 1,00", "type": "side"}
    )


def test_meal_creation_prepend_price(create_model):
    meal = create_model(
        Meal, {"allergens": [], "kind": "soup", "name": "Carrot soup: 350 ml", "price": "1,00", "type": "side"}
    )

    assert meal.price == "€ 1,00"
