#!/usr/bin/env python3

"""
CSCI 4555: Neural Networks and Machine Learning
Spring 2022
University of Minnesota Morris
Joe Walbran and Natasha Zebrev

Given the Million Song Dataset exported to CSV, read the LastFM genre tags
database, and output a new CSV file with several new columns added.

We add a new column for each of the following genres:
 - Rock
 - Pop
 - Electronic
 - Jazz
 - Metal
 - RAndB
 - Folk
 - HipHop
which correspond to some of the more popular genre tags in the database.

The value of this field is eiter 1, if the song has that tag, or 0, if it
doesn't.

If a song isn't listed in the LastFM genre tags database, we'll drop that row
from the output CSV.

Usage: ./add-genre-tags-to-csv.py [SongCSV.csv file] [lastfm_tags.db file] >output.csv
"""

import collections
import csv
import sqlite3
import sys

Genre = collections.namedtuple('Genre', 'name_in_output names_in_database')

GENRES = [
    Genre('Rock', [
        'rock',
        'classic rock',
        'alternative rock',
        'indie rock',
        'punk',
        'hard rock',
        'punk rock',
        'pop rock',
        'soft rock',
        'blues rock',
        'rock n roll',
        'folk rock',
        'Psychedelic Rock',
        'Rock and Roll',
        'Alternative Punk',
        'Grunge',
        'pop punk',
        'post-rock',
        'Garage Rock',
        'glam rock',
        'rockabilly',
        'Pop-Rock',
        'shoegaze',
        'Gothic Rock',
        'alt rock',
        'folk-rock',
    ]),
    Genre('Pop', [
        'pop',
        'indie pop',
        'pop rock',
        'new wave',
        'britpop',
        'synthpop',
        'electropop',
        'pop punk',
        'synth pop',
        'Pop-Rock',
    ]),
    Genre('Electronic', [
        'electronic',
        'electronica',
        'electro',
        'House',
        'trance',
        'techno',
        'club',
        'electropop',
        'idm',
        'progressive trance',
        'indietronica',
    ]),
    Genre('Jazz', [
        'jazz',
        'Smooth jazz',
        'jazzy',
        'acid jazz',
        'swing',
        'nu jazz',
    ]),
    Genre('Metal', [
        'metal',
        'heavy metal',
        'death metal',
        'Progressive metal',
        'metalcore',
        'thrash metal',
        'black metal',
        'Power metal',
        'Melodic death metal',
        'alternative metal',
        'Gothic Metal',
        'melodic metal',
        'doom metal',
        'Nu Metal',
    ]),
    Genre('RAndB', [
        'soul',
        'funk',
        'rnb',
        'Disco',
        'rhythm and blues',
        'r&b',
        'RB',
        'motown',
        'r and b',
    ]),
    Genre('Folk', [
        'folk',
        'folk rock',
        'irish',
        'celtic',
        'folk-rock',
    ]),
    Genre('HipHop', [
        'Hip-Hop',
        'rap',
        'hip hop',
        'hiphop',
    ]),
]

def is_track_in_database(track_id, db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM tids WHERE tid = :track_id', {
        'track_id': track_id,
    })
    return cursor.fetchone() is not None

def does_track_have_genre(track_id, genre, db_connection):
    cursor = db_connection.cursor()
    for tag_name in genre.names_in_database:
        cursor.execute('''
            SELECT * FROM tid_tag
            JOIN tids ON tid_tag.tid = tids.ROWID
            JOIN tags ON tid_tag.tag = tags.ROWID
            WHERE tids.tid = :track_id
              AND tags.tag LIKE :tag_name
        ''', {
            'track_id': track_id,
            'tag_name': tag_name,
        })
        if cursor.fetchone() is not None:
            return True
    return False

def main(song_csv_filename, tags_sqlite_filename):
    with \
            open(song_csv_filename) as song_csv_file, \
            sqlite3.connect(tags_sqlite_filename) as tags_db_connection:
        csv_data = csv.DictReader(song_csv_file)

        genre_names = [genre.name_in_output for genre in GENRES]
        new_csv_writer = csv.DictWriter(
            sys.stdout,
            fieldnames=(csv_data.fieldnames + genre_names),
        )
        new_csv_writer.writeheader()

        for row in csv_data:
            if not is_track_in_database(row['TrackID'], tags_db_connection):
                continue
            new_row = row.copy()
            for genre in GENRES:
                if does_track_have_genre(row['TrackID'], genre, tags_db_connection):
                    new_row[genre.name_in_output] = 1
                else:
                    new_row[genre.name_in_output] = 0
            new_csv_writer.writerow(new_row)

if __name__ == '__main__':
    main(*sys.argv[1:])
