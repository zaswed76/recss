#!/usr/bin/env python
# -*- coding: utf-8 -*-


k=[1700,9000,1500,1700,2500]
b=[240,300,180,170,250]
k1=[1100, 9000, 1500,1800,2500]
b1=[240,300,180,190,250]

def calculate_indexes(seq1, seq2):
    return [n for n, (x, y) in enumerate(zip(seq1, seq2)) if x != y]

print(calculate_indexes(k, k1))
print(calculate_indexes(b, b1))




