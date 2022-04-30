from ugent_food.data.enums import Message, Language, Kind

kinds: dict[Kind, dict[Language, str]] = {
    Kind.FISH: {
        Language.EN: "Fish",
        Language.NL: "Vis"
    },
    Kind.MEAT: {
        Language.EN: "Meat",
        Language.NL: "Vlees"
    },
    Kind.SOUP: {
        Language.EN: "Soup",
        Language.NL: "Soep"
    },
    Kind.VEGAN: {
        Language.EN: "Vegan",
        Language.NL: "Vegan"
    },
    Kind.VEGETARIAN: {
        Language.EN: "Vegetarian",
        Language.NL: "Vegetarisch"
    }
}


messages: dict[Message, dict[Language, str]] = {
    Message.RESTO_CLOSED: {
        Language.EN: "The restaurants are closed on {day}.",
        Language.NL: "De resto's zijn gesloten op {day}."
    },
    Message.VEGETABLES: {
        Language.EN: "Vegetables:\n{vegetables}",
        Language.NL: "Groenten:\n{vegetables}"
    }
}


class Translator:
    """Class that handles translation of messages"""
    language: Language

    def __init__(self, language: Language):
        self.language = language

    def kind(self, kind: Kind) -> str:
        """Get a translation for a meal kind in the configured language"""
        return kinds[kind][self.language]

    def message(self, message: Message, **kwargs) -> str:
        """Get a specific message in the configured language"""
        return messages[message][self.language].format(**kwargs)
