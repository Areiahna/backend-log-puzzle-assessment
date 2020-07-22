#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
__author__ = 'Areiahna Cooks'

import argparse
import urllib.request
import sys
import re
import os

PATTERN = r'\S+puzzle\S+'


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    # +++your code here+++
    with open(filename, 'r') as f:
        puzzle_IP = f.read()
    urls = []
    matches = list(set(re.findall(PATTERN, puzzle_IP, re.DOTALL)))
    for url in matches:
        urls.append("https://code.google.com"+url)
    urls = sorted(urls, key=lambda url: url[-8:])
    return urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    images = []
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    x = 0
    for url in img_urls:
        x = x+1
        image_url = f'img{x}.jpg'
        print(f'Hacking {image_url}')
        urllib.request.urlretrieve(url, f'{dest_dir}/{image_url}')
        images.append(image_url)

    with open(f'{dest_dir}/index.html', 'w') as f:
        f.write("""
        <html> <body>
        """)

        for image in images:
            f.write(f'<img src="{image}"/>')
        f.write("""
        </body>
        </html>
        """)


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
