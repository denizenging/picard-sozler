# Picard Sözler is a plugin that fetches lyrics from a public API.
# Copyright (C) 2024 Deniz Engin <dev@dilbil.im>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

PLUGIN_NAME = "Picard Sözler"
PLUGIN_AUTHOR = "Deniz Engin <dev@dilbil.im>"
PLUGIN_DESCRIPTION = "Sözler is a lyrics fetcher for Picard. It uses the public API provided by the lrclib.net project, which requires no registration or API keys! The API provides synced lyrics and unsynced ones as a fallback. We prioritize the syced ones. The lrclib project does not utilize MB IDs, so the results may not be as accurate. It is recommended to glimpse over your lyrics when tagging."
PLUGIN_VERSION = "0.0.2"
PLUGIN_API_VERSIONS = ["2.1"]
PLUGIN_LICENSE = "GPL-3.0-or-later"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-3.0-standalone.html"

from functools import partial
import json

from picard.metadata import register_track_metadata_processor
from picard import log

LRCLIB_HOST = "lrclib.net"
LRCLIB_PORT = 443


def log_debug(s):
    log.debug(f"{PLUGIN_NAME}: {s}")


def log_err(s):
    log.error(f"{PLUGIN_NAME}: {s}")


def process_response(album, metadata, data, reply, error):
    if error:
        album._requests -= 1
        album._finalize_loading(None)
        return

    try:
        log_debug("starting to process")
        log_debug(f"got response: {data}")
        instrumental = data.get("instrumental")
        if instrumental:
            log_debug("instrumental track; skipping")
            lyrics = None
        else:
            # Fallbacks to plain, ie, unsynced lyrics.
            lyrics = data.get("syncedLyrics") or data.get("plainLyrics")

        if lyrics is not None:
            metadata["lyrics"] = lyrics
    except AttributeError:
        log_err(f"api malformed response: {data}")
    finally:
        album._requests -= 1
        album._finalize_loading(None)


def process_track(album, metadata, track, __):
    (mins, secs) = map(int, metadata["~length"].split(":"))
    query = {
        "artist_name": metadata["albumartist"] or metadata["artist"],
        "album_name": metadata["album"],
        "track_name": metadata["title"],
        "duration": mins*60 + secs, # accepts seconds only
    }
    log_debug(f"trying to query with: {query}")
    album.tagger.webservice.get(
        LRCLIB_HOST,
        LRCLIB_PORT,
        "/api/get",
        handler=partial(process_response, album, metadata),
        parse_response_type='json',
        queryargs=query,
    )
    album._requests += 1

register_track_metadata_processor(process_track)
