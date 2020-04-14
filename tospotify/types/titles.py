import logging

from ..processing import clean_title, MIN_LENGTH_NAME


class Title:
    """ Base class for a song title """
    def __init__(self, title: str) -> None:
        self.title = title

    def makes_sense(self) -> bool:  # pylint: disable=no-self-use
        """ Checks whether it makes sense to compile a query given this song title

        :return: True if a query would make sense, False otherwise
        :rtype: bool
        """
        return True

    def process(self) -> str:
        """ Processes the title according to the implemented rules.

        :return: processed title
        :rtype: str
        """
        return self.title


class CleanedTitle(Title):
    """ Title class which will clean the song title if it makes sense,
    e.g. Every breath feat. Sting -> Every breath
    """
    def makes_sense(self) -> bool:
        return clean_title(self.title) != self.title

    def process(self) -> str:
        title = clean_title(self.title)

        if len(title) < MIN_LENGTH_NAME:
            logging.warning('Encountered title after cleaning with too short name={}'.format(title))

        return title
