import json
import os

# set paths
SOURCE_DIR = './extractor/'
SOURCE_FILES = os.listdir(SOURCE_DIR)
SOURCE_FILES.remove('localization.json')
SOURCE_FILES.remove('extractor.py')
SOURCE_FILES.remove('Put clean install localization json file here.txt')

# read base data
with open('./extractor/localization.json', 'r', encoding='utf-8') as base_json:
    BASE_DATA = json.load(base_json)

# extract every source file
for i in SOURCE_FILES:
    SOURCE_FILE_PATH = SOURCE_DIR+i
    with open(SOURCE_FILE_PATH, 'r', encoding='utf-8') as source_json:
        SOURCE_DATA = json.load(source_json)
    # delete same key items
    for key in list(SOURCE_DATA.keys()):
        if key in BASE_DATA:
            del SOURCE_DATA[key]
    # save result to file
        output_file_path = './source/extensions/' + \
            os.path.basename(SOURCE_FILE_PATH)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(SOURCE_DATA, f, ensure_ascii=False, indent=2)
    os.remove(SOURCE_FILE_PATH)
