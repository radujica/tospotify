import logging
import re
from typing import Tuple


# TODO: handle utf-8 properly
def clean_name(name: str) -> str:
    # keep only ascii and extra relevant characters: \s,&()[]
    # Spotify seems to handle single quotes ' well, so can remove
    cleaned_name = re.sub(r'[^a-zA-Z0-9\s,;&()\[\]]', '', name)
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name)
    cleaned_name = cleaned_name.strip()
    cleaned_name = cleaned_name.lower()

    if len(cleaned_name) == 0:
        logging.warning('Encountered empty string after cleaning. Original string={}'.format(name))

    return cleaned_name


def process_song_name(song_name: str) -> Tuple[str, str]:
    song_split = song_name.split('-')

    if len(song_split) == 1:
        raise ProcessingException('Could not split song into artist and title! song={}'.format(song_name))
    elif len(song_split) != 2:
        logging.warning('Encountered more than 2 chunks when splitting song into artist and title. '
                        'song={}'.format(song_name))

    artist = clean_name(song_split[0])
    title = clean_name(song_split[1])

    return artist, title


class ProcessingException(Exception):
    pass
