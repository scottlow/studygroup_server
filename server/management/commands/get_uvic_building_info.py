""" Script to scrape and insert UVic's building information into the database.

Example:
    To generate a csv file for UVic building information:
        $ python2.7 manage.py get_uvic_building_info
    To insert to the database using a csv file:
        $ python2.7 manage.py get_uvic_building_info [name of csv file]
"""

from collections import namedtuple
import csv
from difflib import SequenceMatcher
from django.core.management.base import BaseCommand, CommandError
import json
import os
import re
import requests
from server.models import Location, University
from studygroup_server import settings
import time


# UVic building information from Domino's
DOMINO_URL = "http://express.dominos.ca/site-locator/site/120/buildings"
# API information: https://developers.google.com/maps/documentation/geocoding/
GOOGLE_API_URL = "http://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=false"
# Use university and city info when querying Geocode API for better accuracy.
UNIV_NAME = " University of Victoria"
CITY = " Victoria, BC"


class Command(BaseCommand):
    @staticmethod
    def get_building_names():
        """Gets UVic building names from Domino's website (DOMINO_URL)."""

        building_names = []

        response = requests.get(DOMINO_URL)
        if response.status_code != 200:
            raise CommandError("Could not get info about UVic buildings: {}".
            format(response.status_code))

        json_response = response.json()
        if 'Buildings' not in json_response:
            raise CommandError("No building info could be found in the URL "
                               "here: {}".format(DOMINO_URL))

        for building in json_response['Buildings']:
            building_name = building.get('BuildingName')
            if building_name:
                building_name = str(building_name.encode("ascii", "ignore"))

                # Get rid of three-letter code in the beginning of string
                match = re.match("\w{3}- (.*)", building_name)
                if match:
                    building_name = match.group(1)
                building_names.append(building_name)
        return building_names

    @staticmethod
    def write_to_csv(rows):
        """Writes building names, latitudes, and longitudes to a CSV file.

        Args:
            rows: List of namedtuples. ("Building", ["name", "lat", "lng"])
        """

        if rows:
            with open("uvic_building_info.csv", "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                rows.insert(0, ["Name", "Latitude", "Longitude"])
                csv_writer.writerows(rows)

    def write_to_database(self, file_name):
        """Write a given CSV file's rows to the database.

        Args:
            file_name: Name of the CSV file.
        """

        self.stdout.write("Writing to database.")
        count = 0
        uvic = University.objects.get(name="University of Victoria")
        data = []

        # Find the file given the CSV file name.
        for dirpath, dirnames, files in os.walk(settings.BASE_DIR):
            for file in files:
                if file == file_name:
                    with open(os.path.join(dirpath, file), "r") as csv_file:
                        data = csv_file.readlines()

        if not data:
            raise CommandError("Could not find {} in any of the directories "
                               "under {}".format(file_name, settings.BASE_DIR))

        # TODO: Handle duplicate data in the database.
        for line in data[1:]:
            line = line.strip().split(',')
            name, lat, lng = tuple(line)

            location = Location(name=name, latitude=float(lat),
                                longitude=float(lng), university=uvic, frequency=0)
            location.save()
            count += 1
        self.stdout.write("Wrote %d entries to the database." % count)

    def handle(self, *args, **options):
        """Validates given CSV file name, and writes to the database using it.
        """

        self.stdout.write("Starting get_uvic_building_info script.")

        if args:
            file_name = args[0]
            if file_name.endswith(".csv"):
                self.write_to_database(args[0])
            else:
                raise CommandError("Given file name is not a CSV file.")
        else:
            self.handle_noargs()

        self.stdout.write("Script successfully finished.")

    def handle_noargs(self, **options):
        """ Obtains and inserts UVic building info into the server database.

        Queries Domino's website for a JSON list of UVic building names. Uses
        Google Geocode API to get the latitude and longitude of each building,
        then inserts the data into Session table in the server database.
        """

        Building = namedtuple('Building', ['name', 'lat', 'lng'])
        building_info = []

        building_names = self.get_building_names()
        if not building_names:
            raise CommandError("No building names could be found!")

        for name in self.get_building_names():
            resp = requests.get(GOOGLE_API_URL.format(name + UNIV_NAME + CITY))
            if resp.status_code != 200:
                continue

            geocode_info = json.loads(resp.text)
            if geocode_info.get('status') != 'OK':
                continue

            formatted_addr = geocode_info['results'][0]['formatted_address'] \
                                .encode("utf-8")

            lat, lng = None, None
            for match in geocode_info['results']:
                # Fuzzy string matching
                full_name = name + UNIV_NAME + CITY
                if SequenceMatcher(None, match['formatted_address'],
                                   full_name).quick_ratio() > 0.7:
                    location = match['geometry']['location']
                    lat, lng = location['lat'], location['lng']
                    break

            # Lat & long of UVic. If the script gets used for different
            # universities, use Google API. For now, this works.
            if not lat and not lng:
                lat, lng = 48.46491220000001, -123.3113384

            building_info.append(Building(name=name, lat=lat, lng=lng))

            # Querying the Google API too rapidly returns OVER_QUERY_LIMIT.
            time.sleep(0.1)

        self.write_to_csv(building_info)
