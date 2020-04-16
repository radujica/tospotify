from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='tospotify',
    version='0.2',
    description='Create/update a Spotify playlist from a local m3u playlist',
    url='https://github.com/radujica/tospotify',
    author='Radu Jica',
    author_email='radu.jica+code@gmail.com',
    license='GPL-3.0',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Multimedia :: Sound/Audio',
        'Operating System :: OS Independent'
    ],
    packages=['tospotify', 'tospotify.types'],
    include_package_data=True,
    zip_safe=True,
    install_requires=['spotipy', 'm3u8'],
    entry_points={
        'console_scripts': ['tospotify=tospotify.run:main'],
    }
)
