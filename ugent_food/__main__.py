import sys

import ugent_food
from ugent_food.exceptions import UgentFoodException


if __name__ == "__main__":
    try:
        ugent_food.main(sys.argv[1:])
    except UgentFoodException as e:
        print(str(e))
