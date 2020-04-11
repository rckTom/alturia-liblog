import struct
import numpy as np
import functools
import itertools
import pandas as pd

def calcentries(fmt):
    return len(fmt)

class Track:
    def __init__(self):
        self.data = list()
        self.column_names = list()
        self.name = ""
        self.format = ""

    def get_track_entry_length(self):
        return struct.calcsize(self.format)

    def to_dataframe(self):
        return pd.DataFrame(self.data, columns = self.column_names)

    def append(self, data):
        self.data.append(data)

class Alturialog:
    def __init__(self, path):
        self.tracks = dict()
        self.files = dict()
        self.__read(path)

    def get_tracks(self):
        return self.tracks

    def get_track(self, id):
        if id not in self.tracks:
            self.tracks[id] = Track()
        return self.tracks[id]

    def get_track_id(self, fb):
        return fb[0] & 0x0F

    def read_c_string(self, f):
        by = bytes()
        while True:
            b = f.read(1)
            if b[0] == 0:
                break
            by = by + b
        return by.decode('ascii')

    def parse_track_format(self, fb, f):
        tid = self.get_track_id(fb)
        track = self.get_track(tid)
        fmt = self.read_c_string(f)
        track.format = fmt

    def parse_track_series_names(self, fb, f):
        tid = self.get_track_id(fb)
        track = self.get_track(tid)
        namestr = self.read_c_string(f)
        names = namestr.split(',')

        track.column_names = names

    def parse_track_data(self, fb, f):
        tid = self.get_track_id(fb)
        track = self.get_track(tid)
        data = f.read(struct.calcsize(track.format))
        data = struct.unpack(track.format, data)
        track.append(data)

    def parse_track_name(self, fb, f):
        tid = self.get_track_id(fb)
        track = self.get_track(tid)
        name = self.read_c_string(f)
        track.name = name

    def parse_file_chunk(self, fb, f):
        fid = fb[0] & 0xF0
        size = f.read(4)
        size = struct.unpack('I',size)[0]
        self.files[fid] = f.read(size)

    def __read(self,path):
        with open(path,'rb') as f:
            while True:
                fb = f.read(1)
                if not fb:
                    break
                cid = (fb[0] & 0xF0) >> 4
                if cid == 1: # Track format chunk
                    self.parse_track_format(fb, f)
                elif cid == 2: # Track series names chunk
                    self.parse_track_series_names(fb, f)
                elif cid == 3: # Track data chunk
                    self.parse_track_data(fb, f)
                elif cid == 4: # File chunk
                    self.parse_file_chunk(fb, f)
                elif cid == 5: # Track name chunk
                    self.parse_track_name(fb, f)

