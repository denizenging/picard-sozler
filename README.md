# Picard Sözler
Picard Sözler is a plugin for Picard that fetches lyrics from
[the lrclib project](https://github.com/tranxuanthang/lrclib). The synced
lyrics are prioritized over the unsyced ones. The whole projecss is
automated and requires no configuration or API keys. You just pass your
files through Picard and the plugin will do the rest.

## Disclaimer
Some occosional mismatcheds or misses might happen due to the nature of
how tracks are matched against the lrclib. That project does not utilize
MusicBrainz IDs to query tracks. Instead, the names of artists, albums,
tracks, as well as the duration of the tracks are used in combination is
used to match an entry. Please see
[the lrclib API docs](https://lrclib.net/docs) for more info on the
matter. For these reasons, it is advised to skim over your lyrics.

## Installation
Download the file `picard-sozler.py` onto your computer. Then just go to
`Options > Plugins > Install plugin...` and select the downloaded file.
The `Options` menu is on the toolbar, which is normally on the top left
corner of Picard.

## Credits
- [irclib](https://github.com/tranxuanthang/lrclib): The project that
	that literally makes this all possible.
- [musixmatch plugin](https://github.com/metabrainz/picard-plugins/tree/2.0/plugins/musixmatch):
	For the mysterious part regarding the metadata writing that I
	couldn't figure out.

## License
GNU General Public License v3.0 or later. A copy is provided in the
[LICENSE.md](./LICENSE.md) file.
