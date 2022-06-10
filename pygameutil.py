from typing import Any, Callable

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
                 onclick: Callable = lambda *args, **kwargs: None):
        self.text = text
        self.inactive = inactive
        self.active = active
        if isinstance(rect, pygame.Rect):
            self.rect = rect
        elif isinstance(rect, tuple):
            self.rect = pygame.Rect(*rect)
        else:
            self.rect = self.text.rect
        self.onclick = onclick

    def __bool__(self):
        return self.collidepoint(pygame.mouse.get_pos())

    def collidepoint(self, *args):
        return self.rect.collidepoint(*args)

    def draw(self, surface):
        if self:
            pygame.draw.rect(surface, self.active, self.rect)
        else:
            pygame.draw.rect(surface, self.inactive, self.rect)
        surface.blit(self.text.surface, self.text.rect)

    def click(self, *args, **kwargs):
        self.onclick(*args, **kwargs)


class Grid:
    def __init__(self, row, col, *, fill=None, grid=None):
        self.grid = [[fill] * col] * row if grid is None else grid

    # region list magic methods
    # Special method lookup bypasses __getattribute__ and __getattr__, so define explicitly

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
    # endregion

    def __len__(self):
        return len(self.grid)

    def __contains__(self, value):
        return value in self.grid

    # endregion

    def __getattr__(self, name):
        return getattr(self.grid, name)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            x = slice(None, None, None) if len(key) == 0 else key[0]
            y = slice(None, None, None) if len(key) < 2 else key[1]
            if isinstance(x, int):
                return self.grid[x][y]
            sliced = []
            rows = self.grid[x]
            for row in rows:
                sliced.append(row[y])
            return sliced
        else:
            return self.grid[key]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            pass

    def __delitem__(self, *args):
        if isinstance(args[0], tuple):
            args = args[0]
        if len(args) == 1:
            del self.grid[args[0]]
        else:
            if isinstance(args[0], slice):
                sliced = self.grid[args[0]]
                for i in range(len(sliced)):
                    del sliced[i][args[1]]
            else:
                del self.grid[args[0]][args[1]]

    def __str__(self):
        values = [[repr(value) for value in row] for row in self]
        maxlen = max([len(values[x][y]) for x in range(len(self)) for y in range(len(self[0]))])
        string = "["
        for x in range(len(values)):
            string += "["
            for y in range(len(values[x])):
                string += f"{values[x][y]: >{maxlen}}, "
            string += "\b\b]"
            if x != len(values) - 1:
                string += "\n "
        string += "]"
        return string

    def index(self, *args):
        value = args[0]
        start = 0 if len(args) < 2 else args[1]
        end = len(self.grid) if len(args) < 3 else args[2]


    def count(self, value):
        def recur_count(array):
            if len(array) == 0:
                return 0
            if not isinstance(array[0], list):
                return array.count(value)
            count = array.count(value)
            for child_array in array:
                count += recur_count(child_array)
            return count

        return recur_count(self.grid)

    def line(self, *args):
        if len(args) == 0:
            raise TypeError("line expected at least 1 argument, got 0")
        start, stop, step = (0, 0), (len(self), len(self[0])), (1, 1)
        if len(args) == 1:
            pass

        x_indices = [x for x in range(start[0], stop[0], step[0])]
        y_indices = [y for y in range(start[1], stop[1], step[1])]
        items = []
        for k in range(min(len(x_indices), len(y_indices))):
            items.append(self.grid[x_indices[k]][y_indices[k]])
        return items

    def positions(self):
        return [(x, y) for x in range(len(self)) for y in range(len(self[0]))]


class GridBoard(Grid):
    # take arguments for Board
    def __init__(self, row, col, *, fill=None, grid=None, default_grid=None):
        # instead of using fill for __delitem__, just replace item at that index with the item in default
        super().__init__(row, col, fill=fill, grid=grid)
        self.default = Grid(row, col, fill=fill, grid=default_grid)

    def __contains__(self, value):
        return any(value in row for row in self.grid) or value in self.grid

    # add update method to update surface
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        # self.update()

    # add update method to update surface
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
        # self.update()

    def __repr__(self):
        return f"GridBoard({len(self)}, {len(self[0])}, grid={self.grid}, default_grid={self.default})"

    def copy(self):
        return GridBoard(len(self), len(self[0]), grid=self.copy(), default_grid=self.default.copy())

    def remove(self, value):
        pass

    # add update method to update surface
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

    def unset_positions(self):
        return [pos for pos in self.positions() if self[pos] == self.default[pos]]

    def set_positions(self):
        return [pos for pos in self.positions() if self[pos] != self.default[pos]]

    def is_default(self, key):
        return self[key] == self.default[key]
