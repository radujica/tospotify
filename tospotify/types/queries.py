import abc
from typing import Generator

from .artists import Artist
from .titles import Title

SEP_SEMICOLON = ';'
# added spaces to avoid and being inside a word, e.g. andrew
SEP_AND = ' and '
SEP_AND_SYMBOL = ' & '
TOKEN_THE = 'the '  # nosec


class Query(abc.ABC):
    """ Abstract class for a type of query """
    def __init__(self, artist: Artist, title: Title) -> None:
        self.artist = artist
        self.title = title

    def makes_sense(self) -> bool:
        """ Checks whether it makes sense to compile a query using its artist and title

        :return: true if it makes sense, false otherwise
        :rtype: bool
        """
        return self.artist.makes_sense() and self.title.makes_sense()

    @abc.abstractmethod
    def compile(self) -> Generator[str, None, None]:
        """ Compiles a valid Spotify search query parameter.

        :return: a Spotify search query parameter
        :rtype: str
        """
        raise NotImplementedError

    @staticmethod
    def _surround_with_quotes(string: str) -> str:
        return '\"' + string + '\"'

    @staticmethod
    def _prepare_query_component(string: str, query_type: str) -> str:
        # need to escape the quotes else requests will url-encode them
        return query_type + ':' + Query._surround_with_quotes(string)

    def _prepare_artist_component(self) -> Generator[str, None, None]:
        for artist in self.artist.process():
            yield Query._prepare_query_component(artist, 'artist')

    def _prepare_title_component(self) -> str:
        return Query._prepare_query_component(self.title.process(), 'track')


class QueryArtistTitle(Query):
    """ Query which specifically looks for a given artist and a given title """
    def compile(self) -> Generator[str, None, None]:
        title = self._prepare_title_component()
        for artist in self._prepare_artist_component():
            yield ' '.join([artist, 'AND', title])


class QueryWildcard(Query):
    """ Query which lets Spotify returns its best result based on the artist and title """
    def compile(self) -> Generator[str, None, None]:
        title = self.title.process()
        for artist in self.artist.process():
            yield Query._surround_with_quotes(artist + ' ' + title)
