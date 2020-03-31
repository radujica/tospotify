import abc
from typing import List


SEP_SEMICOLON = ';'
SEP_AND = ' and '
SEP_AND_SYMBOL = ' & '


class Query(abc.ABC):
    def __init__(self, artist: str, title: str) -> None:
        self.artist = artist
        self.title = title

    def makes_sense(self) -> bool:
        """check if this query makes sense; returns bool"""
        raise NotImplementedError

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


class QueryTitle(Query):
    def makes_sense(self) -> bool:
        return True

    def compile(self) -> List[str]:
        query = Query._prepare_search_query_component(self.title, 'track')

        return [query]


class QueryWildcard(Query):
    def makes_sense(self) -> bool:
        return True

    def compile(self) -> List[str]:
        return [Query._surround_with_quotes(self.artist + ' ' + self.title)]


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
            query = QueryArtistTitle(artist, self.title)
            queries.append(query.compile()[0])

        return queries


class QuerySplitMultipleArtists(QueryMultipleArtist):
    def __init__(self, artist, title):
        super().__init__(artist, title, SEP_SEMICOLON)


class QuerySplitAndArtists(QueryMultipleArtist):
    def __init__(self, artist, title):
        # added spaces to avoid and being inside a word, e.g. andrew
        super().__init__(artist, title, SEP_AND)


class QuerySplitAndSymbolArtists(QueryMultipleArtist):
    def __init__(self, artist, title):
        super().__init__(artist, title, SEP_AND_SYMBOL)


class QueryTogetherArtist(QueryMultipleArtist):
    def __init__(self, artist, title, sep, to_sep):
        self.to_sep = to_sep
        super().__init__(artist, title, sep)

    def compile(self) -> List[str]:
        artist = self.artist.replace(self.sep, self.to_sep, 1)
        if self.sep in artist:
            print('Warning! Encountered more than 2 occurrence of sep={} when detecting artist as multiple artists. '
                  'artist={}'.format(self.sep, self.artist))
        query = QueryArtistTitle(artist, self.title).compile()[0]

        return [query]


class QueryMultipleAndArtists(QueryTogetherArtist):
    def __init__(self, artist, title):
        super().__init__(artist, title, SEP_AND, SEP_AND_SYMBOL)


class QueryMultipleAndSymbolArtists(QueryTogetherArtist):
    def __init__(self, artist, title):
        super().__init__(artist, title, SEP_AND_SYMBOL, SEP_AND)


# first query always tried
DEFAULT_QUERY = QueryArtistTitle
# in reversed order, so queries will be tried bottom up
ADDITIONAL_QUERIES = [
    QueryWildcard,
    QueryTitle,
    QuerySplitAndArtists,
    QuerySplitAndSymbolArtists,
    QueryMultipleAndSymbolArtists,
    QueryMultipleAndArtists,
    QuerySplitMultipleArtists
]
