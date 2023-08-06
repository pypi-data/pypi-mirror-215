import os.path
import re
import readline  # this is imported to fix input usage
import shutil
import sys

import requests

import trulogger

import musicbrainzngs

import mutagen
from mutagen.id3 import APIC, TIT2, TALB, TPE1, TPE2, TRCK, TDRC, TPOS, TCON
from mutagen.mp4 import MP4Cover

import pylast


class TruMusic:
    supported_file_extensions = ['mp3', 'm4a']

    field_maps = {
        'MP4': {
            "artist": "\xa9ART",
            "album_artist": "aART",
            "album": "\xa9alb",
            "title": "\xa9nam",
            "year": "\xa9day",
            "track": "trkn",
            "disk": "disk",
            "cover": "covr",
        },
        "MP3": {
            "artist": TPE1,
            "album_artist": TPE2,
            "album": TALB,
            "title": TIT2,
            "year": TDRC,
            "track": TRCK,
            "disk": TPOS,
            "cover": APIC,
            # "genre": TCON,
        }
    }

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            lastfm_api_key: str,
            lastfm_api_secret: str,
            ext: str = '.mp3',
            dry_run: bool = False,
            quiet: bool = False,
            verbose: bool = False,
    ):
        musicbrainzngs.set_useragent("TruMusic", 1.0)
        if lastfm_api_key is None or lastfm_api_secret is None:
            raise pylast.PyLastError("Must provide last.fm api key and secret")
        self.ext = ext
        self.dry_run = dry_run
        self.logger = trulogger.TruLogger({'verbose': verbose})
        self.quiet = quiet

        self._image_file: str = None

        self.album_info: dict = {}

    @property
    def image_file(self):
        if self._image_file is None:
            album_art_file = f"{self.album_info['path']}/art.jpg"
            album_art_url = self.album_info['image_url']
            try:
                if album_art_url is not None:
                    req = requests.get(album_art_url, stream=True, timeout=10)
                    if req.status_code == 200:
                        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                        req.raw.decode_content = True
                        with open(album_art_file, 'wb') as file_handle:
                            shutil.copyfileobj(req.raw, file_handle)
                            self._image_file = album_art_file
            except pylast.WSError as err:
                print(err)
        return self._image_file

    @staticmethod
    def _clean_string(title):
        return re.sub(' +', ' ', re.sub('[/|⧸]', '', title))

    @staticmethod
    def _clean_search_string(title):
        return title.replace('⧸', '/')

    def _set_log_prefix(self, prefix=None):
        _prefix = ""
        if self.dry_run:
            _prefix += "[ DRY RUN ] "
        if prefix is not None:
            if isinstance(prefix, list):
                for item in prefix:
                    _prefix += f"[ {item} ] "
            elif isinstance(prefix, str):
                _prefix += f"[ {prefix} ] "
        self.logger.set_prefix(_prefix)

    def _cleanup(self):
        if self.image_file is not None and os.path.exists(self.image_file):
            os.remove(self.image_file)
            self._image_file = None
            self.album_info = {}

    # pylint: disable=too-many-branches,too-many-locals)
    def _get_album_info(self, album_artist: str, album_title: str):
        network = pylast.LastFMNetwork(
            api_key=os.environ.get('LASTFM_API_KEY', None),
            api_secret=os.environ.get('LASTFM_API_SECRET', None),
        )

        album_search = network.search_for_artist(album_artist)
        results = album_search.get_next_page()
        matching_results = []
        for res in results:
            if res.name == album_artist:
                for top_item in res.get_top_albums():
                    item = top_item.item
                    if str(item.title).casefold() == album_title.casefold():
                        try:
                            album_tracks = item.get_tracks()
                        except pylast.WSError as pye:
                            self.logger.debug(pye)
                            continue
                        release_date = None
                        mbid = item.get_mbid()
                        if mbid is not None:
                            release = musicbrainzngs.get_release_by_id(id=mbid)
                            release_date = release['release']['date']
                        # this is hacky...
                        item.release_date = release_date
                        matching_results.append(item)
                        if not self.quiet:
                            print(f"\t{len(matching_results)}. {album_artist} {item.title} ({len(album_tracks)} tracks)"
                                  f" ({item.release_date})")

        album = None
        match_count = len(matching_results)
        if match_count == 1 or (match_count > 0 and self.quiet):
            album = matching_results[0]
        elif match_count > 1:
            while album is None:
                selection = int(input(f"{match_count} matching results found; select one: ")) - 1
                if 0 <= selection < match_count:
                    album = matching_results[selection]
                else:
                    print(f"Invalid selection {selection + 1}")
        else:
            self.logger.error(f"No match found for \"{album_artist}\" - \"{album_title}\"")
            return False

        try:
            # get tracks and sort them by title length, preserving track number
            album_tracks = {num: track.title for num, track in enumerate(album.get_tracks(), start=1)}
            album_tracks_list = sorted(list(album_tracks.items()), key=lambda key: len(key[1]), reverse=True)
            album_tracks_sorted = {track[0]: {"title": self._clean_string(track[1])} for track in album_tracks_list}
            release_date = album.release_date

            if not self.quiet or release_date is None:
                rd_input = input(
                    f"Enter '{album_artist}: {album_title}' release date ({release_date or 'YYYY-MM-DD'}): "
                )
                if rd_input:
                    release_date = rd_input

            self.album_info = {
                "artist": album_artist,
                "title": self._clean_string(album_title),
                "release_date": release_date,
                "image_url": album.get_cover_image().replace("300x300", "1000x1000").replace(".png", ".jpg"),
                "tracks": album_tracks_sorted,
                "path": f"{album_artist}/{album_title}",
            }
            return True
        except AttributeError as attrerr:
            self.logger.debug(album.get_url())
            self.logger.error(attrerr)
            return False

    # pylint: disable=too-many-statements,too-many-branches,too-many-locals
    def tag_files(self, artist: str, album: str, track_files: list):
        """
        Tag audio files based on directory structure
        :param artist:
        :param album:
        :param track_files:
        :return:
        """
        self._set_log_prefix([artist, album])
        if not self._get_album_info(artist, album):
            self.logger.error("Unable to get album info")
            return False

        if len(track_files) == 0:
            self.logger.info("No tracks to tag")
            return False

        album_tags = {
            "artist": artist,
            "album": album,
            "album_artist": artist,
            "year": self.album_info['release_date'],
            "cover": self.image_file
        }

        track_count = len(self.album_info['tracks'])
        # pylint: disable=too-many-nested-blocks
        for num, track in self.album_info['tracks'].items():
            num = str(num).zfill(2)
            for track_file in track_files:
                if track["title"].lower() in self._clean_string(track_file.lower()):
                    track_file_path = f"{self.album_info['path']}/{track_file}"
                    new_track_file_path = f"{self.album_info['path']}/{num} - {track['title']}{self.ext}"
                    if track_file_path != new_track_file_path:
                        if os.path.exists(new_track_file_path):
                            self.logger.error(f"File already exists: {track_file_path}")
                        else:
                            self.logger.debug(f"RENAMING: '{track_file_path}' to '{new_track_file_path}'")
                            if self.dry_run:
                                new_track_file_path = track_file_path
                            else:
                                os.rename(track_file_path, new_track_file_path)
                    self.logger.success(f"TAGGING: {new_track_file_path}")
                    track_tags = {
                        "title": track["title"],
                        "track": (int(num), track_count),
                        "disk": (1, 1),
                    }
                    track_tags.update(album_tags)
                    track_files.remove(track_file)

                    audiofile = mutagen.File(new_track_file_path)

                    if hasattr(audiofile, "tags"):
                        del audiofile.tags
                    audiofile.add_tags()

                    file_type = audiofile.__class__.__name__
                    if file_type not in self.field_maps:
                        self.logger.error(f"Unsupported file type: {file_type}")
                        return False

                    field_map = self.field_maps[file_type]
                    for field in field_map:
                        if field in track_tags:
                            _field = field_map[field]
                            if field == "cover":
                                if os.path.exists(track_tags[field]):
                                    with open(track_tags[field], "rb") as file_handle:
                                        if file_type == "MP4":
                                            audiofile.tags[_field] = [
                                                MP4Cover(file_handle.read(), imageformat=MP4Cover.FORMAT_JPEG)
                                            ]
                                        elif file_type == "MP3":
                                            audiofile.tags.add(
                                                APIC(
                                                    mime='image/jpeg',
                                                    type=3,
                                                    desc='Cover',
                                                    data=file_handle.read()
                                                )
                                            )
                                        else:
                                            self.logger.warning(f"Unsupported file type (cover art): {file_type}")
                                else:
                                    self.logger.warning(f"Album art is missing: {track_tags[field]}")
                            else:
                                if file_type == "MP3":
                                    if field in ["track", "disk"]:
                                        track_tags[field] = f"{track_tags[field][0]}/{track_tags[field][1]}"
                                    audiofile.tags[_field] = field_map[field](encoding=3, text=track_tags[field])
                                elif file_type == "MP4":
                                    audiofile.tags[_field] = [track_tags[field]]
                        else:
                            self.logger.warning(f"Field not found in data: {field}")

                    if not self.dry_run:
                        audiofile.save()
        if len(track_files) > 0:
            print(self.album_info['tracks'])
            self.logger.warning(f"{len(track_files)} files not processed:\n{track_files}")
        self._cleanup()
        return True

    # pylint: disable=too-many-branches
    def clean_tags(self, _file_path):
        """
        Tag audio files based on directory structure
        :param _file_path:
        :return:
        """

        self.logger.info(f"CLEANING TAGS: {_file_path}")

        audiofile = mutagen.File(_file_path)

        file_type = audiofile.__class__.__name__
        if file_type not in self.field_maps:
            self.logger.error(f"Unsupported file type: {file_type}")
            return False

        field_map = self.field_maps[file_type]
        # pylint: disable=too-many-nested-blocks
        if hasattr(audiofile, "tags"):
            tags = {}
            for field, _field in field_map.items():
                if _field in audiofile.tags:
                    field_data = audiofile.tags[_field]
                    if field == "cover":
                        if file_type == "MP4":
                            audiofile.tags[_field] = [
                                MP4Cover(field_data, imageformat=MP4Cover.FORMAT_JPEG)
                            ]
                        elif file_type == "MP3":
                            tags[_field] = field_data
                            #audiofile.tags.add(
                            #    APIC(mime='image/jpeg', type=3, desc=u'Cover', data=field_data))
                        else:
                            self.logger.warning(f"Unsupported file type (cover art): {file_type}")
                    else:
                        if file_type == "MP3":
                            module = getattr(sys.modules[__name__], field_map[field])
                            if field in ["track", "disk"]:
                                if str(field_data).endswith("/0") or str(field_data).startswith("0/"):
                                    field_data = "1/1"
                            tags[_field] = module(encoding=3, text=str(field_data))
                        elif file_type == "MP4":
                            tags[_field] = [field_data]
                else:
                    self.logger.warning(f"Field not found in data: {field}/{_field}")
                    if field == "disk":
                        self.logger.info(f"Populating field with default value: {field}/{_field} :: 1/1")
                        if file_type == "MP3":
                            module = getattr(sys.modules[__name__], field_map[field])
                            tags[_field] = module(encoding=3, text="1/1")
                        elif file_type == "MP4":
                            tags[_field] = ["1/1"]
            del audiofile.tags
            audiofile.add_tags()
            for tag in tags.values():
                audiofile.tags.add(tag)
            if not self.dry_run:
                audiofile.save()
        return True
