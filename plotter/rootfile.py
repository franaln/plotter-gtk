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

    def __iter__(self):
        depth = 0
        for depth, path, name in self.browse_dir(depth, ''):
            yield (depth, path, name)

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

    def browse_dir(self, depth, parent_name):

        cdir = self._file.GetDirectory(parent_name)

        for key in cdir.GetListOfKeys():
            obj = key.ReadObj()
            name = obj.GetName()

            if parent_name:
                path = parent_name + '/' + name
            else:
                path = name

            if obj.IsFolder():
                if obj.InheritsFrom('TTree'):

                    yield (depth, path, name)

                    for idepth, branch in self.browse_tree(depth, name):
                        path = name + ':' + branch
                        yield (idepth, path, branch)

                else:
                    yield (depth, path, name)

                    for ddepth, dpath, dname in self.browse_dir(depth, name):
                        yield (ddepth, dpath, dname)

            elif obj.InheritsFrom('TH1') or obj.InheritsFrom('TGraph'):
                yield (depth, path, name)

            else:
                yield (depth, path, name)



    def get_object(self, path):

        # tree
        if ':' in path:

            treename, name = path.split(':')

            hname = "h_" + name

            tree = ROOT.TTree(treename, '')
            self._file.GetObject(treename, tree)

            tree.Draw(name+'>>'+hname, '', 'goff')

            #htmp = ROOT.TH1F(hname, hname, 100, 0, 100)
            #tree.Project(hname, name, '')

            htmp = ROOT.gDirectory.Get(hname)

            obj = htmp.Clone()




        elif '/' in path:
            dirname, name = path.split('/')



        else:
            # histogram/graph
            obj = self._file.Get(path)



        ROOT.SetOwnership(obj, False)
        try:
            obj.SetDirectory(0)
        except:
            pass

        return obj
