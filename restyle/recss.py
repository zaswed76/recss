#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from PyQt5 import QtWidgets
from form import Ui_Form


def regular_expression(selector, property):
    pat = re.compile(r'''
        ({selector}
        .+?
        (?<={property}\:))
        .+?
        (\w+)
         '''.format(selector=selector, property=property),
    re.VERBOSE | re.DOTALL | re.IGNORECASE)
    return pat

def restyle(source, regular_expression, replacement):
    return regular_expression.sub(r'\1 {}'.format(replacement), source)

def file_name():
    try:
        name = sys.argv[1]
    except IndexError:
        print("первым аргументом должно быть имя файла")
        sys.exit()
    else: return name

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



class TestForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton_1.clicked.connect(self.do_replace)
        self.style_file = StyleFile(file_name())
        print(self.style_file.style)

    def do_replace(self):
        selector = self.ui.LineEdit_1.text()
        property = self.ui.LineEdit_3.text()
        value = self.ui.LineEdit_4.text()

        pat = regular_expression(selector, property)
        new_style = restyle(self.style_file.style, pat, value)
        self.style_file.style = new_style
        sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = TestForm()
    myapp.show()
    sys.exit(app.exec_())