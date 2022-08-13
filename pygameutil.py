import itertools
from typing import Any, Callable
import random

import pygame


class Text:
    def __init__(self, font: pygame.font.Font | tuple,
                 text: str | bytes, color: Any, *, antialias: bool = True,
                 background: Any | None = None):
        if isinstance(font, pygame.font.Font):
            self.font = font
        elif isinstance(font, tuple):
            self.font = pygame.font.Font(*font)
        self.text = text
        self.color = color
        self.antialias = antialias
        self.background = background
        self.surface = self.font.render(text, antialias, color, background)
        self.rect = self.surface.get_rect()

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


class Button:
    def __init__(self, text: Text, inactive: Any, active: Any,
                 rect: pygame.Rect | tuple | None = None,
                 onclick: Callable = None):
        self.text = text
        self.inactive = inactive
        self.active = active
        if isinstance(rect, pygame.Rect):
            self.rect = rect
        elif isinstance(rect, tuple):
            self.rect = pygame.Rect(*rect)
        else:
            self.rect = self.text.rect
        self.onclick = (lambda *args, **kwargs: None) if onclick is None else onclick

    def __bool__(self):
        return self.collidepoint(pygame.mouse.get_pos())

    def collidepoint(self, *args):
        return self.rect.collidepoint(*args)

    def draw(self, surface):
        if self:
            pygame.draw.rect(surface, self.active, self.rect)
class AbstractGrid:
    def __init__(self, grid_type, grid=None, *, row=0, col=0, fill=None):
        self.grid_type = grid_type
        self.obrace, self.cbrace = str(grid_type())
        if grid is None:
            self.grid = grid_type(grid_type(fill for _ in range(col)) for _ in range(row))
        else:
            pygame.draw.rect(surface, self.inactive, self.rect)
        surface.blit(self.text.surface, self.text.rect)

    def click(self, *args, **kwargs):
        self.onclick(*args, **kwargs)


            self.grid = grid_type(grid_type(row) for row in grid)

    # region Comparison methods
    def __lt__(self, other):
        return self.grid < other

    def __le__(self, other):
        return self.grid <= other

    def __eq__(self, other):
        return self.grid == other

    def __ne__(self, other):
        return self.grid != other

    def __gt__(self, other):
        return self.grid > other

    def __ge__(self, other):
        return self.grid >= other

    # endregion

    # region Iteration methods
    def __iter__(self):
        return iter(self.grid)

    def __reversed__(self):
        return reversed(self.grid)

    def positions(self):
        return [(x, y) for x in range(len(self)) for y in range(len(self[0]))]

    # endregion

    # region Item-related methods
    def __contains__(self, value):
        return value in self.grid or any(value in row for row in self.grid)

    def count(self, value):
        count = self.grid.count(value)
        for row in self.grid:
            count += row.count(value)
        return count

    def index(self, *args):
        value = args[0]
        start = slice(None) if len(args) < 2 else args[1]
        stop = slice(None) if len(args) < 3 else args[2]
        if isinstance(start, int):
            x_offset = start
        else:
            x_offset = 0 if start.start is None else start.start
        if isinstance(stop, int):
            y_offset = stop
        else:
            y_offset = 0 if stop.start is None else stop.start
        search_grid = self[start, stop]
        if value in search_grid:
            return x_offset + search_grid.index(value)
        if len(search_grid) != 0 and isinstance(search_grid[0], self.grid_type):
            for x in range(len(search_grid)):
                for y in range(len(search_grid[x])):
                    if search_grid[x][y] == value:
                        return x_offset + x, y_offset + y
        raise ValueError(f"{value} is not in {type(self).__name__}")

    def __getitem__(self, key):
        if isinstance(key, tuple):
            x = slice(None) if len(key) == 0 else key[0]
            y = slice(None) if len(key) < 2 else key[1]
            if isinstance(x, int):
                return self.grid[x][y]
            return self.grid_type(row[y] for row in self.grid[x])
        else:
            return self.grid[key]

    # make work with slice objects
    def line(self, *args):
        def change_move(move, arg, i):
            if isinstance(arg, int):
                move[i] = (arg,) * 2
            elif isinstance(arg, tuple) and len(arg) != 0:
                if len(arg) == 1 and arg[0] is not None:
                    move[i] = arg * 2
                else:
                    if arg[0] is not None:
                        move[i] = (arg[0], move[i][1])
                    if arg[1] is not None:
                        move[i] = (move[i][0], arg[1])

        move = [(0, 0), (len(self), len(self[0])), (1, 1)]

        if len(args) == 1:
            if isinstance(args[0], slice):
                change_move(move, args[0].start, 0)
                change_move(move, args[0].stop, 1)
                change_move(move, args[0].step, 2)
            else:
                change_move(move, args[0], 1)
        elif len(args) >= 2:
            if isinstance(args[0], slice) or isinstance(args[1], slice):
                if isinstance(args[0], slice) ^ isinstance(args[1], slice):
                    raise TypeError("Both arguments must be slice objects if one of them is")
                change_move(move, (args[0].start, args[1].start), 0)
                change_move(move, (args[0].stop, args[1].stop), 1)
                change_move(move, (args[0].step, args[1].step), 2)
            else:
                change_move(move, args[0], 0)
                change_move(move, args[1], 1)
                if len(args) >= 3:
                    change_move(move, args[2], 2)



        # need to check indices to make sure in bounds


        start, stop, step = move
        x_indices = [x for x in range(start[0], stop[0], step[0])]
        y_indices = [y for y in range(start[1], stop[1], step[1])]
        items = []
        for k in range(min(len(x_indices), len(y_indices))):
            items.append(self.grid[x_indices[k]][y_indices[k]])
        return items

    # endregion

    def __len__(self):
        return len(self.grid)

    def __str__(self):
        string = self.obrace
        if len(self) != 0:
            values = [[repr(value) for value in row] for row in self]
            maxlen = max([len(values[x][y]) for x in range(len(self)) for y in range(len(self[0]))])
            for x in range(len(values)):
                string += self.obrace
                for y in range(len(values[x])):
                    string += f"{values[x][y]: >{maxlen}}, "
                string += f"\b\b{self.cbrace}"
                if x != len(values) - 1:
                    string += "\n "
        string += self.cbrace
        return string


class ImmutableGrid(AbstractGrid):
    def __init__(self, grid=None, *, row=0, col=0, fill=None):
        super().__init__(tuple, grid, row=row, col=col, fill=fill)

    def __hash__(self):
        return hash(self.grid)


class Grid(AbstractGrid):
    def __init__(self, grid=None, default_grid=None, *, row=0, col=0, fill=None):
        super().__init__(list, grid, row=row, col=col, fill=fill)
        self.default = ImmutableGrid(default_grid, row=len(self.grid), col=len(self.grid[0]), fill=fill)

    # make sure to include setting sliced i.e. g[1:4, :2] = value   and   g[1:4, :2] = iterable
    def __setitem__(self, key, value):
        def set_slice(indices):  # need to check indices to make sure in bounds
            rows = len(self)
            if isinstance(indices[0], int):
                for i in range(len(indices) - 1, -1, -1):
                    if not indices[i] < rows:
                        indices.pop(i)
            else:
                cols = len(self[0])
                for i in range(len(indices) - 1, -1, -1):
                    if not indices[i][0] < rows and not indices[i][1] < cols:
                        indices.pop(i)
            try:
                if len(value) == len(indices):
                    if isinstance(indices[0], int):
                        for i in range(len(indices)):
                            self.grid[indices[i]] = value[i]
                    else:
                        for i in range(len(indices)):
                            row, col = indices[i]
                            self.grid[row][col] = value[i]
                else:
                    raise TypeError()
            except TypeError:
                if isinstance(indices[0], int):
                    for i in indices:
                        self.grid[i] = value
                else:
                    for row, col in indices:
                        self.grid[row][col] = value

        if isinstance(key, int):
            set_slice([(key, col) for col in range(len(self[key]))])
        elif isinstance(key, tuple):
            if len(key) == 1:
                if isinstance(key[0], int):
                    row = key[0]
                    set_slice([(row, col) for col in range(len(self[row]))])
                elif isinstance(key[0], slice):
                    row_indices = [x for x in range(*key[0].indices(len(self)))]
                    col_indices = [y for y in range(len(self[0]))]
                    for row, col in itertools.product(row_indices, col_indices):
                        self.grid[row][col] = value
            elif len(key) == 2:
                if isinstance(key[0], int):
                    if isinstance(key[1], int):
                        self.grid[key[0]][key[1]] = value
                    elif isinstance(key[1], slice):
                        row = key[0]
                        set_slice([(row, col) for col in range(*key[1].indices(len(self[0])))])
                elif isinstance(key[0], slice):
                    if isinstance(key[1], int):
                        col = key[1]
                        set_slice([(row, col) for row in range(*key[0].indices(len(self)))])
                    elif isinstance(key[1], slice):
                        row_indices = [x for x in range(*key[0].indices(len(self)))]
                        col_indices = [y for y in range(*key[1].indices(len(self[0])))]
                        for row, col in itertools.product(row_indices, col_indices):
                            self.grid[row][col] = value
        elif isinstance(key, slice):
            set_slice([row for row in range(*key.indices(len(self)))])

    def __delitem__(self, *args):
        if isinstance(args[0], tuple):
            args = args[0]
        if len(args) == 1:
            self.grid[args[0]] = self.default[args[0]].copy()
        else:
            if isinstance(args[0], slice):
                sliced_grid = self.grid[args[0]]
                sliced_default = self.default[args[0]]
                for i in range(len(sliced_grid)):
                    sliced_grid[i][args[1]] = sliced_default[i][args[1]]
            else:
                self.grid[args[0]][args[1]] = self.default[args[0]][args[1]]

    def copy(self):
        return Grid(self.grid.copy())

    def flip(self, h=True, v=True):
        if h:
            for row in self:
                row.reverse()
        if v:
            self.grid.reverse()

    def unset_positions(self):
        return [pos for pos in self.positions() if self[pos] == self.default[pos]]

    def set_positions(self):
        return [pos for pos in self.positions() if self[pos] != self.default[pos]]

    def is_default(self, key):
        return self[key] == self.default[key]

    def shuffle(self):
        rows = len(self)
        cols = len(self[0])
        flattened = [item for row in self.grid for item in row]
        random.shuffle(flattened)
        for row in range(rows):
            self[row][:] = flattened[cols * row:cols * row + cols]


    # maybe have this?
    # either set the value to value returned by func if not None or don't change values
    # def foreach(self, func):
    #     pass


class GridBoard(Grid):
    # take arguments for Board when Board is implemented
    def __init__(self, grid=None, default_grid=None, *, row=0, col=0, fill=None):
        super().__init__(grid, row=row, col=col, fill=fill)
        self.default = Grid(default_grid, row=len(self.grid), col=len(self.grid[0]), fill=fill)

    # add update method to update image
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        # self.update()

    # add update method to update image
    def __delitem__(self, *args):
        super().__delitem__(*args)
        # self.update()

    def __repr__(self):
        return f"GridBoard({len(self)}, {len(self[0])}, grid={self.grid}, default_grid={self.default})"

    def copy(self):
        return GridBoard(len(self), len(self[0]), grid=self.copy(), default_grid=self.default.copy())

    def remove(self, value):
        del self[self.index(value)]
        # self.update()

    # add update method to update image
    def clear(self, *args):
        if len(args) == 0:
            args = (slice(None), slice(None))
        self.__delitem__(*args)

    # make signature take just mouse_pos and get screen_size and pos_length from Board (take in __init__)
    def get_pos(self, mouse_pos, screen_size, pos_length):
        pos = -1
        if 0 < mouse_pos[0] < screen_size[0] and 0 < mouse_pos[1] < screen_size[1]:
            row = mouse_pos[1] // pos_length
            col = mouse_pos[0] // pos_length
            if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
                pos = (row, col)
        return pos
