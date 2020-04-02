from ..processing import clean_title


class Title(object):
    def __init__(self, title: str) -> None:
        self.title = title

    def makes_sense(self) -> bool:
        return True

    def process(self) -> str:
        return self.title


class CleanedTitle(Title):
    def makes_sense(self) -> bool:
        return clean_title(self.title) != self.title

    def process(self) -> str:
        title = clean_title(self.title)

        return title
