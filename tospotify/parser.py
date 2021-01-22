import logging

import m3u8


def convert_utf8(playlist_path: str) -> str:
    """ Convert file to utf-8 after parsing with locale.getpreferredencoding

    :param playlist_path: absolute path of the playlist
    :return: Path of converted file
    """
    logging.warning('Converting file to utf-8')
    path_without_extension = playlist_path.rsplit('.', 1)[0]
    output_path = path_without_extension + '_utf8.m3u8'

    # here it uses the locale.getpreferredencoding, which could be cp1252 for Windows
    with open(playlist_path, mode='r') as input_:
        with open(output_path, encoding='utf-8', mode='w') as output_:
            for line in input_.readlines():
                output_.write(line.encode('utf-8').decode('utf-8'))

    return output_path


def parse_songs(playlist_path: str) -> m3u8.SegmentList:
    """ Parse and return the songs found in the file

    :param playlist_path: absolute path of the playlist
    :type playlist_path: str
    :return:
    """
    # m3u8 uses open(..., encoding='utf-8') which will through exception when the file cannot be parsed as utf-8
    playlist = m3u8.load(playlist_path)
    segments = playlist.segments

    if len(segments) <= 0:
        logging.error('Could not find any songs in the file!')

    return segments
