from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='tospotify',
    version='0.1.1',
    description='Create/update a Spotify playlist from a local m3u playlist',
    url='https://github.com/radujica/tospotify',
    author='Radu Jica',
    author_email='radu.jica+code@gmail.com',
    license='GPL-3.0',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=['tospotify', 'tospotify.types'],
    include_package_data=True,
    zip_safe=True,
    install_requires=['spotipy', 'm3u8'],
    entry_points={
        'console_scripts': ['tospotify=tospotify.run:main'],
    }
)
