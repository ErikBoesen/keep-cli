import urwid
import logging
import gkeepapi
import widget.note
import widget.edit
import application
import query

class Grid(urwid.Filler):
    def __init__(self, app: 'application.Application', q: query.Query):
        self.application = app
        self.query = q

        size = app.config.get('size', {})
        self.size = (size.get('width', 26), size.get('height', 10))

        self.w_grid = urwid.GridFlow([], self.size[0], 1, 1, urwid.LEFT)

        super(Grid, self).__init__(self.w_grid, valign=urwid.TOP)

    def refresh(self, keep: gkeepapi.Keep):
        self.w_grid.contents = [
            (urwid.BoxAdapter(widget.note.Note(n), self.size[1]), self.w_grid.options()) for n in self.query.filter(keep)
        ]
        if self.w_grid.contents:
            self.w_grid.focus_position = 0

    def selectable(self):
        return True

    def keypress(self, size, key):
        if key == 'j':
            key = 'down'
        elif key == 'k':
            key = 'up'
        elif key == 'h':
            key = 'left'
        elif key == 'l':
            key = 'right'
        elif key == 'c':
            note = self.application.keep.createNote()
            w_edit = widget.edit.Edit(self.application, note)
            self.application.push(w_edit)
            key = None
        elif key == 'C':
            note = self.application.keep.createList()
            w_edit = widget.edit.Edit(self.application, note)
            self.application.push(w_edit)
            key = None
        elif key == 'enter':
            if self.w_grid.focus is not None:
                w_edit = widget.edit.Edit(self.application, self.w_grid.focus.note)
                self.application.push(w_edit)
            key = None
        elif key == 'esc':
            self.application.pop()
            key = None
        if self.w_grid.focus is not None:
            key = super(Grid, self).keypress(size, key)
        return key
