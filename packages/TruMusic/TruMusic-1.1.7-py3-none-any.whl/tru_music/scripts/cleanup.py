#!/usr/bin/env python
import os
import argparse

from tru_music import TruMusic


def list_str(values):
    return values.split(',')


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Run Cleanup',
    )

    parser.add_argument(
       '-d', '--dry_run',
       action='store_true',
       dest='dry_run',
       default=False,
       help='Dry run mode',
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

    return args


def main():
    exts = ['.mp3', '.m4a']
    args = parse_args()

    trumusic = TruMusic(
        lastfm_api_key=args.lastfm_api_key,
        lastfm_api_secret=args.lastfm_api_secret,
        dry_run=args.dry_run,
    )

    cwd = os.getcwd()
    for root, _, files in os.walk(cwd):
        for name in files:
            file_path = os.path.join(root, name)
            _, extension = os.path.splitext(file_path)
            file_name = os.path.basename(file_path)
            if not file_name.startswith('.') and extension in exts:
                trumusic.clean_tags(file_path)


if __name__ == '__main__':
    main()
