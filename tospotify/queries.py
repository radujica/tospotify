import abc
import logging
from typing import List

from .processing import clean_title

# TODO: atm these presume the strings are cleaned and lowercase; improve
SEP_SEMICOLON = ';'
# added spaces to avoid and being inside a word, e.g. andrew
SEP_AND = ' and '
SEP_AND_SYMBOL = ' & '
TOKEN_THE = 'the '


class Query(abc.ABC):
    def __init__(self, artist: str, title: str) -> None:
        self.artist = artist
        self.title = title

    @abc.abstractmethod
    def makes_sense(self) -> bool:
        """check if this query makes sense; returns bool"""
        raise NotImplementedError

    @abc.abstractmethod
    def compile(self) -> List[str]:
        """Return list of queries"""
        raise NotImplementedError

    @staticmethod
    def _surround_with_quotes(s: str) -> str:
        return '\"' + s + '\"'

    @staticmethod
    def _prepare_search_query_component(s: str, query_type: str) -> str:
        # need to escape the quotes else requests will url-encode them
        return query_type + ':' + Query._surround_with_quotes(s)


class QueryArtistTitle(Query):
    def makes_sense(self) -> bool:
        return True

    def compile(self) -> List[str]:
        artist = Query._prepare_search_query_component(self.artist, 'artist')
        title = Query._prepare_search_query_component(self.title, 'track')

        query = ' '.join([artist, 'AND', title])

        return [query]


class QueryArtistCleanedTitle(QueryArtistTitle):
    # TODO: don't like cleaning twice
    def makes_sense(self) -> bool:
        return clean_title(self.title) != self.title

    def compile(self) -> List[str]:
        self.title = clean_title(self.title)

        return super().compile()


class QueryArtistTitleMightClean(QueryArtistTitle):
    def compile(self) -> List[str]:
        queries = []
        query_title_cleaned = QueryArtistCleanedTitle(self.artist, self.title)
        if query_title_cleaned.makes_sense():
            queries = queries + query_title_cleaned.compile()

        return super().compile() + queries


class QueryWildcard(Query):
    def makes_sense(self) -> bool:
        return True

    def compile(self) -> List[str]:
        return [Query._surround_with_quotes(self.artist + ' ' + self.title)]


# TODO: need to refactor these classes. This is the same code as QueryArtistCleanedTitle
class QueryWildcardCleanTitle(QueryWildcard):
    def makes_sense(self) -> bool:
        return clean_title(self.title) != self.title

    def compile(self) -> List[str]:
        self.title = clean_title(self.title)

        return super().compile()


class QueryMultipleArtist(Query):
    def __init__(self, artist, title, sep):
        self.sep = sep
        super().__init__(artist, title)

    def makes_sense(self) -> bool:
        return self.sep in self.artist

    def compile(self) -> List[str]:
        artists = self.artist.split(self.sep)
        queries = []
        for artist in artists:
            artist = artist.strip()

            if len(artist) == 0:
                logging.warning('Encountered empty string after splitting artist on {}. Original artists={}'
                                .format(self.sep, self.artist))

            query = QueryArtistMightBeginWithTheTitle(artist, self.title).compile()
            queries = queries + query

        return queries


class QuerySplitMultipleArtists(QueryMultipleArtist):
    def __init__(self, artist, title):
        super().__init__(artist, title, SEP_SEMICOLON)


class QuerySplitAndArtists(QueryMultipleArtist):
    def __init__(self, artist, title):
        super().__init__(artist, title, SEP_AND)


class QuerySplitAndSymbolArtists(QueryMultipleArtist):
    def __init__(self, artist, title):
        super().__init__(artist, title, SEP_AND_SYMBOL)


# TODO: perhaps do more recursively,
#  e.g. for Sting & The Police also try Sting and Police, not only Sting and The Police
class QueryTogetherArtist(QueryMultipleArtist):
    def __init__(self, artist, title, sep, to_sep):
        self.to_sep = to_sep
        super().__init__(artist, title, sep)

    def compile(self) -> List[str]:
        artist = self.artist.replace(self.sep, self.to_sep, 1)
        if self.sep in artist:
            logging.warning('Encountered more than 2 occurrences of sep={} when detecting artist '
                            'as multiple artists. artist={}'.format(self.sep, self.artist))
        query = QueryArtistMightBeginWithTheTitle(artist, self.title).compile()

        return query


class QueryMultipleAndArtists(QueryTogetherArtist):
    def __init__(self, artist, title):
        super().__init__(artist, title, SEP_AND, SEP_AND_SYMBOL)


class QueryMultipleAndSymbolArtists(QueryTogetherArtist):
    def __init__(self, artist, title):
        super().__init__(artist, title, SEP_AND_SYMBOL, SEP_AND)


class QueryArtistBeginsWithThe(QueryArtistTitleMightClean):
    def makes_sense(self) -> bool:
        return self.artist.startswith(TOKEN_THE)

    def compile(self) -> List[str]:
        self.artist = self.artist.replace(TOKEN_THE, '', 1)

        return super().compile()


class QueryArtistMightBeginWithTheTitle(QueryArtistTitleMightClean):
    def compile(self) -> List[str]:
        queries = []
        query_without_the = QueryArtistBeginsWithThe(self.artist, self.title)
        if query_without_the.makes_sense():
            queries = queries + query_without_the.compile()

        return super().compile() + queries


# default query always tried
DEFAULT_QUERY = QueryArtistMightBeginWithTheTitle
# in reversed order, so queries will be tried bottom up
ADDITIONAL_QUERIES = [
    QueryWildcardCleanTitle,
    QueryWildcard,
    QuerySplitAndSymbolArtists,
    QuerySplitAndArtists,
    QueryMultipleAndSymbolArtists,
    QueryMultipleAndArtists,
    QuerySplitMultipleArtists
]
