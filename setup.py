from setuptools import setup

setup(
    name='beets-plugins',
    version='0.1.0',
    description='Beets plugin for splitting tags by a separator, and fetching extra discogs data.',
    long_description=open('README.md').read(),
    author='Simon Persson',
    author_email='simon@flaskpost.me',
    url='http://www.github.com/SimonPersson/beets-plugins',
    license='MIT',
    platforms='ALL',

    packages=['beetsplug'],

    install_requires=[
        'beets>=1.4.7',
        'discogs_client',
        'musicbrainzngs',
    ],

    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console'
    ],
)
