#!/usr/bin/env python

import os
import sys
import glob
import argparse

from tru_music import TruMusic


def list_str(values):
    return values.split(',')


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Run TruMusic Functions',
    )

    parser.add_argument(
        '-d', '--dry_run',
        action='store_true',
        dest='dry_run',
        help='Dry run mode',
        default=False,
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        dest='quiet',
        help='All prompts are skipped and continue with defaults',
        default=False,
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='verbose',
        help='Enable verbose logging',
    )

    parser.add_argument(
        '-a', '--artist',
        dest='artist',
        help="Filter by album artist",
        type=str.lower,
    )

    parser.add_argument(
        '-t', '--title',
        dest='title',
        help="Filter by album title",
        type=str.lower,
    )

    parser.add_argument(
        '-f', '--file_format',
        dest='file_format',
        help=f"Format of the files to be uploaded. Supported file formats: {TruMusic.supported_file_extensions}",
        default='mp3',
    )

    parser.add_argument(
        '-k', '--lastfm_api_key',
        dest='lastfm_api_key',
        help="Last.fm api key",
        default=os.environ.get('LASTFM_API_KEY'),
    )

    parser.add_argument(
        '-s', '--lastfm_api_secret',
        dest='lastfm_api_secret',
        help="Last.fm api secret",
        default=os.environ.get('LASTFM_API_SECRET'),
    )

    args = parser.parse_args()

    if args.file_format not in TruMusic.supported_file_extensions:
        parser.error(f"Invalid file format specified: {args.file_format}")

    return args


def main():
    args = parse_args()

    trumusic = TruMusic(
        lastfm_api_key=args.lastfm_api_key,
        lastfm_api_secret=args.lastfm_api_secret,
        ext=f".{args.file_format}",
        dry_run=args.dry_run,
        quiet=args.quiet,
        verbose=args.verbose,
    )

    cwd = os.getcwd()

    result = True
    artist_paths = glob.glob(f"{cwd}/*")
    for artist_path in artist_paths:
        if not os.path.isdir(artist_path):
            trumusic.logger.warning(f"ARTIST NOT A PATH: {artist_path}")
            continue
        artist = os.path.basename(artist_path)
        if args.artist is not None and args.artist not in artist.lower():
            continue

        album_paths = glob.glob(f"{artist_path}/*")
        for album_path in album_paths:
            if not os.path.isdir(album_path):
                trumusic.logger.warning(f"ALBUM NOT A PATH: {album_path}")
                continue
            album = os.path.basename(album_path)
            if args.title is not None and args.title not in album.lower():
                continue
            track_files = sorted(list(map(os.path.basename, glob.glob(f"{album_path}/*{trumusic.ext}"))))
            if len(track_files) > 0:
                if not trumusic.tag_files(artist=artist, album=album, track_files=track_files):
                    result = False

    if not result:
        sys.exit(1)


if __name__ == '__main__':
    main()
