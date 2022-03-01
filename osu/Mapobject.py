from .osuparser import *


class Mapobject():
    def __init__(self, filename=None):
        if type(filename) == str:
            self.parse_osu_file(filename)

    def parse_osu_file(self, filename):
        # Reads the osu file given and splits it up
        with open(filename, encoding="utf-8") as f:
            data = f.read()
            data = data.replace("\n\n\n", "\n\n")
            sections = data[:-1].split("\n\n")

        self.mapdata = defaultdict()

        # Reads the different sections of a map to a dictionary
        for sect in sections:
            sect_lst = sect.split("\n")
            key = ((sect_lst[0].replace("[", "")).replace("]", "")).lower()

            if key in ["general", "editor", "metadata", "difficulty", "colours"]:
                self.mapdata[key] = defaultdict()
                for s in sect_lst[1:]:
                    # Splits the list and lowercase the keys
                    split = s.split(":")
                    s_key = (split[0].strip()).lower()
                    # Some of the variables are stored differently these if are for those
                    if s_key == "bookmarks":
                        self.mapdata[key][s_key] = [int(x) for x in (
                            split[1].strip()).split(",")]
                    elif key == "colours":
                        self.mapdata[key][s_key] = [int(x) for x in (
                            split[1].strip()).split(",")]
                    else:
                        try:
                            self.mapdata[key][s_key] = int(split[1].strip())
                        except:
                            try:
                                self.mapdata[key][s_key] = float(
                                    split[1].strip())
                            except:
                                self.mapdata[key][s_key] = split[1].strip()

            if key in ["timingpoints", "hitobjects"]:
                self.mapdata[key] = [s for s in sect_lst[1:]]

            if key == "events":
                self.mapdata[key] = sect
