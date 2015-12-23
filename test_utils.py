#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from utils import a_or_an

class TestUtils(unittest.TestCase):
    def test_a_or_an(self):
       self.assertEqual(a_or_an('ottle'), 'an ottle') 
       self.assertEqual(a_or_an('bottle'), 'a bottle') 
