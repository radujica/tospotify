import abc
from typing import List


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


class QueryMultipleArtists(Query):
    def makes_sense(self) -> bool:
        return ';' in self.artist

    def compile(self) -> List[str]:
        artists = self.artist.split(';')
        queries = []
        for artist in artists:
            query = QueryArtistTitle(artist, self.title)
            queries.append(query.compile()[0])

        return queries


# in reversed order, so queries will be tried from right to left
# first query always tried
ADDITIONAL_QUERIES = [QueryWildcard, QueryTitle, QueryMultipleArtists]
DEFAULT_QUERY = QueryArtistTitle
