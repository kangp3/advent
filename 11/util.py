from copy import deepcopy


class Grid:
    def __init__(self):
        self.grid = []

    @classmethod
    def from_file(cls, fname, sep=None, type=None):
        g = Grid()
        with open(fname) as f:
            for line in f:
                row = []

                vals = line.strip()
                if sep is not None:
                    vals = vals.split(sep)
                for val in vals:
                    if type is None:
                        row.append(val)
                    else:
                        row.append(type(val))

                g.grid.append(row)
        return g

    def copy(self):
        new = Grid()
        new.grid = deepcopy(self.grid)
        return new

    def __iter__(self):
        return self.grid.__iter__()

    def __repr__(self):
        return '\n'.join(self.grid)

    def __getitem__(self, key):
        return self.grid[key]

    def __setitem__(self, key, val):
        self.grid[key] = val

    def __contains__(self, coords):
        if isinstance(coords, complex):
            row_idx = int(coords.real)
            col_idx = int(coords.imag)
        elif isinstance(coords, GridCoord):
            row_idx = coords.row
            col_idx = coords.col
        return 0 <= row_idx < self.width and 0 <= col_idx < self.height

    @property
    def width(self):
        return len(self.grid)

    @property
    def height(self):
        return len(self.grid[0])

    def coord(self, coords):
        return GridCoord(self, coords)


class GridCoord:
    def __init__(self, grid, coords):
        self.grid = grid
        self.coords = coords

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, o):
        return self.row == o.row and self.col == o.col

    def __ne__(self, o):
        return self.row != o.row or self.col != o.col

    @property
    def row(self):
        return int(self.coords.real)

    @property
    def col(self):
        return int(self.coords.imag)

    def offset(self, off):
        return self.grid.coord(self.coords + off)

    def neighbors(self, include_diagonals=False):
        offsets = [-1, 1j, 1, -1j]
        if include_diagonals:
            offsets = [-1, -1+1j, 1j, 1j+1, 1, 1-1j, -1j, -1j-1]
        return [
            self.offset(off)
            for off in offsets
            if self.offset(off) in self.grid
        ]
