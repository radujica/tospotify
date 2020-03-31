import abc


class Query(abc.ABC):
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title

    def makes_sense(self):
        """check if this query makes sense; returns bool"""
        raise NotImplementedError

    def compile(self):
        """Return list of queries"""
        raise NotImplementedError

    @staticmethod
    def _prepare_search_query_component(s: str, query_type: str) -> str:
        # need to escape the quotes else requests will url-encode them
        return query_type + ':' + '\"' + s + '\"'


class QueryArtistTitle(Query):
    def makes_sense(self):
        return True

    def compile(self):
        artist = Query._prepare_search_query_component(self.artist, 'artist')
        title = Query._prepare_search_query_component(self.title, 'track')

        query = ' '.join([artist, 'AND', title])

        return [query]


class QueryTitle(Query):
    def makes_sense(self):
        return True

    def compile(self):
        query = Query._prepare_search_query_component(self.title, 'track')

        return [query]


class QueryMultipleArtists(Query):
    def makes_sense(self):
        return ';' in self.artist

    def compile(self):
        artists = self.artist.split(';')
        queries = []
        for artist in artists:
            query = QueryArtistTitle(artist, self.title)
            queries.append(query.compile()[0])

        return queries


# in reversed order, so queries will be tried from right to left
# first query always tried
ADDITIONAL_QUERIES = [QueryTitle, QueryMultipleArtists]
DEFAULT_QUERY = QueryArtistTitle
