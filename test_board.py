#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2024-03-07 21:56:59 krylon>
#
# /home/krylon/OneDrive/Dokumente/code/boardgame/game/test_board.py
# created on 05. 03. 2024
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
game.test_board

(c) 2024 Benjamin Walkenhorst
"""

import math
import unittest

from boardgame.board import Board, Direction, Vector


class TestVector(unittest.TestCase):
    """Test the Vector class"""

    def test_01_eq(self) -> None:
        """Test for equality"""
        test_cases = [
            (Vector(5, 7), Vector(5, 7), True),
            (Vector(1, 1), Vector(24, 17), False),
        ]

        for c in test_cases:
            result = c[0] == c[1]
            self.assertEqual(result, c[2])

    def test_02_sub(self) -> None:
        """Test subtraction."""
        test_cases = [
            (Vector(10, 10), Vector(5, 5), Vector(5, 5)),
            (Vector(5, 5), Vector(5, 5), Vector(0, 0)),
        ]

        for c in test_cases:
            v = c[0] - c[1]
            self.assertEqual(v, c[2])

    def test_03_add(self) -> None:
        """Test addition."""
        test_cases = [
            (Vector(0, 0), Direction.Up, Vector(0, 1)),
            (Vector(25, 2), Direction.DownLeft, Vector(24, 1)),
            (Vector(19, 5), Direction.Right, Vector(20, 5)),
        ]

        for c in test_cases:
            v = c[0] + c[1]
            self.assertEqual(v, c[2])

    def test_04_length(self) -> None:
        """Test the length method."""
        test_cases = [
            (Vector(0, 0), 0),
            (Vector(1, 1), math.sqrt(2)),
        ]

        for c in test_cases:
            r = c[0].length()
            self.assertEqual(r, c[1])


class TestBoard(unittest.TestCase):
    """Test the Board"""

    def test_01_pos_valid(self) -> None:
        """Test if we can tell valid places from invalid ones."""
        # b = Board([[Field(0, "Grass") for x in range(20)] for x in range(20)])
        b = Board.make_plain_board(20, 20)

        test_cases = [
            (Vector(2, 7), True),
            (Vector(42, 1), False),
            (Vector(19, 19), True),
            (Vector(0, 0), True),
            (Vector(19, 0), True),
            (Vector(0, 19), True),
            (Vector(-1, 0), False),
        ]

        for c in test_cases:
            r = b.pos_valid(c[0])
            self.assertEqual(r, c[1])

    def test_02_path(self) -> None:
        """Test the naive path finding algorithm."""
        b = Board.make_plain_board(8, 8)
        test_cases = [
            (Vector(0, 0), Vector(7, 7), [Direction.UpRight for x in range(7)]),
            (Vector(0, 0), Vector(7, 0), [Direction.Right for x in range(7)]),
            (Vector(4, 4), Vector(5, 4), [Direction.Right]),
        ]

        for c in test_cases:
            p = b.path_straight(c[0], c[1])
            self.assertIsNotNone(p)
            assert p is not None
            self.assertCountEqual(p, c[2])

# Local Variables: #
# python-indent: 4 #
# End: #
