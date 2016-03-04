import os, re
import uuid as _uuid

import ROOT

class RootFile:

    def __init__(self, path):
        self.path = path
        self.name = path.replace(".root", "").split('/')[-1]

        self.file = ROOT.TFile.Open(path)
        # filename = filename.replace(".root", "").split('/')[-1]

        self.items = [ key.GetName() for key in self.file.GetListOfKeys() ]

        # self.current_path = ''
        # self.entry = 0
        # self.parent = ParentItem(0, '', '', 'Dir')
        # self.browse_dir(self.parent)

        # self.title = title
        # self.content = content
        # self.ctime = ctime
        # self.utime = utime
        # self.uuid = uuid
        # self.tags = set(tags)

    def get_object(self, iname):

        # name = self.items[iitem]

        obj = self.file.Get(iname)
        ROOT.SetOwnership(obj, False)

        try:
            obj.SetDirectory(0)
        except:
            pass

        return obj


    # @classmethod
    # def from_file(cls, fname):
    #     with open(fname) as f:
    #         title = f.readline().replace('\n', '')
    #         tags = tags_re.findall(f.readline())
    #         ctime = os.path.getctime(fname)
    #         utime = os.path.getmtime(fname)
    #         uuid = os.path.basename(fname).replace('.txt', '')
    #         content = f.read()
    #         return cls(fname, title, content, ctime, utime, uuid, tags)

    # @classmethod
    # def new(cls, dbpath):
    #     uuid = str(_uuid.uuid4())
    #     fname = os.path.join(dbpath, uuid+'.txt')
    #     open(fname, 'w')
    #     return cls(fname, '', '', os.path.getctime(fname), os.path.getmtime(fname), uuid, [])

    # def rename(self):
    #     # name = hashlib.sha256(bytes(self.title, 'utf-8')).hexdigest()
    #     # new_name = os.path.join(os.path.dirname(self.fname), name+'.txt')
    #     os.rename(self.fname, new_name)
    #     self.fname = new_name

    # def save(self):
    #     if not self.title:
    #         return

    #     with open(self.fname, 'w') as f:
    #         f.write('%s\n' % self.title)
    #         f.write('%s\n' % ' @'.join(self.tags))
    #         f.write(self.content)

    #     # after save update utime
    #     self.utime = os.path.getmtime(self.fname)


        # def __contains__(self, tag):
        #     if tag in self.tags:
        #         return True
        #     else:
        #         return False
