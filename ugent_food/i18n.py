from ugent_food.data.enums import Message, Language


messages: dict[Message, dict[Language, str]] = {
    Message.RESTO_CLOSED: {
        Language.EN: "The restaurants are closed on {day}.",
        Language.NL: "De resto's zijn gesloten op {day}."
    },
    Message.SOUP: {
        Language.EN: "Soup:\n {soup}",
        Language.NL: "Soep:\n {soup}"
    }
}


class Translator:
    """Class that handles translation of messages"""
    language: Language

    def __init__(self, language: Language):
        self.language = language

    def message(self, message: Message, **kwargs) -> str:
        """Get a specific message in the configured language"""
        return messages[message][self.language].format(**kwargs)
