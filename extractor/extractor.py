import json
import os

# set paths
source_dir = './extractor/'
source_files = os.listdir(source_dir)
source_files.remove('localization.json')
source_files.remove('extractor.py')
source_files.remove('extension-list-updater.py')
source_files.remove('Put clean install localization json file here.txt')

# read base data
with open('./extractor/localization.json', 'r', encoding='utf-8') as f:
    base_data = json.load(f)

# extract every source file
for i in source_files:
    source_file_path = source_dir+i
    with open(source_file_path, 'r', encoding='utf-8') as f:
        source_data = json.load(f)
    # delete same key items
    for key in list(source_data.keys()):
        if key in base_data:
            del source_data[key]
    # save result to file
        output_file_path = './source/extensions/' + \
            os.path.basename(source_file_path)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(source_data, f, ensure_ascii=False, indent=4)
    print(f'{output_file_path} extracted.')
