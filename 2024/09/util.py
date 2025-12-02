from copy import deepcopy


class Grid:
    def __init__(self):
        self.grid = []

    @classmethod
    def from_file(fname, sep=None):
        with open(fname) as f:
            for line in f:
                row = []

                vals = line.strip()
                if sep is not None:
                    vals = vals.split(sep)
                for val in vals:
                    row.append(val)

                self.grid.append(row)

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
        return 0 <= coords[0] < self.width and 0 <= coords[1] < self.height

    @property
    def width(self):
        return len(self.grid)

    @property
    def height(self):
        return len(self.grid[0])
