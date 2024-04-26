# extracted from Louie, http://pylouie.org/
# updated for Python 3
#
# Copyright (c) 2006 Patrick K. O'Brien, Mike C. Fletcher,
#                    Matthew R. Scott
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * Neither the name of the <ORGANIZATION> nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import typing as t
import unittest

from blinker._saferef import safe_ref


class _Sample1:
    def x(self) -> None:
        pass


def _sample2(obj: t.Any) -> None:
    pass


class _Sample3:
    def __call__(self, obj: t.Any) -> None:
        pass


class TestSaferef(unittest.TestCase):
    # XXX: The original tests had a test for closure, and it had an
    # off-by-one problem, perhaps due to scope issues.  It has been
    # removed from this test suite.

    def setUp(self) -> None:
        samples: list[t.Any] = []
        refs: list[t.Any] = []
        for _ in range(100):
            sample: t.Any = _Sample1()
            samples.append(sample)
            ref = safe_ref(sample.x, self._closure)
            refs.append(ref)
        samples.append(_sample2)
        refs.append(safe_ref(_sample2, self._closure))
        for _ in range(30):
            sample = _Sample3()
            samples.append(sample)
            ref = safe_ref(sample, self._closure)
            refs.append(ref)
        self.ts = samples
        self.ss = refs
        self.closure_count = 0

    def tearDown(self) -> None:
        if hasattr(self, "ts"):
            del self.ts
        if hasattr(self, "ss"):
            del self.ss

    def test_In(self) -> None:
        """Test the `in` operator for safe references (cmp)"""
        for sample in self.ts[:50]:
            assert safe_ref(sample.x) in self.ss

    def test_Valid(self) -> None:
        """Test that the references are valid (return instance methods)"""
        for s in self.ss:
            assert s()

    def test_ShortCircuit(self) -> None:
        """Test that creation short-circuits to reuse existing references"""
        sd = {}
        for s in self.ss:
            sd[s] = 1
        for sample in self.ts:
            if hasattr(sample, "x"):
                assert safe_ref(sample.x) in sd
            else:
                assert safe_ref(sample) in sd

    def test_Representation(self) -> None:
        """Test that the reference object's representation works

        XXX Doesn't currently check the results, just that no error
            is raised
        """
        repr(self.ss[-1])

    def _closure(self, ref: t.Any) -> None:
        """Dumb utility mechanism to increment deletion counter"""
        self.closure_count += 1
