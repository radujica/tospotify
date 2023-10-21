from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='tospotify',
    version='0.3.2',
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Multimedia :: Sound/Audio',
        'Operating System :: OS Independent'
    ],
    packages=['tospotify', 'tospotify.types'],
    include_package_data=True,
    zip_safe=True,
    install_requires=['spotipy>=2.11.1', 'm3u8>=0.7.1,<3.5'],
    entry_points={
        'console_scripts': ['tospotify=tospotify.run:main'],
    }
)
