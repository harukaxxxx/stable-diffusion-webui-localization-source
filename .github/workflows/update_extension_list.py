import json
import urllib.request

# gathering extension data from stable-diffusion-webui-extensions
with urllib.request.urlopen('https://raw.githubusercontent.com/AUTOMATIC1111/stable-diffusion-webui-extensions/master/index.json') as response:
    extensions_data = json.loads(response.read().decode())['extensions']


def extract_name_and_description(data, index):
    # extract name and description in extension data
    return {data[index]['name']: data[index]['name'], data[index]['description']: data[index]['description']}


# combine extracted data
for index in range(0, len(extensions_data)):
    extension_data = extract_name_and_description(extensions_data, index)
    if index == 0 and extension_data:
        extracted_data = extension_data
    elif extension_data:
        extracted_data.update(extension_data)

# save to ExtensionList.json
with open('./source/ExtensionList.json', 'w', encoding='utf-8') as outfile:
    json.dump(extracted_data, outfile, indent=2)
