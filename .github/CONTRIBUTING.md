# Adding a new source file

To add a new extension source file from stable-diffusion-webui, follow the steps below:

1. Install a clean stable-diffusion-webui.
2. Generate a localization.json file by going to Settings > Actions > Download localization template.
3. Put the localization.json file in `'./extractor/'`.
4. Install the extension that you want to separate and repeat step 2.
5. Rename the new localization.json file to the extension's repository name (e.g. `stable-diffusion-webui-localization-source.json`).
6. Put the json file from step 5 in `'./extractor/'`.
7. Run `'./extractor/extractor.py'`, and the separated-extension source file will be placed in `'./source/extensions/'`.
8. Manually modify the new source file, such as removing unnecessary symbols, delet file paths only for your environment, etc. (Optionally)
9. Once finished, submit a pull request and wait for approval.

⚠️ Before separating an extension, it is highly recommended to delete the extension's folder in webui, close the terminal, and restart webui. Then start from step 4 above.

# Modifying an existing source file

To modify an existing source file, you can either repeat the "Adding a new source file" steps to update the file or manually add new text to the source file and submit a pull request.