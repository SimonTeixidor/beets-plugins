# beet-plugins

Two plugins for my personal use.

## tagsplit

Splits a tag by a separator string into multiple tags.

## discogs_extradata

Fetches extra data from discogs:

* Original year, if earlier than musicbrainz
* Label is set to label of original release
* Performers tag is populated

## Config example
```
plugins: discogs_extradata tagsplit

tagsplit:
    separator: '|'
    fields:
        - genre
        - label
        - performer

discogs_extradata:
    token: 'usertoken, can be generated in discogs settings page'
    separator: '|'
```
