#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from PyQt5 import QtWidgets

from form import Ui_Form


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
        print(new_style)
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
        pat = re.compile(r'''
            ({selector}
            .+?
            \s+
            (?<={property}\:))
            .+?
            (\w+)
             '''.format(selector=selector, property=property),
                         re.VERBOSE | re.DOTALL | re.IGNORECASE)
        return pat.sub(r'\1 {}'.format(replacement), self.css_str)

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
        self.parser = Parser(file_name())
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton_1.clicked.connect(self.do_replace)
        self.style_file = StyleFile(file_name())

        self.ui.LineEdit_1.addItems(self.parser.selectors())
        self.ui.LineEdit_3.addItems(self.parser.properties())

    def do_replace(self):
        selector = self.ui.LineEdit_1.currentText()
        property = self.ui.LineEdit_3.currentText()
        value = self.ui.LineEdit_4.text()
        if not all([value, property, property]):
            print('css файл не изменён')
            sys.exit()

        new_style = self.parser.new_css_value(selector, property,
                                              value)
        # записать в файл
        self.style_file.style = new_style
        sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = TestForm()
    myapp.show()
    sys.exit(app.exec_())
