import os, re
import uuid as _uuid

import ROOT

class RootFile:

    def __init__(self, path):
        self.path = path
        self.name = path.replace(".root", "").split('/')[-1]

        self._file = ROOT.TFile.Open(path)
        # filename = filename.replace(".root", "").split('/')[-1]

        # self.items = [ key.GetName() for key in self._file.GetListOfKeys() ]

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

    def __del__(self):
        self._file.Close()

    # def __iter__(self):
    #     return iter(self.files)


    # loop over objects
    def browse_tree(self, depth, name):
        tree = ROOT.TTree(name, '')
        self._file.GetObject(name, tree)

        lb = tree.GetListOfBranches()
        nbranches = lb.GetSize()
        for k in xrange(nbranches):
            branch = lb.At(k)
            if not branch:
                continue
            yield (depth+1, branch.GetName())

    def browse_dir(self, depth, name):

        cdir = self._file.GetDirectory(name)

        for key in cdir.GetListOfKeys():
            obj = key.ReadObj()
            name = obj.GetName()

            if not name:
                name = title

            if obj.IsFolder():
                if obj.InheritsFrom('TTree'):

                    yield (depth, name)

                    for idepth, branch in self.browse_tree(depth, name):
                        yield (idepth, branch)

                else:
                    yield (depth, name)

                    for idepth, iname in self.browse_dir(depth, name):
                        yield (idepth, iname)

            elif obj.InheritsFrom('TH1') or obj.InheritsFrom('TGraph'):
                yield (depth, name)

            else:
                yield (depth, name)


    def loop(self):

        depth = 0
        for depth, name in self.browse_dir(depth, ''):
            yield (depth, name)


    def get_object(self, iname):

        # name = self.items[iitem]

        obj = self.file.Get(iname)
        ROOT.SetOwnership(obj, False)

        try:
            obj.SetDirectory(0)
        except:
            pass

        return obj


    # def browse_dir(self, pt):

    #     last_path = self.current_path
    #     self.current_path = pt.get_name()

    #     cdir = self._file.GetDirectory(pt.get_name())

    #     for key in cdir.GetListOfKeys():
    #         obj = key.ReadObj()
    #         name = obj.GetName()
    #         title = obj.GetTitle()

    #         if not name:
    #             name = title

    #         if obj.IsFolder():
    #             if obj.InheritsFrom('TTree'):

    #                 it = ParentItem(self.entry, name, title, 'Tree')

    #                 pt.add_item(it)
    #                 self.entry += 1
    #                 self.browse_tree(it)
    #             else:
    #                 it = ParentItem(self.entry, name, title, 'Dir')
    #                 pt.add_item(it)
    #                 self.entry += 1
    #                 self.browse_dir(it)
    #         elif obj.InheritsFrom("TH1"):
    #             if obj.InheritsFrom("TH3"):
    #                 it = Item(self.entry, name, title, 'Hist3D')
    #             elif obj.InheritsFrom("TH2"):
    #                 it = Item(self.entry, name, title, 'Hist2D')
    #             else:
    #                 it = Item(self.entry, name, title, 'Hist1D')
    #             pt.add_item(it)
    #             self.entry += 1
    #         elif obj.InheritsFrom("TGraph"):
    #             it = Item(self.entry, name, title, 'Graph')
    #             pt.add_item(it)
    #             self.entry += 1

    # def browse_tree(self, pt):

    #     t = ROOT.TTree(pt.get_name(), '')
    #     self._file.GetObject(pt.get_name(), t)

    #     l = t.GetListOfBranches()
    #     nbranches = l.GetSize()
    #     for k in xrange(nbranches):
    #         branch = l.At(k)
    #         if not branch:
    #             continue
    #         it = Item(self.entry, branch.GetName(), branch.GetTitle(), 'Branch')
    #         pt.add_item(it)
    #         self.entry += 1



    # # @classmethod
    # # def from_file(cls, fname):
    # #     with open(fname) as f:
    # #         title = f.readline().replace('\n', '')
    # #         tags = tags_re.findall(f.readline())
    # #         ctime = os.path.getctime(fname)
    # #         utime = os.path.getmtime(fname)
    # #         uuid = os.path.basename(fname).replace('.txt', '')
    # #         content = f.read()
    # #         return cls(fname, title, content, ctime, utime, uuid, tags)

    # # @classmethod
    # # def new(cls, dbpath):
    # #     uuid = str(_uuid.uuid4())
    # #     fname = os.path.join(dbpath, uuid+'.txt')
    # #     open(fname, 'w')
    # #     return cls(fname, '', '', os.path.getctime(fname), os.path.getmtime(fname), uuid, [])

    # # def rename(self):
    # #     # name = hashlib.sha256(bytes(self.title, 'utf-8')).hexdigest()
    # #     # new_name = os.path.join(os.path.dirname(self.fname), name+'.txt')
    # #     os.rename(self.fname, new_name)
    # #     self.fname = new_name

    # # def save(self):
    # #     if not self.title:
    # #         return

    # #     with open(self.fname, 'w') as f:
    # #         f.write('%s\n' % self.title)
    # #         f.write('%s\n' % ' @'.join(self.tags))
    # #         f.write(self.content)

    # #     # after save update utime
    # #     self.utime = os.path.getmtime(self.fname)


    #     # def __contains__(self, tag):
    #     #     if tag in self.tags:
    #     #         return True
    #     #     else:
    #     #         return False
