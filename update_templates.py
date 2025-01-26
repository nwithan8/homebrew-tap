#!/usr/bin/env python
import datetime
import json
import platform

import objectrest
import os
import re
from typing import Union
import argparse


def replace(text: str, pattern: str, replacement: str) -> str:
    return re.sub(pattern, replacement, text)


def load_packages(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)


def save_package_data(package_name: str, file_path: str, data: dict) -> None:
    with open(file_path, 'r') as f:
        json_data = json.load(f)
        json_data[package_name] = data

    with open(file_path, 'w') as f:
        json.dump(json_data, f)


def load_template(package_name: str) -> str:
    with open(package_name, 'r') as f:
        return f.read()


def save_template(file_name: str, text: str) -> None:
    with open(file_name, 'w') as f:
        f.write(text)


def build_template(package_name: str, data: dict) -> None:
    template = load_template(f'templates/{package_name}.txt')

    for key, value in data.items():
        replace_pattern = f"REPLACE_{key.upper()}"
        template = replace(text=template, pattern=replace_pattern, replacement=value)

    save_template(file_name=f'Formula/{package_name}.rb', text=template)


def parse_version_number(version: str) -> str:
    """
    Remove unwanted characters from the version number
    :param version:
    :return:
    """
    version = version.lower()
    return version.replace('v', '').replace('release', '').replace(' ', '')


def calculate_sha256(file_path: str) -> str:
    if platform.system() == 'Windows':
        return os.popen(f'CertUtil -hashfile {file_path} SHA256').read().split(' ')[-1].strip()
    elif platform.system() == 'Linux':
        return os.popen(f'sha256sum {file_path}').read().split(' ')[0]
    elif platform.system() == 'Darwin':
        return os.popen(f'shasum -a 256 {file_path}').read().split(' ')[0]
    else:
        raise Exception(f'Unsupported OS: {platform.system()}')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Update Homebrew formulae')
    parser.add_argument('--force', action='store_true', help='Force update all formulae')
    args = parser.parse_args()

    packages: dict = load_packages(file_path='packages.json')

    os.makedirs('Formula', exist_ok=True)

    updated_templates: list[str] = []

    for package_name, package_data in packages.items():

        print(f"Checking for updates for {package_name}...")

        current_version: Union[str, None] = package_data.get('version', None)
        if current_version is None:
            raise Exception(f'No version found for {package_name}')
        print(f"Last saved version: {current_version}")

        # Get the latest version from GitHub
        print(f"Getting latest version from GitHub...")
        author: str = package_data.get('github_author', None)
        repo: str = package_data.get('github_repo', None)
        release_data: dict = objectrest.get_json(f'https://api.github.com/repos/{author}/{repo}/releases/latest')
        latest_version_string: str = release_data.get('tag_name', None)

        if latest_version_string is None:
            raise Exception(f'No version found for {author}/{repo}')

        latest_version: str = parse_version_number(version=latest_version_string)

        # Check if the latest GitHub version is newer than the current version
        if latest_version == current_version and not args.force:
            print("No new version found. Skipping...")
            continue

        print(f"New version found: {latest_version}")
        source_code_url: str = release_data.get('tarball_url', None)
        if source_code_url is None:
            raise Exception(f'No source code url found for {author}/{repo}')

        # Download the source code and calculate the sha256
        print(f"Downloading source code from {source_code_url}...")
        source_code_file_name: str = f'{package_name}-latest.tar.gz'
        os.system(f'curl -L {source_code_url} -o {source_code_file_name}')
        print(f"Calculating sha256 for {source_code_file_name}...")
        sha256: str = calculate_sha256(file_path=source_code_file_name)
        print(f"sha256: {sha256}")
        os.remove(source_code_file_name)

        # Save the new package data
        package_data['version'] = latest_version
        package_data['url'] = source_code_url
        package_data['sha256'] = sha256
        print(f"Updating data for {package_name}...")
        save_package_data(package_name=package_name, file_path='packages.json', data=package_data)

        # Build the formula
        print(f"Updating formula for {package_name}...")
        build_template(package_name=package_name, data=package_data)

        print(f"{package_name} updated successfully!\n")
        updated_templates.append(package_name)

    # Log the last time the script was run
    with open('last_run.txt', 'w') as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Log which packages were updated
    if len(updated_templates) == 0:
        updated_templates.append('None')
    with open('updated_templates.txt', 'w') as f:
        f.write(', '.join(updated_templates))
