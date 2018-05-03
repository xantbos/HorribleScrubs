import json
import io
import shutil, os, sys
from shutil import copyfile
from pathlib import Path
		
def returnJsonUnicode(filePath, fileName):
    if fileName.endswith('.json'):
        fileName = fileName[:-5]
    with open(filePath + fileName + '.json', encoding="utf8") as data_file:    
        data = json.load(data_file)
    return data
	
def setUnicodeData(data, json_Name):
    archiver(json_Name + '.json', json_Name + '.json.archive')
    with io.open(json_Name + '.json', 'w', encoding='utf8') as json_file:
        data = json.dumps(data, ensure_ascii=False, indent=2)
        # unicode(data) auto-decodes data to unicode if str
        json_file.write(str(data))
        #json.dump(data, json_Name, ensure_ascii=False)
		
def archiver(file, archive):
    if os.path.isfile(file):
        copyfile(file, archive)
    else:
        Path(file).touch()