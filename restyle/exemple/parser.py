#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from pprint import pprint


class FileError(Exception): pass


class StyleFile:
    def __init__(self, file):
        if os.path.isfile(file):
            self._file = file
        else:
            raise FileError('файл < "{}" > не найден'.format(file))
        self._style_list = None

    @property
    def file(self):
        return self._file

    def read_style(self):
        with open(self.file, "r") as f:
            return f.readlines()

    def write_style_to_file(self, new_style_list, file=None):
        if file is None:
            file = self.file
        with open(file, "w") as f:
            f.write(new_style_list)


class Parser:
    properties_pat = re.compile(r'''
                (?<!\/\*)
                \s+
                ([-\w]*?) # свойство
                \:.*?
                \;$
                (?!\*\/)
                ''',
                                re.VERBOSE | re.MULTILINE)

    selector_pat = re.compile(r'\n*?(\.?\w+\b).*?\s*?\{')

    def __init__(self, file):
        self._file = file
        self.file_obj = StyleFile(file)
        self._source_lst = []
        self._selectors_split_lst = []

    @property
    def selectors_split_lst(self):
        return self._selectors_split_lst

    def split_on_selectors(self):
        glob_lst = []
        local = []
        p = re.compile('\/\*')
        for s in self.source_lst:
            if p.match(s) or '}' in s:
                local.append(s)
                glob_lst.append(''.join(local))
                local.clear()
            else:
                local.append(s)
        self._selectors_split_lst = glob_lst

    @property
    def source_lst(self):
        return self.file_obj.read_style()

    def properties(self, s):
        return self.properties_pat.findall(s)

    def selector(self, s):
        g = self.selector_pat.match(s)
        if g:
            return g.groups()[0]

    def parser_dict(self):
        selectors = dict()
        properties = dict()
        for s in self.selectors_split_lst:

            pr = self.properties(s)
            if pr:
                properties = dict.fromkeys(pr)
            sel = self.selector(s)
            if sel:
                try:
                    selectors[sel].update(properties)
                except KeyError:
                    selectors[sel] = properties
        return selectors

    def __str__(self):
        return str(self.selectors_split_lst)

    @property
    def display(self):
        t = []
        for i in self.selectors_split_lst:
            t.append(str(i))
        return t

if __name__ == '__main__':
    pass
    p = Parser("demo.css")
    p.split_on_selectors()
    pprint(p.display)
    s = p.selectors_split_lst[0]
    # print(p.selector(s))
    # print(p.properties(s))
    # print(p.parser_dict())
