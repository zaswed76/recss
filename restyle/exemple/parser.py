#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pprint

class FileError(Exception): pass

class StyleFile:
    def __init__(self, file):
        if os.path.isfile(file):
            self._file = file
        else: raise FileError('файл < "{}" > не найден'.format(file))
        self._style_list = None

    @property
    def file(self):
        return self._file

    def read_style(self):
        with open(self.file, "r") as f:
            return f.readlines()


    def write_style_to_file(self, new_style_list):
        with open(self.file, "w") as f:
            f.write(new_style_list)

class Parser:
    def __init__(self, file):
        self._file = file
        self.file_obj= StyleFile(file)
        self.source_lst = self.file_obj.read_style()
        self._selectors_split_lst = None

    @property
    def selectors_split_lst(self):
        return self._selectors_split_lst

    def split_on_selectors(self):
        glob_lst = []
        local = []
        for s in  self.source_lst:
            if not '}' in s:
                local.append(s)
            else:
                local.append(s)
                glob_lst.append(local[:])
                local.clear()
        self._selectors_split_lst = glob_lst

    def __str__(self):
        return str(self.source_lst)



p = Parser("style.css")
p.split_on_selectors()
pprint.pprint(p.selectors_split_lst)