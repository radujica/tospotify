import abc


def _prepare_search_query_component(s: str, query_type: str) -> str:
    # need to escape the quotes else requests will url-encode them
    return query_type + ':' + '\"' + s + '\"'


class Query(abc.ABC):
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title

    @staticmethod
    def makes_sense(artist, title):
        """check if this query makes sense; returns bool;
        static because attempting to avoid creating unnecessary objects"""
        raise NotImplementedError

    def compile(self):
        """Return list of queries"""
        raise NotImplementedError


class QueryArtistTitle(Query):
    @staticmethod
    def makes_sense(artist, title):
        return True

    def compile(self):
        artist = _prepare_search_query_component(self.artist, 'artist')
        title = _prepare_search_query_component(self.title, 'track')

        query = ' '.join([artist, 'AND', title])

        return [query]


class QueryTitle(Query):
    @staticmethod
    def makes_sense(artist, title):
        return True

    def compile(self):
        query = _prepare_search_query_component(self.title, 'track')

        return [query]


class QueryMultipleArtists(Query):
    @staticmethod
    def makes_sense(artist, title):
        return ';' in artist

    def compile(self):
        artists = self.artist.split(';')
        queries = []
        for artist in artists:
            query = QueryArtistTitle(artist, self.title)
            queries.append(query.compile())

        return queries


# in reversed order, so queries will be tried from right to left
# first query always tried
ADDITIONAL_QUERIES = [QueryTitle, QueryMultipleArtists]
DEFAULT_QUERY = QueryArtistTitle
