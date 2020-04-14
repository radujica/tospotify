import logging
import re
from typing import Tuple


MIN_LENGTH_NAME = 3


def clean_title(title: str) -> str:
    """ Clean a song title:

    - remove brackets and text within ()[] brackets, e.g. [acoustic]
    - remove text (and including) feat. or featuring or ft.
    - strip the remaining whitespaces

    :param title: song title to clean
    :type title: str
    :return: cleaned song title
    :rtype: str
    """
    cleaned_title = re.sub(r'\([^)]*\)|\[[^)]*\]', '', title)
    cleaned_title = re.sub(r'(\sfeat\..*)|(\sfeaturing.*)|(\sft\..*)', '', cleaned_title)
    cleaned_title = cleaned_title.strip()

    return cleaned_title


def clean_name(name: str) -> str:
    """ Clean either artist or title:

    - keep only ascii and some relevant characters: \\,&()[]
    - note that single quotes are also removed since Spotify seems to handle those well
    - strip and lowercase

    :param name: artist or song title to clean
    :type name: str
    :return: cleaned name
    :rtype: str
    """
    cleaned_name = re.sub(r'[^a-zA-Z0-9\s,;&()\[\]]', '', name)
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name)
    cleaned_name = cleaned_name.strip()
    cleaned_name = cleaned_name.lower()

    if len(cleaned_name) == 0:
        logging.warning('Encountered empty string after cleaning. Original string={}'.format(name))

    return cleaned_name


def process_song_name(song_name: str) -> Tuple[str, str]:
    """ Splits m3u line of artist - title and cleans using clean_name

    :param song_name:
    :type song_name: str
    :return: tuple of artist and title
    :rtype: (str, str)
    """
    song_split = song_name.split('-')

    if len(song_split) == 1:
        raise ProcessingException('Could not split song into artist and title! song={}'.format(song_name))

    if len(song_split) != 2:
        logging.warning('Encountered more than 2 chunks when splitting song into artist and title. '
                        'song={}'.format(song_name))

    artist = clean_name(song_split[0])
    title = clean_name(song_split[1])

    return artist, title


class ProcessingException(Exception):
    """ Custom exception for errors in processing the data """
