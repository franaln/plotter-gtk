import os
import sys

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango

from plotter.rootfile import RootFile
from plotter.plot import Plot
from plotter.history import History
from plotter.style import *

import ROOT

NAME    = 'plotter'
VERSION = '0.1dev'

class App:

    def __init__(self, file_paths):

        self.nfiles = len(file_paths)

        # files
        self.files = []
        for path in file_paths:
            print('loading %s' % path)
            self.files.append(RootFile(path))

        # models
        self.models = self.create_models()
        self.views = self.create_views()

        # plot model: (file, item, path, opts, sel)
        self.plot_model = Gtk.ListStore(int, int, str, str, str)

        # create main window
        self.create_window()

        # plots
        self.plots = []

        self.history = History()


    def create_window(self):

        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_default_size(600, 600)
        self.window.set_position(Gtk.WindowPosition.CENTER)

        self.window.connect('key_press_event', self.on_key_press)
        self.window.connect('delete_event', self.close)

        self.winbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Header Bar
        self.headerbar = self.create_header()
        self.window.set_titlebar(self.headerbar)

        # Search bar
        self.search_bar = Gtk.SearchBar()
        self.search_entry = Gtk.SearchEntry(placeholder_text='Search...')
        # #self.entry.connect('search-changed', self.on_search)
        # self.search_entry.connect('changed', self.on_search)

        self.search_bar.connect_entry(self.search_entry)
        self.search_bar.add(self.search_entry)

        self.mainbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        self.boxes = []
        for view in self.views:

            box = self.create_box(view)
            self.boxes.append(box)

            self.mainbox.pack_start(box, True, True, 0)

        self.create_plot_box()
        self.mainbox.pack_start(self.plotbox, True, True, 0)

        self.winbox.pack_start(self.search_bar, False, False, 0)
        self.winbox.pack_start(self.mainbox, True, True, 0)

        self.window.add(self.winbox)
        self.window.show_all()


    def create_header(self):

        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.get_style_context().add_class('titlebar')

        self.title = Gtk.Label(NAME)
        self.title.props.max_width_chars = 20
        self.title.props.ellipsize = Pango.EllipsizeMode.END

        self.title.get_style_context().add_class('title')
        header.set_custom_title(self.title)

        self.menu_button = Gtk.Button(image=Gtk.Image().new_from_icon_name('view-list-symbolic', Gtk.IconSize.MENU))
        #self.menu_button.connect('clicked', self.on_menu_press)

        self.find_button = Gtk.ToggleButton(image=Gtk.Image().new_from_icon_name('edit-find-symbolic', Gtk.IconSize.MENU))
        # self.find_button.connect('toggled', self.on_find_toggle)

        header.pack_start(self.menu_button)
        header.pack_end(self.find_button)

        return header


    def create_files_box(self):
        pass

    def create_plot_box(self):

        self.plotbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Top Box
        self.top_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.plot_label = Gtk.Label('Plot')

        self.button_prev = Gtk.Button()
        self.button_prev.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))

        self.button_next = Gtk.Button()
        self.button_next.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))

        self.button_prev.connect('clicked', self.on_button_prev)
        self.button_next.connect('clicked', self.on_button_next)

        self.top_box.pack_start(self.plot_label,  True, True, 0)
        self.top_box.pack_start(self.button_prev, False, False, 0)
        self.top_box.pack_start(self.button_next, False, False, 2)

        # Middle Box
        self.plot_view = Gtk.TreeView(self.plot_model)

        tr = Gtk.CellRendererText()
        tr.props.wrap_width = 300
        col1 = Gtk.TreeViewColumn("Objects", tr, text=2)
        col1.set_min_width(200)
        #col1.set_cell_data_func(tr, self.cell_data_fn_object)

        tr2 = Gtk.CellRendererText()
        tr2.props.foreground = 'grey'
        tr2.props.style = Pango.Style.ITALIC
        tr2.props.scale = 0.8
        col2 = Gtk.TreeViewColumn("Options", tr2, text=3)


        tr3 = Gtk.CellRendererText()
        tr3.set_property('editable', True)
        tr3.connect("edited", self.on_tr_sel_edited)
        col3 = Gtk.TreeViewColumn("Selection", tr3, text=4)
        col3.set_visible(False)

        selection = self.plot_view.get_selection()
        selection.set_mode(Gtk.SelectionMode.MULTIPLE)

        self.plot_view.append_column(col1)
        self.plot_view.append_column(col2)
        self.plot_view.append_column(col3)

        # buttons
        self.button_up = Gtk.Button()
        self.button_up.add(Gtk.Arrow(Gtk.ArrowType.UP, Gtk.ShadowType.NONE))

        self.button_down = Gtk.Button()
        self.button_down.add(Gtk.Arrow(Gtk.ArrowType.DOWN, Gtk.ShadowType.NONE))

        self.button_stack = Gtk.Button('Stack')
        self.button_rebin = Gtk.Button('Rebin')

        self.button_norm = Gtk.CheckButton('norm')
        self.button_hist = Gtk.CheckButton('hist')
        self.button_colz = Gtk.CheckButton('colz')

        self.button_logx = Gtk.CheckButton('logx')
        self.button_logy = Gtk.CheckButton('logy')

        #self.button_clear = Gtk.Button('Add Cut')
        self.button_clear = Gtk.Button('Clear')
        self.button_draw = Gtk.Button('Draw')
        self.button_draw_ratio = Gtk.Button('Draw Ratio')
        self.button_draw_and_ratio = Gtk.Button('Draw + Ratio')

        self.button_up.connect('clicked', self.on_button_up)
        self.button_down.connect('clicked', self.on_button_down)
        self.button_clear.connect('clicked', self.on_button_clear)
        self.button_draw.connect('clicked', self.on_button_draw)
        self.button_draw_ratio.connect('clicked', self.on_button_draw_ratio)
        self.button_draw_and_ratio.connect('clicked', self.on_button_draw_and_ratio)

        # Add selection column
        self.button_sel = Gtk.ToggleButton('Selection')
        self.button_sel.connect('toggled', self.on_button_sel)

        # Bottom Box
        self.bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        #self.bottom_box.pack_start(self.button_prev, False, True, 0)
        # self.bottom_box.pack_start(self.button_next, False, True, 0)
        self.bottom_box.pack_start(self.button_up, False, True, 0)
        self.bottom_box.pack_start(self.button_down, False, True, 0)
        #self.bottom_box.pack_end(self.button_norm, False, True, 2)
        #self.bottom_box.pack_end(self.button_hist, False, True, 2)
        #self.bottom_box.pack_end(self.button_colz, False, True, 2)
        self.bottom_box.pack_end(self.button_logy, False, True, 2)
        self.bottom_box.pack_end(self.button_logx, False, True, 2)
        self.bottom_box.pack_end(self.button_sel,  False, True, 2)

        # All together
        self.plotbox.pack_start(self.top_box, False, True, 8)
        self.plotbox.pack_start(self.plot_view, True, True, 0)
        self.plotbox.pack_start(self.bottom_box, False, True, 2)
        self.plotbox.pack_start(self.button_clear, False, True, 2)
        self.plotbox.pack_start(self.button_draw, False, True, 2)
        # self.plotbox.pack_start(self.button_draw_ratio, False, True, 2)
        # self.plotbox.pack_start(self.button_draw_and_ratio, False, True, 2)


    def create_models(self):

        models = []
        for i in range(self.nfiles):
            models.append(Gtk.TreeStore(int, int, int, str, str))

        # fill each model
        # item: (file, item, depth, path, name)
        for ifile, model in enumerate(models):

            for i, (depth, path, name) in enumerate(self.files[ifile]):

                path = '%i:%s' % (ifile, path)
                if depth == 0:
                    it = model.append(None, [ifile, i, depth, path, name])
                else:
                    model.append(it, [ifile, i, depth, path, name])

        return models

    def create_views(self):

        views = []
        for i, model in enumerate(self.models):

            view = Gtk.TreeView(model)

            selection = view.get_selection()
            selection.set_mode(Gtk.SelectionMode.MULTIPLE)
            selection.set_select_function(self.selected_row_callback, i)

            # Column title/tags
            cell_name = Gtk.CellRendererText()
            cell_name.props.editable = False
            cell_name.props.wrap_mode = Pango.WrapMode.WORD
            cell_name.props.wrap_width = 200

            column_note = Gtk.TreeViewColumn('(%i) %s' % (i, self.files[i].name), cell_name, text=4)
            column_note.set_min_width(150)
            column_note.set_expand(True)
            view.append_column(column_note)

            view.expand_all()

            views.append(view)

        return views


    def create_box(self, view):

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(view)

        box.pack_start(scroll, True, True, 0)
        return box

    def close(self, window=None, dummy=None):
        for plot in self.plots:
            del plot

        Gtk.main_quit()

    def run(self):
        Gtk.main()

    def clear_plot(self):
        self.plot_model.clear()
        self.update_plot_label()

    def on_search(self, entry):
        txt = entry.get_text().lower()
        print(txt)

    def on_key_press(self, window, event):

        key = Gdk.keyval_name(event.keyval)

        if event.state and Gdk.ModifierType.CONTROL_MASK:

            ## ctrl-q: exit
            if  key == 'q':
                self.close()

            ## ctrl-f: find
            elif key == 'f':
                if self.search_bar.get_search_mode():
                    self.search_bar.set_search_mode(False)
                else:
                    self.search_bar.set_search_mode(True)

            ## ctrl-d: draw
            elif key == 'd':
                self.draw()

            ## ctrl-c: clear selection
            elif key == 'c':
                self.clear_plot()

            ## ctrl-s: save plots
            elif key == 's':
                for plot in self.plots:
                    plot.save()

            ## ctrl-x: be sure to do nothing!
            elif key == 'x':
                pass

            return False

        # move
        if key == 'Left':
            pass
        elif key == 'Right':
            pass
        elif key == 'Down':
            pass
        elif key == 'Up':
            pass
        elif key == 'Tab':
            pass


    def selected_row_callback(self, treesel, model, path, nose, ifile):

        treeiter = model.get_iter(path)

        if model.iter_next(treeiter) is not None and model.iter_has_child(treeiter):
            return False

        ifile = model.get_value(treeiter, 0)
        path  = model.get_value(treeiter, 3)
        item = len(self.plot_model)

        opts = default_colours[item]
        if item > 0:
            opts += ',same'

        sel = ''

        if (ifile, item, path, opts, sel) in self.plot_model:
            return False

        self.plot_model.append((ifile, item, path, opts, sel))

        return False


    ## Buttons cb
    def on_button_clear(self, btn):
        self.clear_plot()

    def on_button_draw(self, btn):
        self.draw()

    def on_button_draw_ratio(self, btn):
        pass

    def on_button_draw_and_ratio(self, btn):
        pass

    def on_button_up(self, btn):

        selection = self.plot_view.get_selection()
        (model, pathlist) = selection.get_selected_rows()

        if not pathlist:
            return

        path = pathlist[0]

        curr_iter = self.plot_model.get_iter(path)

        if not path.prev():
            return

        prev_iter = self.plot_model.get_iter(path)

        self.plot_model.move_before(curr_iter, prev_iter)

    def on_button_down(self, btn):

        selection = self.plot_view.get_selection()
        (model, pathlist) = selection.get_selected_rows()

        # if not pathlist:
        #     return

        path = pathlist[0]

        curr_iter = self.plot_model.get_iter(path)

        # if not path.next():
        #     return

        next_iter = self.plot_model.get_iter(path)

        self.plot_model.move_after(curr_iter, next_iter)


    def on_button_prev(self, btn):
        self.clear_plot()

        prev_plot = self.history.back()

        if prev_plot is not None:
            for obj in prev_plot:
                self.plot_model.append(obj)

        self.update_plot_label()

    def on_button_next(self, btn):
        self.clear_plot()
        for obj in self.history.forward():
            self.plot_model.append(obj)

        self.update_plot_label()


    def on_tr_sel_edited(self, widget, path, text):
        self.plot_model[path][4] = text

    def on_button_sel(self, btn):
        col = self.plot_view.get_column(2)
        col.set_visible(not col.get_visible())


    def update_plot_label(self):
        self.plot_label.set_label('Plot (%i/%i)' % (self.history.index()+1, len(self.history)+1))


    ## Draw
    def draw(self):

        if not self.plot_model or len(self.plot_model) < 1:
            return

        plot = Plot()

        # add objects
        first_hist_norm = None
        for (ifile, item, path, opts, sel) in self.plot_model:

            obj = self.files[ifile].get_object(path, sel).Clone()
            obj.SetDirectory(0)
            ROOT.SetOwnership(obj, False)

            if self.button_hist.get_active():
                opts += ',hist'
            if self.button_colz.get_active():
                opts += ',colz'

            if self.button_norm.get_active():
                if first_hist_norm is None:
                    first_hist_norm = obj.Integral()
                else:
                    obj.Scale(first_hist_norm/obj.Integral())

            plot.add(obj, opts)


        # create
        plot.create(
            logx=self.button_logx.get_active(),
            logy=self.button_logy.get_active()
        )

        self.plots.append(plot)
        plot.canvas.Update()
        self.history.add([ (ifile, item, path, opts, sel) for (ifile, item, path, opts, sel) in self.plot_model ])

        self.clear_plot()
