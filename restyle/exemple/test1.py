#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
f = '/home/sergk/project/recss/restyle/exemple/style.css'
with open(f, "r") as f:
    s = f.readlines()

def f():
    glob_lst = []
    local = []

    for i in s:
        if not '}' in i:
            local.append(i)
        else:
            local.append(i)
            glob_lst.append(local[:])
            local.clear()

    return glob_lst


with open("file.css", "a") as fs:
    for i in f():
        print(i)
        fs.writelines(i)

