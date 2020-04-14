import logging
from typing import Generator

from ..processing import MIN_LENGTH_NAME


SEP_SEMICOLON = ';'
# added spaces to avoid and being inside a word, e.g. andrew
SEP_AND = ' and '
SEP_AND_SYMBOL = ' & '
TOKEN_THE = 'the '  # nosec


class Artist:
    """ Base class for an Artist """
    def __init__(self, artist: str) -> None:
        self.artist = artist

    def makes_sense(self) -> bool:  # pylint: disable=no-self-use
        """ Checks whether it makes sense to compile a query given this artist

        :return: True if a query would make sense, False otherwise
        :rtype: bool
        """
        return True

    def process(self) -> Generator[str, None, None]:
        """ Processes the artist according to the implemented rules.
        Note it might result in multiple titles to try.

        :return: processed title
        :rtype: str
        """
        yield self.artist


class ArtistBeginsWithThe(Artist):
    """ Artist class which will clean "the" from the artist name if it begins as such,
    e.g. The Gipsy Kings -> Gipsy Kings
    """
    def makes_sense(self) -> bool:
        return self.artist.lower().startswith(TOKEN_THE)

    def process(self) -> Generator[str, None, None]:
        artist = self.artist[len(TOKEN_THE):]

        if len(artist) < MIN_LENGTH_NAME:
            logging.warning('Encountered artist after removing "the" with '
                            'too short name={}'.format(artist))

        yield artist


class MultipleArtist(Artist):
    """ Base class for an Artist actually containing multiple artists separated by some separator """
    def __init__(self, artist: str, sep: str) -> None:
        self.sep = sep
        super().__init__(artist)

    def makes_sense(self) -> bool:
        return self.sep in self.artist.lower()


class MultipleTogetherArtist(MultipleArtist):
    """ MultipleArtist class which will try converting the separator to another separator,
    e.g. Sting & The Police -> Sting and The Police
    """
    def __init__(self, artist: str, sep: str, to_sep: str) -> None:
        self.to_sep = to_sep
        super().__init__(artist, sep)

    def process(self) -> Generator[str, None, None]:
        artist = self.artist.replace(self.sep, self.to_sep, 1)
        if self.sep in artist:
            logging.warning('Encountered more than 2 occurrences of sep={} when detecting artist '
                            'as multiple artists. artist={}'.format(self.sep, self.artist))

        yield artist


class MultipleTogetherAndArtist(MultipleTogetherArtist):
    """ MultipleTogetherArtist class where separator is "and" """
    def __init__(self, artist: str) -> None:
        super().__init__(artist, SEP_AND, SEP_AND_SYMBOL)


class MultipleTogetherAndSymbolArtist(MultipleTogetherArtist):
    """ MultipleTogetherArtist class where separator is "&" """
    def __init__(self, artist: str) -> None:
        super().__init__(artist, SEP_AND_SYMBOL, SEP_AND)


class MultipleSplitArtist(MultipleArtist):
    """ MultipleArtist class which will try splitting the artist string into its actual artists,
    e.g. Sting & The Police -> Sting, The Police
    """
    def process(self) -> Generator[str, None, None]:
        artists = self.artist.split(self.sep)
        for artist in artists:
            artist = artist.strip()

            if len(artist) < MIN_LENGTH_NAME:
                logging.warning('Encountered artist after splitting on={} '
                                'with too short name={}'.format(self.sep, artist))

            yield artist


class MultipleSplitSemicolonArtist(MultipleSplitArtist):
    """ MultipleSplitArtist class where separator is ";" """
    def __init__(self, artist: str) -> None:
        super().__init__(artist, SEP_SEMICOLON)


class MultipleSplitAndArtist(MultipleSplitArtist):
    """ MultipleSplitArtist class where separator is "and" """
    def __init__(self, artist: str) -> None:
        super().__init__(artist, SEP_AND)


class MultipleSplitAndSymbolArtist(MultipleSplitArtist):
    """ MultipleSplitArtist class where separator is "&" """
    def __init__(self, artist: str) -> None:
        super().__init__(artist, SEP_AND_SYMBOL)
