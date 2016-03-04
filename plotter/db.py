import os
import glob

from plotter.rootfile import RootFile

import ROOT

class Database:

    def __init__(self, file_paths):
        # self.path = db_path
        self.files = []
        for path in file_paths:
            self.files.append(RootFile(path))


        #self.keys
        # if not os.path.isdir(self.path):
        #     self.create_dir(self.path)

    def __getitem__(self, nfile):
        try:
            return self.notes[key]
        except IndexError:
            raise

    def __len__(self):
        return len(self.notes)

    def __iter__(self):
        return iter(self.notes)

    def __del__(self):
        pass #self.close()


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

    # def close(self):
    #     pass

    # def create_dir(self, path):
    #     try:
    #         os.makedirs(path)
    #     except OSError:
    #         pass

    # ## TODO
    # def backup(self):
    #     # copy db to a backup file
    #     pass

    # ## TODO
    # def move(self, new_path):
    #     self.create_dir(new_path)
    #     for note in self.notes.values():
    #         os.rename(note.fname)

    # def add_note(self, note):
    #     self.notes[len(self.notes)] = note

    # def update_note_prop(self, idx, prop, newvalue):
    #     current = getattr(self.notes[idx], prop)
    #     if newvalue != current:
    #         setattr(self.notes[idx], prop, newvalue)
    #         self.notes[idx].save()

    # def get_note_name(self, idx):
    #     return self.notes[idx]

    # def get_note_prop(self, idx, prop):
    #     return getattr(self.notes[idx], prop)

    # def add_tags(self, idx, *tags):
    #     for tag in tags:
    #         if not tag in self.notes[idx].tags:
    #             self.notes[idx].tags.add(tag)
    #             self.notes[idx].save()

    # def remove_tags(self, idx, *tags):
    #     for tag in tags:
    #         try:
    #             self.notes[idx].tags.remove(tag)
    #         except (ValueError, KeyError):
    #             pass
    #         else:
    #             self.notes[idx].save()

    # def new_note(self):
    #     idx = len(self.notes)
    #     note = Note.new(self.path)
    #     self.add_note(note)
    #     return idx

    # def search_matches(self, text):
    #     matches_idx = []
    #     for idx, note in self.notes.items():
    #         if '@trash' in note.tags and not '@trash' in text:
    #             continue
    #         elif text in note.title.lower():
    #             matches_idx.append(idx)
    #         elif '@' in text and text in ''.join(note.tags):
    #             matches_idx.append(idx)
    #     return matches_idx

    # def lock(self):
    #     pass

    # def unlock(self):
    #     pass
