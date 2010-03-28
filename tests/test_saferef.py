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
#
import unittest

from blinker._saferef import safe_ref


class _Sample1(object):
    def x(self):
        pass


def _sample2(obj):
    pass


class _Sample3(object):
    def __call__(self, obj):
        pass


class TestSaferef(unittest.TestCase):

    # XXX: The original tests had a test for closure, and it had an
    # off-by-one problem, perhaps due to scope issues.  It has been
    # removed from this test suite.

    def setUp(self):
        ts = []
        ss = []
        for x in range(100):
            t = _Sample1()
            ts.append(t)
            s = safe_ref(t.x, self._closure)
            ss.append(s)
        ts.append(_sample2)
        ss.append(safe_ref(_sample2, self._closure))
        for x in range(30):
            t = _Sample3()
            ts.append(t)
            s = safe_ref(t, self._closure)
            ss.append(s)
        self.ts = ts
        self.ss = ss
        self.closure_count = 0

    def tearDown(self):
        if hasattr(self, 'ts'):
            del self.ts
        if hasattr(self, 'ss'):
            del self.ss

    def test_In(self):
        """Test the `in` operator for safe references (cmp)"""
        for t in self.ts[:50]:
            assert safe_ref(t.x) in self.ss

    def test_Valid(self):
        """Test that the references are valid (return instance methods)"""
        for s in self.ss:
            assert s()

    def test_ShortCircuit(self):
        """Test that creation short-circuits to reuse existing references"""
        sd = {}
        for s in self.ss:
            sd[s] = 1
        for t in self.ts:
            if hasattr(t, 'x'):
                assert safe_ref(t.x) in sd
            else:
                assert safe_ref(t) in sd

    def test_Representation(self):
        """Test that the reference object's representation works

        XXX Doesn't currently check the results, just that no error
            is raised
        """
        repr(self.ss[-1])

    def _closure(self, ref):
        """Dumb utility mechanism to increment deletion counter"""
        self.closure_count += 1
