import os
import sys
# import re
# import time
# from datetime import datetime

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk
# from gi.repository import GdkPixbuf
from gi.repository import Pango

from plotter.db import Database

import ROOT

NAME    = 'plotter'
VERSION = '0.1dev'


class App:

    def __init__(self, filenames):

        self.file_names = filenames

        self.nfiles = len(self.file_names)
        self.selected_items = []

        # self.settings = Settings(conf_path)

        # if self.settings.get_value('db_path'):
        #     self.db_path = self.settings.get_value('db_path')
        # else:
        #     self.db_path = default_db_path
        #     self.settings.set_value('db_path', self.db_path)

        # load db
        self.db = Database(filenames)
        # self.db.load()
        # self.current_idx = None


        # models
        self.models = self.create_models()
        self.views = self.create_views()


        # create main window
        # self.boxes = self.create_boxes()
        self.create_window()

        self.plots = []
        self.items = []


    def create_window(self):

        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_default_size(500, 600)
        self.window.set_position(Gtk.WindowPosition.CENTER)

        self.window.connect('key_press_event', self.on_key_press)
        self.window.connect('delete_event', self.close)

        self.headerbar = self.create_header()
        self.window.set_titlebar(self.headerbar)

        # self.stack = Gtk.Stack(
        #     transition_type=Gtk.StackTransitionType.SLIDE_LEFT,
        #     transition_duration=100,
        #     visible=True
        # )

        self.mainbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        self.boxes = []
        for view in self.views:

            box = self.create_box(view)
            self.boxes.append(box)

            self.mainbox.pack_start(box, True, True, 0)


        # plot box
        self.plot_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.plot_model = Gtk.ListStore(int,int, str)
        # ls.append(["Testrow 1"])
        # ls.append(["Testrow 2"])
        # ls.append(["Testrow 3"])
        tv = Gtk.TreeView(self.plot_model)
        tr = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn("Plot", tr, text=2)
        tv.append_column(col)


        self.button_up = Gtk.Button(image=Gtk.Image().new_from_icon_name('go-up', Gtk.IconSize.MENU))
        self.button_up.connect('clicked', self.on_clear)

        self.button_down = Gtk.Button(image=Gtk.Image().new_from_icon_name('go-down', Gtk.IconSize.MENU))
        self.button_down.connect('clicked', self.on_clear)

        self.button_clear = Gtk.Button('Clear')
        self.button_clear.connect('clicked', self.on_clear)

        self.button_draw = Gtk.Button('Draw')
        self.button_draw.connect('clicked', self.on_draw)

        self.button_draw_ratio = Gtk.Button('Draw Ratio')
        self.button_draw_ratio.connect('clicked', self.on_draw_ratio)

        self.button_draw_and_ratio = Gtk.Button('Draw + Ratio')
        self.button_draw_and_ratio.connect('clicked', self.on_draw_and_ratio)

        # self.meditor = self.create_editor_view()

        # self.stack.add_named(self.mlist,     'list')
        # self.stack.add_named(self.meditor, 'editor')

        self.plot_box.pack_start(tv, True, True, 0)

        plot_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        plot_buttons.pack_start(self.button_up, False, True, 0)
        plot_buttons.pack_start(self.button_down, False, True, 0)

        self.plot_box.pack_start(plot_buttons, False, True, 0)
        self.plot_box.pack_start(self.button_clear, False, True, 0)
        self.plot_box.pack_start(self.button_draw, False, True, 0)
        self.plot_box.pack_start(self.button_draw_ratio, False, True, 0)
        self.plot_box.pack_start(self.button_draw_and_ratio, False, True, 0)

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
            models.append(Gtk.ListStore(int, int, str))

        # self.model.set_sort_func(5, self.compare_fn, None)
        # self.model.set_sort_column_id(5, Gtk.SortType.DESCENDING)

        # filter
        # self.model_filter = self.model.filter_new()
        # self.idx = []
        # self.populate_model()

        for ifile, model in enumerate(models):
            for iitem, iname in enumerate(self.db.files[ifile].items):
                model.append([ifile, iitem, iname])

        # self.show_idx = self.idx

        #self.model_filter.set_visible_func(self.visible_fn, self.show_idx)
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
            cell_name.props.wrap_width = 300
            # cell_title.connect('edited', self.on_cell_edit)
            # cell_title.connect('editing-started', self.on_cell_editing_started)

            # cell_tags = Gtk.CellRendererText()
            # cell_tags.props.foreground = 'grey'
            # cell_tags.props.style = Pango.Style.ITALIC
            # cell_tags.props.scale = 0.8

            # column_note = Gtk.TreeViewColumn('File %i' % i, cell_title)
            column_note = Gtk.TreeViewColumn(self.file_names[i], cell_name, text=2)
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


    def close(self, window=None, dummy=None):
        # if editing note: update note
        # if self.current_idx:
        #     self.exit_edit_note()

        # # close database
        # self.db.close()

        # save settings
        # self.settings.save()

        Gtk.main_quit()

    def run(self):
        Gtk.main()

    def get_idx(self, path):
        return self.model_filter[path][0]

    # def show_view(self, name):
    #     # self.stack.set_visible_child_name(name)
    #     # if name == 'list':
    #     #     self.back_button.hide()
    #     #     self.new_button.show()
    #     #     self.del_button.show()
    #     #     self.find_button.show()
    #     #     self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
    #     #     self.title.set_label(NAME)
    #     # elif name == 'editor':
    #     #     self.text_view.grab_focus()
    #     #     self.new_button.hide()
    #     #     self.del_button.hide()
    #     #     self.back_button.show()
    #     #     self.find_button.hide()
    #     #     self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_RIGHT)
    #     pass

    # def populate_model(self):

    #     # for idx, key in enumerate(keys):
    #     #     self.model.append([idx])

    #     for idx in self.db.notes.keys():
    #         self.model.append([idx])
    #         # if not '@trash' in self.db.get_note_prop(idx, 'tags'):
    #         #     self.idx.append(idx)

    # def refilter_model(self, filter_txt=''):
    #     del self.show_idx[:]
    #     matches_idx = self.db.search_matches(filter_txt)
    #     for idx in matches_idx:
    #         self.show_idx.append(idx)
    #     self.model_filter.refilter()

    # def resort_model(self):
    #     """ trick to sort the model """
    #     self.model_filter[0][0] = self.model_filter[0][0]

    # def new_note(self):
    #     idx = self.db.new_note()
    #     self.model.append([idx])
    #     self.idx.append(idx)
    #     self.model_filter.refilter()
    #     self.modelview.set_cursor(Gtk.TreePath(0), self.modelview.get_column(0), True)

    # def delete_note(self):
    #     if len(self.model) == 0:
    #         return

    #     (model, treeiter) = self.selection.get_selected()
    #     if treeiter is not None:
    #         idx = model[treeiter][0]
    #         self.db.add_tags(idx, '@trash')
    #         self.refilter_model()

    # def edit_note(self):
    #     if len(self.model) == 0:
    #         return

    #     (model, treeiter) = self.selection.get_selected()
    #     if treeiter is None:
    #         return

    #     idx = model[treeiter][0]
    #     content = self.db.get_note_prop(idx, 'content')
    #     self.text_buffer.set_text(content)

    #     self.show_view('editor')

    #     title = self.db.get_note_prop(idx, 'title')
    #     self.title.set_label(title)

    #     self.current_idx = idx

    # def exit_edit_note(self):
    #     text = self.text_buffer.get_text(self.text_buffer.get_start_iter(),
    #                                      self.text_buffer.get_end_iter(), True)
    #     self.db.update_note_prop(self.current_idx, 'content', text)
    #     self.text_buffer.set_text('')
    #     self.show_view('list')
    #     self.current_idx = None

    def show_hide(self, *args):
        if self.window.get_visible():
            self.size = self.window.get_size()
            self.pos = self.window.get_position()
            self.window.hide()
        else:
            self.window.present()
            self.window.resize(int(self.size[0]), int(self.size[1]))
            self.window.move(int(self.pos[0]), int(self.pos[1]))

    # def show_searchbar(self):
    #     if self.searchbar.get_search_mode():
    #         self.searchbar.set_search_mode(False)
    #         self.entry.set_text('')
    #     else:
    #         self.searchbar.set_search_mode(True)
    #         self.entry.grab_focus()

    # def compare_fn(self, model, row1, row2, user_data):
    #     idx1 = model.get_value(row1, 0)
    #     idx2 = model.get_value(row2, 0)

    #     # date1 = self.db.get_note_prop(idx1, 'utime')
    #     # date2 = self.db.get_note_prop(idx2, 'utime')

    #     return idx1 > idx2 ##(date1 > date2) - (date1 < date2)

    # def cell_data_fn_title(self, column, cell, model, treeiter, data=None):
    #     ifile = model.get_value(treeiter, 0)
    #     iitem = model.get_value(treeiter, 1)

    #     # title = self.db.files[ifile].items[iitem]

    #     #if self.db.get_note_prop(idx, 'content'):
    #     #    title += '<i><span foreground=\'grey\'> ... </span></i>'
    #     # if '!' in title:
    #     #     title = '<b>' + title + '</b>'
    #     cell.set_property('markup', title)

    # def cell_data_fn_tags(self, column, cell, model, treeiter, data=None):
    #     idx = model.get_value(treeiter, 0)
    #     #tags = self.db.get_note_prop(idx, 'tags')
    #     cell.set_property('text', 'hola')

    def cell_data_fn_utime(self, column, cell, model, treeiter, data=None):
        # idx = model.get_value(treeiter, 0)
        # timestamp = self.db.get_note_prop(idx, 'utime')
        # ts = float(timestamp)
        # dt = datetime.fromtimestamp(ts)
        # now = datetime.now()
        # time_str = ''

        # if dt.date() == now.date():          # today -> 'HH:MM'
        #     time_str = dt.strftime('%H:%M')
        # elif dt.year == now.year:            # this year - > 'Month Day'
        #     time_str = dt.strftime('%b') + ' ' + str(dt.day)
        # else:                                # before -> 'Month Day, Year'
        #     time_str = '%s %d, %d' % (dt.strftime('%b'), dt.day, dt.year)

        # cell.set_property('text', time_str)
        pass

    # def visible_fn(self, model, treeiter, data):
    #     return model.get_value(treeiter, 0) in data

    # def on_search(self, entry):
    #     txt = entry.get_text().lower()
    #     self.refilter_model(txt)

    # def on_cell_editing_started(self, cell, entry, path, data=None):
    #     entry.set_text(entry.get_text().replace('...', '').strip())

    # def on_cell_edit(self, widget, path, text):
    #     pass
    #     tags = tags_re.findall(text)
    #     rmtags = [ t.replace('-', '@') for t in rmtags_re.findall(text) ]

    #     title = tags_re.sub('', text)
    #     title = rmtags_re.sub('', title)

    #     idx = self.get_idx(path)
    #     self.db.update_note_prop(idx, 'title', title)
    #     self.db.add_tags(idx, *tags)
    #     self.db.remove_tags(idx, *rmtags)
    #     self.refilter_model()
    #     self.resort_model()

    # def on_find_toggle(self, btn):
    #     self.show_searchbar()

    # toolbar callbacks
    # def on_new_press(self, btn):
    #     self.new_note()

    # def on_del_press(self, btn):
    #     self.delete_note()

    # def on_edit_press(self, btn):
    #     self.edit_note()

    # def on_back_press(self, btn):
    #     self.exit_edit_note()

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
            elif key == 'n':
                # self.new_note()
                self.draw()


            ## ctrl-c: clear selection
            elif key == 'c':
                self.plot_model.clear()

            ## ctrl-d: delete note
            # elif key == 'd':
            #     self.delete_note()

            ## ctrl-h: hide window
            # elif self.stack.get_visible_child_name() == 'list' and key == 'h':
            #     self.show_hide()

            ## ctrl-x: be sure to do nothing!
            elif key == 'x':
                pass

            ## ctrl-s: update current note content
            # elif key == 's':
            #     text = self.text_buffer.get_text(self.text_buffer.get_start_iter(),
            #                                      self.text_buffer.get_end_iter(), True)
            #     self.db.update_note_prop(self.current_idx, 'content', text)

            return False


    def selected_row_callback(self, treesel, model, path, nose, ifile):

        treeiter = model.get_iter(path)
        ifile = model.get_value(treeiter, 0)
        iitem = model.get_value(treeiter, 1)
        iname = model.get_value(treeiter, 2)

        self.plot_model.append((ifile, iitem, iname))

        return False

    def on_clear(self, a):
        self.plot_model.clear()

    def on_draw(self, a):
        self.draw()

    def on_draw_ratio(self, a):
        pass

    def on_draw_and_ratio(self, a):
        pass


    def draw(self):

        """ Draw function. Creates a plot with the selected items and options """

        if not self.plot_model:
            return

        print self.plot_model

        canvas = ROOT.TCanvas()

        for (ifile, iitem, iname) in self.plot_model:

            print ifile, iitem, iname

            obj = self.db.get_object(ifile, iitem, iname)
            print obj
            obj.Draw('same')


        self.plots.append(canvas)

        # h.Draw()

        # Plot order: 1) Selected order (default). 2) Order by file and entry.
        # if(check_order.GetState())  sort(self._items.begin(), self._items.end())

        #p = Plot()

        # p.set_logx(self.check_logx.GetState())
        # p.set_logy(self.check_logy.GetState())


        # self.get_colours()

        # for i, item in enumerate(self.items):
        #     if not item.is_plotable():
        #         msg_error("")
        #         continue
        #     p.add(self.get_object(item), self.colours[i])

        # if self.check_include_ratio.GetState():
        #     p.set_include_ratio(True)
        # elif self.check_include_diff.GetState():
        #     p.set_include_diff(True)

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

        # p.set_draw_options(draw_opts)

        # p.create()

        # self.plots.append(p)
