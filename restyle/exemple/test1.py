#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re


# todo научиться парсить scc файл в список селекторов свойств и значений

from restyle.recss import StyleFile

#
# file = StyleFile('style.css')
# css_str = file.style
# print(css_str)

# pat = re.compile(r'''\n+(\w+).*?(?=\{)''', re.VERBOSE | re.DOTALL | re.IGNORECASE)

# print(set(pat.findall(css_str)))

class Parser:
    def __init__(self, file_name):
        self.file = StyleFile(file_name)
        self.css_str = self.file.style

    def selectors(self):
        pat = re.compile(r'\n+(\w+).*?(?=\{)', re.DOTALL)
        return list(set(pat.findall(self.css_str)))

    def properties(self):
        pat = re.compile(r'''
             #\{
             #.+?
             (\w+\-?\w*?){0,3}\:
             #.+?
             #\}
                        ''', re.DOTALL | re.VERBOSE)
        return list(set(pat.findall(self.css_str)))

if __name__ == '__main__':
    p = Parser('style.css')
    print(p.properties())