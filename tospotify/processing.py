import re
from typing import Tuple


# TODO: handle utf-8 properly
def clean_name(name: str) -> str:
    # keep only ascii and extra relevant characters: \s,&
    # Spotify seems to handle single quotes ' well, so can remove
    name = re.sub(r'[^a-zA-Z0-9\s,;&]', '', name)
    name = re.sub(r'\s+', ' ', name)
    name = name.strip()
    name = name.lower()

    return name


def process_song_name(song_name: str) -> Tuple[str, str]:
    song_split = song_name.split('-')

    if len(song_split) == 1:
        raise ProcessingException('Could not split song into artist and title! song={}'.format(song_name))
    elif len(song_split) != 2:
        print('Warning! Encountered more than 2 chunks when splitting song into artist and title. song={}'.format(song_name))

    artist = clean_name(song_split[0])
    title = clean_name(song_split[1])

    return artist, title


class ProcessingException(Exception):
    pass
