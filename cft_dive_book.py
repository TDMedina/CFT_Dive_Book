# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 22:05:42 2021

@author: Tyler
"""

from collections import namedtuple
from datetime import datetime


DIVE_CODES = {
    "Bh": "Boat Handling",
    "C": "Cave",
    "Dr": "Drift",
    "Md": "Mandatory Decompression",
    "N": "Night",
    "Nx": "Nitrox",
    "P": "Photography",
    "S": "Scenic",
    "Sk": "Snorkel",
    "T": "Test",
    "Tr": "Training",
    "Tx": "Technical Diving",
    "W": "Wreck",
    }

CFT_LEVELS = {}

CONDITIONS_TEMPLATE = {
    "Surface": None,
    "Surf": None,
    "Tide": None,
    "Current": None}

class AnnualLog:
    def __init__(self, year, dives=None):
        self.year = year

        self.dives = dives
        if self.dives is None:
            self.dives = []

        self.number_of_dives = len(self.dives)

    def __repr__(self):
        string = (f"Annual Log: {self.year}\n"
                  f"Total dives: {self.number_of_dives}")
        return string

    def add_dive(self, dive):
        self.dives.append(dive)
        self.number_of_dives += 1


class DiveRecord:
    def __init__(self, divers, date, location, max_depth, duration,
                 code, coordinates=None, conditions=None,
                 qualifying_dive=False, instructors=None):
        self.divers = divers
        self.instructors = instructors

        self.date = date
        self.location = location
        self.coordinates = coordinates

        self.max_depth = max_depth
        self.duration = duration

        self.code = code

        self.qualifying_dive = qualifying_dive

        self.dive_plan = None
        self.conditions = conditions

    def __repr__(self):
        string = "Dive Record\n"
        fields = ["Date:"]
        attrs = [self.date.strftime('%Y-%B-%d')]

        for i, diver in enumerate(self.divers, start=1):
            fields.append(f"Diver {i}:")
            attrs.append(f"{diver.name} ({diver.cft_level})")

        if self.instructors is not None:
            for i, instructor in enumerate(self.instructors, start=1):
                fields.append(f"Instructor {i}:")
                attrs.append(f"{instructor.name} ({instructor.cft_level})")


        fields += ["Location:", "Depth:", "Duration:", "Dive Type:"]
        attrs += [self.location, f"{self.max_depth}m", f"{self.duration}min",
                  DIVE_CODES[self.code]]

        field_pad = 1 + max([len(field) for field in fields
                             if isinstance(field, (str, int))])
        attr_pad = max([len(attr) for attr in attrs
                        if isinstance(attr, (str, int))])
        fields = [f"{field:<{field_pad}}" for field in fields]
        attrs = [f"{attr:>{attr_pad}}" for attr in attrs]
        pieces = [x+y for x, y in zip(fields, attrs)]
        string += "\n".join(pieces)
        return string


class PersonalDiveLog:
    def __init__(self, diver, dive):
        self.diver = diver
        self.dive = dive

        self.equipment = None


PersonalDive = namedtuple("PersonalDive", ["Dive_No", "Dive", "Log"])


class Diver:
    def __init__(self, name, cft_no, club, level,
                 dives=None, annual_logs=None, active=True):
        self.name = name
        self.cft_no = cft_no
        self.club = club

        self.dives = dives
        if self.dives is None:
            self.dives = []
        self.total_dives = len(self.dives)

        self.annual_logs = annual_logs
        if self.annual_logs is None:
            self.annual_logs = {}

        self.cft_level = level

        self.active = active

    def __repr__(self):
        string = (f"Diver:\t{self.name}\n"
                  f"CFT Number:\t{self.cft_no}\n"
                  f"Club:\t{self.club}\n"
                  f"Level:\t{self.cft_level}\n"
                  f"Dives:\t{self.total_dives}\n"
                  f"Active:\t{self.active}\n")
        return string

    def add_dive(self, dive, personal_log=None):
        dive_no = self.total_dives + 1
        self.dives.append(PersonalDive(dive_no, dive, personal_log))
        year = dive.date.year
        if year not in self.annual_logs:
            self.annual_logs[year] = AnnualLog(year)
        self.annual_logs[year].add_dive(dive)
        self.total_dives += 1


