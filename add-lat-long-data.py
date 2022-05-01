#!/usr/bin/env python3

"""
Fill in latitude/longitude data based on place names.

Joe Walbran and Natasha Zebrev

Usage: ./add-lat-long-data.py input_csv_file >output_csv_file
"""

import csv
import json
import sys
import urllib.parse
import urllib.request

def get_location(location_name):
    api_username = 'walbr037'
    api_location_name = urllib.parse.quote(location_name)
    api_url = f'http://api.geonames.org/searchJSON?q={api_location_name}&maxRows=1&username={api_username}'
    with urllib.request.urlopen(api_url) as url:
        response = url.read()
        try:
            location_data = json.loads(response)["geonames"][0]
        except KeyError as e:
            # API error
            print(response, file=sys.stderr)
            raise e
        except IndexError:
            # Location not found
            return "", ""
        else:
            return location_data["lat"], location_data["lng"]


def main(song_csv_filename):
    with open(song_csv_filename) as song_csv_file:

        csv_data = csv.DictReader(song_csv_file)

        new_csv_writer = csv.DictWriter(
            sys.stdout,
            fieldnames=csv_data.fieldnames,
        )
        new_csv_writer.writeheader()

        for row in csv_data:
            new_row = row.copy()
            lat_data_missing = not row['ArtistLatitude']
            lon_data_missing = not row['ArtistLongitude']
            if row['ArtistLocation'] and (lat_data_missing or lon_data_missing):
                lat, lon = get_location(row['ArtistLocation'])
                if lat_data_missing:
                    new_row['ArtistLatitude'] = lat
                if lon_data_missing:
                    new_row['ArtistLongitude'] = lon
            new_csv_writer.writerow(new_row)

if __name__ == '__main__':
    main(*sys.argv[1:])
