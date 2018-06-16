import urwid
import logging
import gkeepapi
import widget.note
import query

class Grid(urwid.Filler):
    def __init__(self, q: query.Query):
        self.query = q
        self.w_grid = urwid.GridFlow([], 20, 1, 1, urwid.LEFT)

        super(Grid, self).__init__(self.w_grid, valign=urwid.TOP)

    def refresh(self, keep: gkeepapi.Keep):
        self.w_grid.contents = [
            (urwid.BoxAdapter(widget.note.Note(n), 10), self.w_grid.options()) for n in self.query.filter(keep)
        ]

    def keypress(self, size, key):
        if key == 'j':
            key = 'down'
        elif key == 'k':
            key = 'up'
        elif key == 'h':
            key = 'left'
        elif key == 'l':
            key = 'right'
        super(Grid, self).keypress(size, key)
        return key
