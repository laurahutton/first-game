#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

def a_or_an(word):
    if re.match(r'[aeiou]', word, re.IGNORECASE):
        return "an %s" % word
    else:
        return "a %s" % word
