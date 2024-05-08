from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: int
    y: int
    width: int
    height: int

    def __iter__(self):
        return iter((self.x, self.y, self.width, self.height))
