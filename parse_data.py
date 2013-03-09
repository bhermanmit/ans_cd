#!/usr/bin/env python

from __future__ import division

import csv

reader = csv.reader(open('data.csv','r'), delimiter=';')
for row in reader:
  print row
