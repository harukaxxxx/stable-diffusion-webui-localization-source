import json
import urllib.request

# gathering extension data from stable-diffusion-webui-extensions
with urllib.request.urlopen('https://raw.githubusercontent.com/AUTOMATIC1111/stable-diffusion-webui-extensions/master/index.json') as response:
    extension_data = json.loads(response.read().decode())['extensions']


def extract_name_and_description(data, index):
    # extract name and description in extension data
    return {data[index]['name']: data[index]['name'], data[index]['description']: data[index]['description']}


# combine extracted data
for index in range(0, len(extension_data)):
    data = extract_name_and_description(extension_data, index)
    if index == 0 and data:
        extracted_data = data
    elif data:
        extracted_data.update(data)

# save to ExtensionList.json
with open('./source/ExtensionList.json', 'w', encoding='utf-8') as outfile:
    json.dump(extracted_data, outfile, indent=2)
