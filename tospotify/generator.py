from typing import Tuple, Type

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


class QueryGenerator(object):
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

    def generate(self) -> str:
        for q in self.queries:
            for a in self.artists:
                artist = a(self.artist)
                for t in self.titles:
                    title = t(self.title)
                    query = q(artist, title)
                    if query.makes_sense():
                        for query2 in query.compile():
                            yield query2
