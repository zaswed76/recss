#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from PyQt5 import QtWidgets

from form import Ui_Form
import parser


def file_name():
    try:
        name = sys.argv[1]
    except IndexError:
        print("первым аргументом должно быть имя файла")
        sys.exit()
    else:
        if name[-3:] == 'css':
            return name
        else:
            print("это не css файл")
            sys.exit()


class StyleFile:
    def __init__(self, file):
        self.file = file
        self._style = None

    @property
    def style(self):
        with open(self.file, "r") as f:
            return f.read()

    @style.setter
    def style(self, new_style):
        with open(self.file, "w") as f:
            f.write(new_style)


class Parser:
    def __init__(self, file_name):
        self.file = StyleFile(file_name)
        # исходная строка
        self.css_str = self.file.style

    def new_css_value(self, selector, property, replacement):
        """
        :return: изменённая строка
        """
        print(replacement)
        pat = re.compile(r'''
            (.+?{selector}
            .+?
            \s+
            ({property}\:))
            .+?
            (\w+)\;
             '''.format(selector=selector, property=property),
                         re.VERBOSE | re.DOTALL | re.IGNORECASE)
        return pat.sub(r'\1 {};'.format(replacement), self.css_str)

    def selectors(self):
        pat = re.compile(r'(\w+).*?\s+(?=\{).*?\}', re.DOTALL)
        return sorted(set(pat.findall(self.css_str)))

    def properties(self):
        pat = re.compile(r'''
                     (?<!\*)\s+([-\w]*?)\:\s+.+?\;
                        ''', re.DOTALL | re.VERBOSE)
        return sorted(set((pat.findall(self.css_str))))


class TestForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parser = parser.Parser(file_name())
        self.parser.split_on_selectors()
        self.parser_dict = self.parser.parser_dict()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton_1.clicked.connect(self.do_replace)
        self.ui.LineEdit_1.currentIndexChanged.connect(self.add_properties)
        self.style_file = StyleFile(file_name())

        self.add_selectors()
        # self.ui.LineEdit_1.addItems(self.parser.selectors())
        # self.ui.LineEdit_3.addItems(self.parser.properties())

    def add_selectors(self):
        self.selectors = sorted(self.parser_dict.keys())
        self.ui.LineEdit_1.addItems(self.selectors)

    def add_properties(self, i):
        self.ui.LineEdit_3.clear()
        properties = self.parser_dict[self.selectors[i]]
        self.ui.LineEdit_3.addItems(sorted(properties.keys()))

    def do_replace(self):
        new_css_lst = []
        selector = self.ui.LineEdit_1.currentText()
        property = self.ui.LineEdit_3.currentText()
        value = self.ui.LineEdit_4.text()
        for s in self.parser.selectors_split_lst:
            print(s)
            new = self.parser.new_css_value(selector, property, value, s)
            print("-----------------")
            print(new)
            new_css_lst.append(new)
        new_css_str = ''.join(new_css_lst)
        self.parser.file_obj.write_style_to_file(new_css_str)
        sys.exit()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = TestForm()
    myapp.show()
    app.exec()
