import json
import io
import re
import os
from os import walk
from os import path
import subprocess
from shutil import copyfile
from shutil import rmtree
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--from', dest="fromF")
parser.add_argument('--to', dest="to")
parser.add_argument('--ext', dest="ext")
args = parser.parse_args()

def findAllDll(fromPath, extension):
	res = []
	for root, dirs, files in walk(fromPath):
	    for file in files:
	    	if file.endswith("." + extension):
	    		res.append((file, path.join(root, file)))
	return res

allDll = findAllDll(args.fromF, args.ext);
for file in allDll:
	copyfile(file[1], args.to+'\\' + file[0])
