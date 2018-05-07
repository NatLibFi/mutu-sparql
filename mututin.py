#!/usr/bin/env python
# coding: utf-8

import csv
import os
import sys
import rdflib
import subprocess
import collections
from subprocess import Popen, PIPE

domain = sys.argv[1]
domain_yso = sys.argv[2]
yso = sys.argv[3]

class MutuSPARQL:
    def __init__(self):
        #self.queries = ['0-pref-changed.rq', '1-same-pref.rq']
        self.queries = ['0-pref-changed.rq', '1-same-pref.rq', '2-diff-broad-pref.rq', '3-diff-broader.rq', '4-missing-broader.rq']
        self.results = {}
        self.col_labels = {'domainc': 'domainc', 'domainPref': 'domainPref', 'pref': 'pref','prefLabel': 'prefLabel','newPref': 'newPref', 'sameNew': 'sameNew', 'sameOld': 'sameOld', 'ysoLinkLab': 'ysoLinkLab', 'ysoBroaderLab': 'ysoBroaderLab', 'broadPref': 'broadPref', 'newPref': 'newPref'}

    def add_col_val(self, uri, prop,value):
        if uri not in self.results:
            self.results[uri] = collections.defaultdict(list)
        if value not in self.results[uri][prop]:
            self.results[uri][prop].append(value)

    def run_sparqls(self):
        results = {}
        for rq_file in self.queries:
            pipe = subprocess.Popen(["sparql","--graph=" + domain,"--graph=" + domain_yso,"--namedGraph=" + yso,"--query=" + rq_file, "--results=CSV"], stdout=subprocess.PIPE)
            result = self.process_query(pipe)

    def process_query(self, pipe):
        col_labels = []
        reader = csv.reader(pipe.stdout)
        for row in reader:
            if len(col_labels) == 0:
                col_labels = row
            else:
                uri = row[0].decode('utf-8')
                for col, value in enumerate(row):
                    prop = col_labels[col]
                    self.add_col_val(uri, prop, value.decode('utf-8'))

    def print_results(self):
        cols = self.col_labels.keys()
        writer = csv.writer(sys.stdout)
        writer.writerow([self.col_labels[col] for col in cols])
        for uri in self.results:
            vals = []
            for col in cols:
                vals.append(','.join(self.results[uri][col]).encode('UTF-8'))
            writer.writerow(vals)

mutu = MutuSPARQL()
mutu.run_sparqls()
mutu.print_results()

