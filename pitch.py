#coding:utf-8
import os

if not os.path.exists("speech2"):
    os.mkdir("speech2")

for file in os.listdir("/speech"):
    source = os.path.join("speech", file)
    target = os.path.join("speech2", file)
    os.system("swab +s < %s > %s" % (source, target))