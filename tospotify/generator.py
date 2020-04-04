from typing import Tuple, Type, Generator

from .types.artists import (
    Artist,
    ArtistBeginsWithThe,
    MultipleTogetherAndArtist,
    MultipleTogetherAndSymbolArtist,
    MultipleSplitSemicolonArtist,
    MultipleSplitAndArtist,
    MultipleSplitAndSymbolArtist
)
from .types.queries import Query, QueryArtistTitle, QueryWildcard
from .types.titles import Title, CleanedTitle

ARTIST_POOL = (Artist, ArtistBeginsWithThe, MultipleTogetherAndArtist, MultipleTogetherAndSymbolArtist,
               MultipleSplitSemicolonArtist, MultipleSplitAndArtist, MultipleSplitAndSymbolArtist)
TITLE_POOL = (Title, CleanedTitle)
QUERY_POOL = (QueryArtistTitle, QueryWildcard)


class QueryGenerator:
    """ Generator of relevant queries for a artist-title pair """
    def __init__(
            self,
            artist: str,
            title: str,
            queries: Tuple[Type[Query]] = QUERY_POOL,
            artists: Tuple[Type[Artist]] = ARTIST_POOL,
            titles: Tuple[Type[Title]] = TITLE_POOL
    ) -> None:
        self.artist = artist
        self.title = title
        self.queries = queries
        self.artists = artists
        self.titles = titles

    def generate(self) -> Generator[str, None, None]:
        """ Return a query at a time if it would make sense to execute

        :return: query as a string
        :rtype: str
        """
        for q_class in self.queries:
            for a_class in self.artists:
                artist = a_class(self.artist)
                for t_class in self.titles:
                    title = t_class(self.title)
                    query = q_class(artist, title)
                    if query.makes_sense():
                        for query2 in query.compile():
                            yield query2
