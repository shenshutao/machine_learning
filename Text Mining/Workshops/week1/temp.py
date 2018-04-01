# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

file = open('moby_dick.txt', mode='r')
print(file.read())
print(file.closed)
file.close()

print(file.closed)

with open('moby_dick.txt') as file:
    print(file.readline())
    print(file.readlines()[6:8])
    
    