import struct
import numpy as np
import functools
import itertools
import pandas as pd

def calcentries(fmt):
    return len(fmt)

class Alturialog:
    def __init__(self, path):
        self.tracks = dict()
        self.files = dict()
        self.track_data = dict()
        self.__read(path)

    def get_tracks(self):
        return self.tracks

    def __read(self,path):
        with open(path,'rb') as f:
                while True:
                    fb = f.read(1)
                    if not fb:
                            break
                    cid = (fb[0] & 0xF0) >> 4
                    if cid == 1: # Track format chunk
                            tid = fb[0] & 0x0F
                            by = bytes()
                            while True:
                                    b = f.read(1)
                                    if b[0] == 0:
                                            break
                                    by = by + b
                            fmt = by.decode('ascii')
                            self.tracks[tid] = dict()
                            self.track_data[tid] = pd.DataFrame(columns=range(0,calcentries(fmt)))
                            self.tracks[tid]['format'] = fmt
                            self.tracks[tid]['length'] = struct.calcsize(fmt)
                    elif cid == 2: # Track series names chunk
                            tid = fb[0] & 0x0F
                            by = bytes()
                            while True:
                                    b = f.read(1)
                                    if b[0] == 0:
                                            break
                                    by = by + b
                            name = by.decode('ascii')
                            names = name.split(',')
                            self.track_data[tid].columns = names
                    elif cid == 3: # Track data chunk
                            tid = fb[0] & 0x0F
                            data = f.read(self.tracks[tid]['length'])
                            values = struct.unpack(self.tracks[tid]['format'],data)
                            self.track_data[tid].loc[len(self.track_data[tid])] = values
                    elif cid == 4: # File chunk
                            fid = fb[0] & 0x0F
                            size = f.read(4)
                            size = struct.unpack('I',size)[0]
                            data = f.read(size)
                            self.files[fid] = data
