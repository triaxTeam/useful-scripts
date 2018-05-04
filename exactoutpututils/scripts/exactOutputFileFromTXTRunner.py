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

class Struct(object): pass

def parseConfig(configName='config.json'):
	data = json.load(open(configName))
	config = Struct()

	config.applycationPath = data["ExectOutputPath"]
	config.binFilePath = data["BinFilePath"]
	config.recalcFilePath = data["FolderWithRecalculated"]
	config.txtFilePath = data["TxtFile"]
	config.regex = data["RegEx"]
	config.actions = set(data["Actions"])
	return config;

def getSetOfMatchedNamesInFile(file, regex):
	filenames = set()
	for line in file:
		curStr = str(line.strip('\n'))
		matched = re.search(config.regex, curStr);
		if(matched):
			filenames.add(matched.group(1).lower())
	return filenames;

def getFileNamesAndFullFN(filesPath):
	fileNames = []
	fullFileNames = []
	exclude = {'.svn'}
	for root, dirs, files in walk(filesPath):
	    dirs[:] = [d for d in dirs if d not in exclude]
	    for file in files:
	        fullFileNames.append(path.join(root, file))
	        fileNames.append(file.lower());
	return (fileNames, fullFileNames);

def removeFolder(path):
	rmtree(path)

def copyFile(filenamesAndFullFnTuple, filesToCheck, dirName):
	for fN, fullFN in filenamesAndFullFnTuple:
		if fN in filesToCheck:
			copyfile(fullFN, dirName+'\\' + fN)

def execute(dirName, appPath):
	curFilePath = os.path.dirname(os.path.realpath(__file__))
	subprocess.call([appPath, '-path:' +curFilePath+'\\' + dirName])

def getFileNameSetInDir(pathToFile):
	foundFiles = {}
	exclude = {'.svn'}
	for root, dirs, files in walk(pathToFile):
	    dirs[:] = [d for d in dirs if d not in exclude]
	    for file in files:
	    	file = file.lower()
	    	foundFiles[file] = path.join(root, file)
	return foundFiles

def copyFileThatExistInSet(filenameSet, dirFrom):
	exclude = {'.svn'}
	for root, dirs, files in walk(dirFrom):
	    dirs[:] = [d for d in dirs if d not in exclude]
	    for file in files:
	    	file = file.lower()
	    	if(file in filenameSet):
	    		fullPath = path.join(root, file)
	    		copyfile(fullPath, filenameSet[file])

def getNewestFolderInPath(pathToFile):
	return max(glob.glob(os.path.join(pathToFile, '*/')), key=os.path.getmtime);

config = parseConfig();
tmpDirName= "TempBinFiles"

file = io.open(config.txtFilePath,'r', encoding='utf-16')
diffFilenames = getSetOfMatchedNamesInFile(file, config.regex)
fileNames, fullFileNames = getFileNamesAndFullFN(config.binFilePath)
	
if("copySource" in config.actions):
	if os.path.exists(tmpDirName):
		removeFolder(tmpDirName)
	os.makedirs(tmpDirName)
	copyFile(zip(fileNames, fullFileNames), diffFilenames, tmpDirName)

if("calculate" in config.actions):
	execute(tmpDirName, config.applycationPath)

if("copyResult" in config.actions):
	folderWithDifferent = getNewestFolderInPath(config.recalcFilePath) + 'different';
	if os.path.exists(folderWithDifferent):
		binNames = getFileNameSetInDir(config.binFilePath)
		copyFileThatExistInSet(binNames, folderWithDifferent)

if("removeTmp" in config.actions):
	removeFolder(tmpDirName)

