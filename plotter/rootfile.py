import os, re
import uuid as _uuid

import ROOT

class RootFile:

    def __init__(self, path):
        self.path = path
        self.name = path.replace(".root", "").split('/')[-1]
        self._file = ROOT.TFile.Open(path)

    def __del__(self):
        self._file.Close()

    def __iter__(self):
        for depth, path, name in self.browse_dir(0, ''):
            yield (depth, path, name)

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

                    tree = self._file.Get(name)
                    for b in tree.GetListOfLeaves():
                        bname = b.GetName()
                        yield (depth+1, name + ':' + bname, bname)

                else:
                    yield (depth, path, name)

                    for ddepth, dpath, dname in self.browse_dir(depth+1, name):
                        yield (ddepth, dpath, dname)

            elif obj.InheritsFrom('TH1') or obj.InheritsFrom('TGraph'):
                yield (depth, path, name)

            else:
                continue


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

            obj = None

        else:
            # histogram/graph
            obj = self._file.Get(path)



        ROOT.SetOwnership(obj, False)
        try:
            obj.SetDirectory(0)
        except:
            pass

        return obj
