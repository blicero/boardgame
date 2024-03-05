#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2024-03-05 18:38:48 krylon>
#
# /home/krylon/OneDrive/Dokumente/code/boardgame/server/board.py
# created on 29. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY BENJAMIN WALKENHORST ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

"""
board

(c) 2024 Benjamin Walkenhorst
"""

import math
from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple, Optional


class Field(NamedTuple):
    """One field on the board"""

    elevation: int
    terrain: str


class Direction(Enum):
    """Describe the direction of a move."""
    Up = auto()
    UpRight = auto()
    Right = auto()
    DownRight = auto()
    Down = auto()
    DownLeft = auto()
    Left = auto()
    UpLeft = auto()


@dataclass(slots=True)
class Vector:
    """Vector can be both a position on a board and a direction and distance of movement."""
    x: int
    y: int

    def length(self) -> float:
        """Return the length of a vector"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def distance(self, other: 'Vector') -> float:
        """Return the distance between the Vector and the given other Vector"""
        return (other - self).length()

    def __eq__(self, other) -> bool:
        return isinstance(other, Vector) and (self.x == other.x) and (self.y == other.y)

    def __sub__(self, other: 'Vector') -> 'Vector':
        delta = Vector(self.x - other.x, self.y - other.y)
        return delta

    def __add__(self, heading: Direction) -> 'Vector':
        x: int = self.x
        y: int = self.y
        match heading:
            case Direction.Up:
                y += 1
            case Direction.UpRight:
                x += 1
                y += 1
            case Direction.Right:
                x += 1
            case Direction.DownRight:
                x += 1
                y -= 1
            case Direction.Down:
                y -= 1
            case Direction.DownLeft:
                x -= 1
                y -= 1
            case Direction.Left:
                x -= 1
            case Direction.UpLeft:
                x -= 1
                y += 1
            case _:
                raise ValueError(f"Invalid Direction: {heading}")
        return Vector(x, y)


class Board:  # pylint: disable-msg=R0903
    """The Board where it all happens"""

    __slots__ = [
        "size",
        "fields",
    ]

    size: tuple[int, int]
    fields: list[list[Field]]

    def __init__(self, fields: list[list[Field]]):
        self.fields = fields
        self.size = (len(fields), len(fields[0]))

        for i in range(1, len(fields)):
            assert len(fields[i]) == len(fields[0])

    def pos_valid(self, p: Vector) -> bool:
        """Check if the given Vector points to a Field on the Board"""
        return 0 <= p.x < self.size[0] and 0 <= p.y < self.size[1]


@dataclass(slots=True, kw_only=True)
class Piece:
    """A game piece"""

    pid: int
    name: str
    hp: int
    ap: int
    attack_range: int
    pos: Vector

    def __init__(self, **fields):
        self.pid = fields.get("pid", 0)
        self.name = fields["name"]
        self.hp = fields["hp"]
        self.ap = fields["ap"]
        self.attack_range = fields.get("attack_range", 1)
        self.pos = fields.get("pos", Vector(0, 0))

        assert self.hp > 0, \
            f"Invalid HP: {self.hp} (must be a positive integer)"
        assert self.ap > 0, \
            f"Invalid AP: {self.ap} (must be a positive integer)"
        assert self.attack_range > 0, \
            f"Invalid attack_range: {self.attack_range} (must be a positive integer)"  # noqa: E501

    def distance(self, pos: Vector) -> float:
        """Return the distance between the Pieces current position and the given position."""
        delta: Vector = pos - self.pos
        return delta.length()

    def move(self, d: Direction):
        """Move the piece one field in the given Direction"""
        self.pos = self.pos + d


class Game:  # pylint: disable-msg=R0903
    """A game. We'll see where this goes."""

    # I would like have some kind of history.

    __slots__ = [
        "board",
        "pieces",
        "turn",
        "history",
    ]

    board: Board
    pieces: list[Piece]
    turn: int
    history: list

    def move(self, p: Piece, dst: Vector) -> None:
        """Attempt to move a piece to the given position."""
        # orig_dist: float = p.distance(dst)
        dist: float = p.distance(dst)  # math.inf
        move_dir: Optional[Direction] = None
        for d in Direction:
            new_pos: Vector = p.pos + d
            if self.board.pos_valid(new_pos):
                new_dist: float = new_pos.distance(dst)
                if new_dist < dist:
                    dist = new_dist
                    move_dir = d
        if move_dir is not None:
            p.move(move_dir)

# Local Variables: #
# python-indent: 4 #
# End: #
