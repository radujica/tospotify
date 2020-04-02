import abc
from typing import Generator

from .artists import Artist
from .titles import Title

SEP_SEMICOLON = ';'
# added spaces to avoid and being inside a word, e.g. andrew
SEP_AND = ' and '
SEP_AND_SYMBOL = ' & '
TOKEN_THE = 'the '


class Query(abc.ABC):
    def __init__(self, artist: Artist, title: Title) -> None:
        self.artist = artist
        self.title = title

    def makes_sense(self) -> bool:
        return self.artist.makes_sense() and self.title.makes_sense()

    @abc.abstractmethod
    def compile(self) -> Generator[str, None, None]:
        raise NotImplementedError

    @staticmethod
    def _surround_with_quotes(s: str) -> str:
        return '\"' + s + '\"'

    @staticmethod
    def _prepare_query_component(s: str, query_type: str) -> str:
        # need to escape the quotes else requests will url-encode them
        return query_type + ':' + Query._surround_with_quotes(s)

    def _prepare_artist_component(self) -> Generator[str, None, None]:
        for artist in self.artist.process():
            yield Query._prepare_query_component(artist, 'artist')

    def _prepare_title_component(self) -> str:
        return Query._prepare_query_component(self.title.process(), 'track')


class QueryArtistTitle(Query):
    def compile(self) -> Generator[str, None, None]:
        title = self._prepare_title_component()
        for artist in self._prepare_artist_component():
            yield ' '.join([artist, 'AND', title])


class QueryWildcard(Query):
    def compile(self) -> Generator[str, None, None]:
        title = self.title.process()
        for artist in self.artist.process():
            yield Query._surround_with_quotes(artist + ' ' + title)
