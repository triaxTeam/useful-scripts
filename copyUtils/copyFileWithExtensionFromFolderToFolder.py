from os import walk
from os import path
from shutil import copyfile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--from', dest="fromF")
parser.add_argument('--to', dest="to")
parser.add_argument('--ext', dest="ext")
args = parser.parse_args()

def findAllFilesWithExtension(fromPath, extension):
	res = []
	for root, dirs, files in walk(fromPath):
	    for file in files:
	    	if file.endswith("." + extension):
	    		res.append((file, path.join(root, file)))
	return res

allFiles = findAllFilesWithExtension(args.fromF, args.ext);
for file in allFiles:
	copyfile(file[1], args.to+'\\' + file[0])
