import os
import glob

from plotter.rootfile import RootFile

import ROOT

class Database:

    def __init__(self, file_paths):

        self.files = []
        for path in file_paths:
            self.files.append(RootFile(path))


    def __len__(self):
        return len(self.files)

    def __iter__(self):
        return iter(self.files)

    def __del__(self):
        self.close()

    def get_object(self, ifile, iitem, iname):
        return self.files[ifile].get_object(iname)


    # def load(self):

    #     for key in self.keys:
    #         self.add_note(key.GetName())
    #     # db_list = glob.glob(self.path + '/*.txt')
    #     # for fn in db_list:
    #     #     note = Note.from_file(fn)
    #     #     self.add_note(note)

    # def save(self):
    #     for note in self.notes.values():
    #         note.save()

    def close(self):
        pass
