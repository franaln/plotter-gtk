import os, re
import uuid as _uuid

import ROOT

class RootFile:

    def __init__(self, path):
        self.path = path
        self.name = path.replace(".root", "").split('/')[-1]

        self._file = ROOT.TFile.Open(path)

        # browse file
        #for depth, name in self:

        # filename = filename.replace(".root", "").split('/')[-1]

        self.items = [ key.GetName() for key in self._file.GetListOfKeys() ] # tmp

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


    # loop over objects
    def __iter__(self):
        depth = 0
        for depth, name in self.browse_dir(depth, ''):
            yield (depth, name)

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



    def get_object(self, iname):

        # name = self.items[iitem]

        # histogram/graph
        if iname in self.items:
            obj = self._file.Get(iname)
            print obj

        # branch
        else:

            hname = "h_" + iname

            tree = ROOT.TTree('mini', '')
            self._file.GetObject('mini', tree)


            #tree.Draw(iname+'>>'+hname, '', 'goff')

            htmp = ROOT.TH1F(hname, hname, 100, 0, 100)

            tree.Project(hname, iname, '')
            # hist = htemp.Clone()

            # print iname, ROOT.gDirectory

            obj = htmp.Clone()
            print 'asd'

        ROOT.SetOwnership(obj, False)
        try:
            obj.SetDirectory(0)
        except:
            pass

        return obj
