import sys

import ugent_food
from ugent_food.cli.arg_parser import create_parser
from ugent_food.exceptions import ArgumentParsingException, UgentFoodException


if __name__ == "__main__":
    try:
        ugent_food.main(sys.argv[1:])
    except ArgumentParsingException as e:
        # Argparse can internally call self.error() which triggers our custom error method
        # so fake the output of the original one
        create_parser().print_usage()
        print(f"ugent-food: error: {str(e)}")
    except UgentFoodException as e:
        print(str(e))
