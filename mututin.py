#!/usr/bin/env python
# coding: utf-8

import csv, os, sys, rdflib, subprocess
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug import SharedDataMiddleware
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
            self.results[uri] = {'domainc': [], 'domainPref': [], 'pref': [],'prefLabel': [],'newPref': [], 'sameNew': [], 'sameold': []}
        if prop not in self.results[uri]:
            print('ERROR: missing property ' + prop)
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
        print(self.results)

    def print_results(self):
        print(';'.join(self.col_labels.values()))
        for uri in self.results:
            row = ''
            for col in self.results[uri]:
                values = ''
                for i, val in enumerate(self.results[uri][col]):
                    if i > 0 and i < len(self.results[uri][col]):
                        values += ','
                    values += val
                row += values + ';'
            print(row)

mutu = MutuSPARQL()
mutu.run_sparqls()
mutu.print_results()

