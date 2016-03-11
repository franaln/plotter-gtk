import os
import sys

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango

#from plotter.db import Database
from plotter.rootfile import RootFile
from plotter.plot import Plot
# import plotter.style

import ROOT

NAME    = 'plotter'
VERSION = '0.1dev'


class App:

    def __init__(self, file_paths):

        self.nfiles = len(file_paths)

        # self.settings = Settings(conf_path)

        # if self.settings.get_value('db_path'):
        #     self.db_path = self.settings.get_value('db_path')
        # else:
        #     self.db_path = default_db_path
        #     self.settings.set_value('db_path', self.db_path)

        # load files
        self.files = []
        for path in file_paths:
            self.files.append(RootFile(path))
        #self.db = Database(file_paths)

        # models
        self.models = self.create_models()
        self.views = self.create_views()

        # create main window
        self.create_window()

        self.plots = []


    def create_window(self):

        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_default_size(500, 600)
        self.window.set_position(Gtk.WindowPosition.CENTER)

        self.window.connect('key_press_event', self.on_key_press)
        self.window.connect('delete_event', self.close)

        self.headerbar = self.create_header()
        self.window.set_titlebar(self.headerbar)

        self.mainbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        self.boxes = []
        for view in self.views:

            box = self.create_box(view)
            self.boxes.append(box)

            self.mainbox.pack_start(box, True, True, 0)

        # plot box
        self.plot_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.plot_label = Gtk.Label('Plot')
        self.plot_box.pack_start(self.plot_label, False, True, 10)


        self.plot_model = Gtk.ListStore(int,int, str)
        tv = Gtk.TreeView(self.plot_model)

        tr = Gtk.CellRendererText()
        tr.props.wrap_width = 300

        col1 = Gtk.TreeViewColumn("Objects", tr, text=2)
        col1.set_min_width(150)
        # col1.set_cell_data_func(tr, self.cell_data_fn_plot_name)

        tr2 = Gtk.CellRendererText()
        tr2.props.foreground = 'grey'
        tr2.props.style =Pango.Style.ITALIC
        tr2.props.scale = 0.8
        col2 = Gtk.TreeViewColumn("Options", tr2)
        col2.set_cell_data_func(tr2, self.cell_data_fn_plot_opts)

        selection = tv.get_selection()
        selection.set_mode(Gtk.SelectionMode.MULTIPLE)

        tv.append_column(col1)
        tv.append_column(col2)

        # buttons
        self.button_up = Gtk.Button()
        self.button_up.add(Gtk.Arrow(Gtk.ArrowType.UP, Gtk.ShadowType.NONE))
        self.button_up.connect('clicked', self.on_button_up)

        self.button_down = Gtk.Button()
        self.button_down.add(Gtk.Arrow(Gtk.ArrowType.DOWN, Gtk.ShadowType.NONE))
        self.button_down.connect('clicked', self.on_button_down)

        button_stack = Gtk.Button('Stack')
        button_logy = Gtk.Button('log y')


        self.button_clear = Gtk.Button('Clear')
        self.button_clear.connect('clicked', self.on_button_clear)

        self.button_draw = Gtk.Button('Draw')
        self.button_draw.connect('clicked', self.on_button_draw)

        self.button_draw_ratio = Gtk.Button('Draw Ratio')
        self.button_draw_ratio.connect('clicked', self.on_button_draw_ratio)

        self.button_draw_and_ratio = Gtk.Button('Draw + Ratio')
        self.button_draw_and_ratio.connect('clicked', self.on_button_draw_and_ratio)


        self.plot_box.pack_start(tv, True, True, 0)

        plot_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        plot_buttons.pack_start(self.button_up, False, True, 0)
        plot_buttons.pack_start(self.button_down, False, True, 0)
        plot_buttons.pack_start(button_stack, False, True, 5)
        plot_buttons.pack_start(button_logy, False, True, 5)

        self.plot_box.pack_start(plot_buttons, False, True, 5)
        self.plot_box.pack_start(self.button_clear, False, True, 2)
        self.plot_box.pack_start(self.button_draw_ratio, False, True, 2)
        self.plot_box.pack_start(self.button_draw_and_ratio, False, True, 2)
        self.plot_box.pack_start(self.button_draw, False, True, 2)

        self.mainbox.pack_start(self.plot_box, True, True, 0)

        self.window.add(self.mainbox)
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

        #self.new_button = Gtk.Button(image=Gtk.Image().new_from_icon_name('list-add-symbolic', Gtk.IconSize.MENU))
        # self.new_button.connect('clicked', self.on_new_press)

        #self.del_button = Gtk.Button(image=Gtk.Image().new_from_icon_name('list-remove-symbolic', Gtk.IconSize.MENU))
        # self.del_button.connect('clicked', self.on_del_press)

        # self.back_button = Gtk.Button(image=Gtk.Image().new_from_icon_name('go-previous-symbolic', Gtk.IconSize.MENU))
        # self.back_button.connect('clicked', self.on_back_press)

        #self.find_button = Gtk.ToggleButton(image=Gtk.Image().new_from_icon_name('edit-find-symbolic', Gtk.IconSize.MENU))
        # self.find_button.connect('toggled', self.on_find_toggle)

        # header.pack_start(self.new_button)
        # header.pack_start(self.del_button)
        # # header.pack_start(self.back_button)
        # header.pack_end(self.find_button)

        return header


    def create_models(self):

        # model
        models = []
        for i in xrange(self.nfiles):
            models.append(Gtk.TreeStore(int, int, str))


        for ifile, model in enumerate(models):

            for iitem, (depth, iname) in enumerate(self.files[ifile]):

                if depth == 0:
                    it = model.append(None, [ifile, iitem, iname])
                else:
                    model.append(it, [ifile, iitem, iname])



        # self.show_idx = self.idx
        # self.model_filter.set_visible_func(self.visible_fn, self.show_idx)
        # self.model_filter.refilter()

        return models


    def create_views(self):

        views = []
        for i, model in enumerate(self.models):

            view = Gtk.TreeView(model) #_filter)

            # self.modelview.set_activate_on_single_click(True)
            # self.modelview.set_headers_visible(False)
            # self.modelview.set_enable_search(False)
            # view.set_rubber_banding(True)

            selection = view.get_selection()
            selection.set_mode(Gtk.SelectionMode.MULTIPLE)
            # selection.selected_foreach_iter(selected_row_callback)
            selection.set_select_function(self.selected_row_callback, i)


            # Column title/tags
            cell_name = Gtk.CellRendererText()
            cell_name.props.editable = False
            cell_name.props.wrap_mode = Pango.WrapMode.WORD
            cell_name.props.wrap_width = 200

            column_note = Gtk.TreeViewColumn('(%i) %s' % (i, self.files[i].name[:25]), cell_name, text=2)
            column_note.set_min_width(100)
            column_note.set_expand(True)

            # column_note.set_cell_data_func(cell_title, self.cell_data_fn_title)
            # column_note.set_cell_data_func(cell_tags, self.cell_data_fn_tags)

            # column_note.pack_end(cell_tags, False)

            # mtime column
            # cell_utime = Gtk.CellRendererText()
            # cell_utime.props.for var in collection:
            #eground = 'grey'

            # column_utime = Gtk.TreeViewColumn('Updated', cell_utime)
            # column_utime.set_min_width(50)
            # column_utime.set_cell_data_func(cell_utime, self.cell_data_fn_utime)
            view.append_column(column_note)
            # self.modelview.append_column(column_utime)

            views.append(view)

        return views


    def create_box(self, view):

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # search entry
        # self.entry = Gtk.SearchEntry(placeholder_text='Search...')
        # self.entry.connect('search-changed', self.on_search)
        # self.entry.set_hexpand(True)

        # self.searchbar = Gtk.SearchBar()
        # self.searchbar.add(self.entry)
        # self.searchbar.connect_entry(self.entry)
        # self.searchbar.props.hexpand = False


        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(view)

        # box.pack_start(self.searchbar, False, False, 0)
        box.pack_start(scroll, True, True, 0)
        return box


    def cell_data_fn_plot_name(self, column, cell, model, treeiter, data=None):
        name = model.get_value(treeiter, 2)
        #title = self.db.get_note_prop(idx, 'title')
        #if self.db.get_note_prop(idx, 'content'):
        #    title += '<i><span foreground=\'grey\'> ... </span></i>'
        #if '!' in title:
        title = '<b>' + name + '</b>'
        cell.set_property('markup', title)

    def cell_data_fn_plot_opts(self, column, cell, model, treeiter, data=None):
        #name = model.get_value(treeiter, 2)
        #title = self.db.get_note_prop(idx, 'title')
        #if self.db.get_note_prop(idx, 'content'):
        #    title += '<i><span foreground=\'grey\'> ... </span></i>'
        #if '!' in title:
        #title = '<b> red </b>'



        cell.set_property('text', style.colors[len(self.plot_model)-1])


    def close(self, window=None, dummy=None):

        for plot in self.plots:
            del plot

        # close database
        # self.db.close()

        # save settings
        # self.settings.save()

        Gtk.main_quit()

    def run(self):
        Gtk.main()


    def clear_plot(self):
        self.plot_model.clear()


    def on_key_press(self, window, event):
        key = Gdk.keyval_name(event.keyval)
        modifiers = Gtk.accelerator_get_default_mod_mask()

        # if self.searchbar.get_search_mode() and key == 'Escape':
        #     self.find_button.set_active(False)

        # if self.stack.get_visible_child_name() == 'editor' and key == 'Escape':
        #     self.exit_edit_note()

        if event.state and Gdk.ModifierType.CONTROL_MASK:

            ## ctrl-q: exit
            if  key == 'q':
                self.close()

            ## ctrl-f: find
            # elif key == 'f':
            #     self.find_button.set_active(True)
            #     self.entry.grab_focus()

            ## ctrl-n: new note
            elif key == 'd':
                self.draw()

            ## ctrl-c: clear selection
            elif key == 'c':
                self.clear_plot()

            ## ctrl-x: be sure to do nothing!
            elif key == 'x':
                pass

            return False


    def selected_row_callback(self, treesel, model, path, nose, ifile):

        treeiter = model.get_iter(path)
        ifile = model.get_value(treeiter, 0)
        iitem = model.get_value(treeiter, 1)
        iname = model.get_value(treeiter, 2)

        new_name = '%i/%s' % (ifile, iname)

        self.plot_model.append((ifile, iitem, new_name))

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
        self.plot_model.move_after()

    def on_button_down(self, btn):
        pass


    ## Draw
    def get_object(self, ifile, iitem, iname):
        return self.files[ifile].get_object(iname)

    def draw(self):

        """ Draw function. Creates a plot with the selected items and options """

        if not self.plot_model:
            return

        plot = Plot()

        # p.logx(self.check_logx.GetState())
        # p.logy(self.check_logy.GetState())

        for iobj, (ifile, iitem, iname) in enumerate(self.plot_model):

            #     print ifile, iitem, iname

            obj = self.get_object(ifile, iitem, iname)

            plot.add(obj, 'red')

        #     if iobj == 0:
        #         obj.Draw()
        #     else:
        #         obj.Draw('same')


        plot.create()

        self.plots.append(plot)

        # for i, item in enumerate(self.items):
        #     if not item.is_plotable():
        #         msg_error("")
        #         continue
        #     p.add(self.get_object(item), self.colours[i])


        # draw_opts = ''
        # if self.check_text.GetState():
        #     draw_opts += "text,"
        # if self.check_hist.GetState():
        #     draw_opts += "hist,"
        # if self.check_p.GetState():
        #     draw_opts += "P,"
        # if self.check_pie.GetState():
        #     draw_opts += "PIE,"

        # if self.radio_scatter.GetState():
        #     draw_opts += "scat,"
        # elif self.radio_box.GetState():
        #     draw_opts += "box,"
        # else:
        #     draw_opts += "colz,"
