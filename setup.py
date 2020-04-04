from setuptools import setup

setup(
    name='tospotify',
    version='0.1',
    description='Create/update a Spotify playlist from a local m3u playlist',
    url='https://github.com/radujica/tospotify',
    author='Radu Jica',
    author_email='radu.jica+code@gmail.com',
    license='GPL-3.0',
    packages=['tospotify'],
    zip_safe=True,
    install_requires=['spotipy', 'm3u8'],
    entry_points={
        'console_scripts': ['tospotify=tospotify.run:main'],
    }
)
