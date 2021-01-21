import logging

import m3u8


def parse_songs(playlist_path: str) -> m3u8.SegmentList:
    """ Parse and return the songs found in the file

    :param playlist_path: absolute path of the playlist
    :type playlist_path: str
    :return:
    """
    playlist = m3u8.load(playlist_path)
    segments = playlist.segments

    if len(segments) <= 0:
        logging.error('Could not find any songs in the file!')

    return segments
