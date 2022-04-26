from ugent_food.data.enums import Message, Language, Kind, Type

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


types: dict[Type, dict[Language, str]] = {
    Type.MAIN: {
        Language.EN: "Main course",
        Language.NL: "Hoofdgerecht"
    },
    Type.COLD: {
        Language.EN: "Cold",
        Language.NL: "Koud"
    },
    Type.SIDE: {
        Language.EN: "Side dish",
        Language.NL: "Bijgerecht"
    }
}


messages: dict[Message, dict[Language, str]] = {
    Message.RESTO_CLOSED: {
        Language.EN: "The restaurants are closed on {day}.",
        Language.NL: "De resto's zijn gesloten op {day}."
    },
    Message.MENU_FOR: {
        Language.EN: "Menu for {weekday} {day}:",
        Language.NL: "Menu voor {weekday} {day}:"
    },
    Message.VEGETABLES: {
        Language.EN: "Vegetables:\n{vegetables}",
        Language.NL: "Groenten:\n{vegetables}"
    }
}


weekdays: dict[int, dict[Language, str]] = {
    0: {
        Language.EN: "Monday",
        Language.NL: "maandag"
    },
    1: {
        Language.EN: "Tuesday",
        Language.NL: "dinsdag"
    },
    2: {
        Language.EN: "Wednesday",
        Language.NL: "woensdag"
    },
    3: {
        Language.EN: "Thursday",
        Language.NL: "donderdag"
    },
    4: {
        Language.EN: "Friday",
        Language.NL: "vrijdag"
    },
    5: {
        Language.EN: "Saturday",
        Language.NL: "zaterdag"
    },
    6: {
        Language.EN: "Sunday",
        Language.NL: "zondag"
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

    def type(self, type_: Type) -> str:
        """Get a translation for a type in the configured language"""
        return types[type_][self.language]

    def message(self, message: Message, **kwargs) -> str:
        """Get a specific message in the configured language"""
        return messages[message][self.language].format(**kwargs)

    def weekday(self, weekday: int) -> str:
        """Get a day of the week in a configured language"""
        return weekdays[weekday][self.language]
