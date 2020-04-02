import logging
from typing import Generator


SEP_SEMICOLON = ';'
# added spaces to avoid and being inside a word, e.g. andrew
SEP_AND = ' and '
SEP_AND_SYMBOL = ' & '
TOKEN_THE = 'the '


class Artist(object):
    def __init__(self, artist: str) -> None:
        self.artist = artist

    def makes_sense(self) -> bool:
        return True

    def process(self) -> Generator[str, None, None]:
        yield self.artist


class ArtistBeginsWithThe(Artist):
    def makes_sense(self) -> bool:
        return self.artist.lower().startswith(TOKEN_THE)

    def process(self) -> Generator[str, None, None]:
        artist = self.artist[len(TOKEN_THE):]

        yield artist


class MultipleArtist(Artist):
    def __init__(self, artist: str, sep: str) -> None:
        self.sep = sep
        super().__init__(artist)

    def makes_sense(self) -> bool:
        return self.sep in self.artist.lower()


class MultipleTogetherArtist(MultipleArtist):
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
    def __init__(self, artist: str) -> None:
        super().__init__(artist, SEP_AND, SEP_AND_SYMBOL)


class MultipleTogetherAndSymbolArtist(MultipleTogetherArtist):
    def __init__(self, artist: str) -> None:
        super().__init__(artist, SEP_AND_SYMBOL, SEP_AND)


class MultipleSplitArtist(MultipleArtist):
    def process(self) -> Generator[str, None, None]:
        artists = self.artist.split(self.sep)
        for artist in artists:
            artist = artist.strip()

            if len(artist) == 0:
                logging.warning('Encountered empty string after splitting artist on {}. Original artists={}'
                                .format(self.sep, self.artist))

            yield artist


class MultipleSplitSemicolonArtist(MultipleSplitArtist):
    def __init__(self, artist: str) -> None:
        super().__init__(artist, SEP_SEMICOLON)


class MultipleSplitAndArtist(MultipleSplitArtist):
    def __init__(self, artist: str) -> None:
        super().__init__(artist, SEP_AND)


class MultipleSplitAndSymbolArtist(MultipleSplitArtist):
    def __init__(self, artist: str) -> None:
        super().__init__(artist, SEP_AND_SYMBOL)
