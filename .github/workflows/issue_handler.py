"""
docstring
"""
import os
import json
import sys
import time
from datetime import datetime
import requests


def get_source_file_list():
    '''
    get source file in 'source/extensions'
    '''
    source_file_dict = []
    for filename in os.listdir('source/extensions'):
        if filename.endswith(".json"):
            filename_string = filename.replace('.json', '')
            source_file_dict.append({"title": filename_string})
    return source_file_dict


def get_extension_list():
    '''
    download extension list from sd-webui-extensions repo
    '''
    owner = 'AUTOMATIC1111'
    repo = 'stable-diffusion-webui-extensions'
    extension_list_url = f'https://raw.githubusercontent.com/{owner}/{repo}/master/index.json'
    response = requests.get(extension_list_url, timeout=30)
    extension_data = json.loads(response.content.decode())['extensions']
    extracted_data = []
    for extension in extension_data:
        if "localization" not in extension["tags"]:
            repo_name = extension["url"].split("/")[-1].split(".")[0]
            repo_url = extension["url"].replace(".git", "")
            body = f'**Extension GitHub URL**\nURL: {repo_url}'
            extracted_data.append(
                {"title": repo_name, "body": body, "labels": ['auto'], "milestone": 1})

    return extracted_data


def get_issue_list(token='', page_num=1, all_issue=None):
    '''
    get issue list from repo
    '''
    owner = 'harukaxxxx'
    repo = 'stable-diffusion-webui-localization-source'
    url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    header = {
        "Authorization": f"token {token}"
    }
    payload = {
        'filter': 'all',
        'page': page_num
    }

    issue_list_response = requests.get(
        url,  params=payload, headers=header, timeout=30)

    if issue_list_response.status_code == 200:
        issues = issue_list_response.json()
        if all_issue is None:
            all_issue = []
        all_issue += [{"title": issue['title']}
                      for issue in issues if 'auto' in [label['name'] for label in issue['labels']]]
        link_header = issue_list_response.headers.get('link')
        if link_header is not None and 'rel="next"' in link_header:
            next_page_num = page_num + 1
            all_issue = get_issue_list(
                token=token, page_num=next_page_num, all_issue=all_issue)
    else:
        print(
            f'Failed to fetch issues: code {issue_list_response.status_code} with message {issue_list_response.json()["message"]}', flush=True)
        sys.exit(1)

    return all_issue


def compare_list(main_list, sub_list):
    '''
    compare title in main_list but not in sub_list
    '''
    sub_list_title = set(item["title"] for item in sub_list)
    result_list = [item for item in main_list if item["title"]
                   not in sub_list_title]
    return result_list


def post_issues_to_github(token, extension_list_post):
    '''
    post not issue that extension source or issue not created
    '''
    owner = 'harukaxxxx'
    repo = 'stable-diffusion-webui-localization-source'
    url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    header = {
        "Authorization": f"token {token}"
    }

    for issue_post_data in extension_list_post:
        response = requests.post(url, data=json.dumps(
            issue_post_data), headers=header, timeout=30)
        if response.status_code == 201:
            print(f"issue {issue_post_data['title']} posted", flush=True)
            time.sleep(2)
        elif response.status_code == 403:
            response = requests.get(
                'https://api.github.com/rate_limit', timeout=10)
            reset_timestamp = int(response.headers['X-RateLimit-Reset'])
            reset_time = datetime.fromtimestamp(reset_timestamp)
            print(
                f"Secondary rate limit exceeded, try at {reset_time}", flush=True)
            current_timestamp = datetime.now().timestamp()
            sleep_duration = reset_timestamp - current_timestamp + 1
            time.sleep(sleep_duration)
            response = requests.post(url, data=json.dumps(
                issue_post_data), headers=header, timeout=30)
            if response.status_code == 201:
                print(f"issue {issue_post_data['title']} posted", flush=True)
            else:
                print("Error posting issue:",
                      issue_post_data["title"], flush=True)
        else:
            print("Error posting issue:", issue_post_data["title"], flush=True)
            print(response.text, flush=True)


GITHUB_TOKEN = os.environ['github_api_token']
source_file_list = get_source_file_list()
extension_list = get_extension_list()
issue_list = get_issue_list(token=GITHUB_TOKEN)
post_list = compare_list(compare_list(
    extension_list, source_file_list), issue_list)
post_issues_to_github(GITHUB_TOKEN, post_list)
