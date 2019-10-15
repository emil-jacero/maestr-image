import urllib.request
import os
import re
import requests
from bs4 import BeautifulSoup
import uuid
import pprint
import datetime
import json
from urllib.parse import urlparse
from pathlib import Path


pp = pprint.PrettyPrinter(indent=2)



def scraper_ubuntu(base_url, version):
    # Retrieve the latest image url
    page = requests.get(base_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    pre = soup.pre  # This is the attribute i am looking for

    links = pre.find_all("a")
    builds_list = []
    for link in links:
        name = link.get("href")
        pattern = re.compile("(ubuntu-.*\.img)|(ubuntu-.*\.tar\.gz)|(ubuntu-.*\.vmdk)")
        if pattern.match(name) is not None:
            # Get sha256 to compare with database
            page = requests.get(f'{base_url}SHA256SUMS')
            shasoup = BeautifulSoup(page.text, 'html.parser')
            hash_list = shasoup.decode().split("\n")
            hash_list.pop(-1)
            for hash in hash_list:
                search_string = f'{name}$'
                if re.search(search_string, hash):
                    image_hash = hash.split(' ')[0]

            builds_dict = {}
            builds_dict['distro'] = "ubuntu"
            builds_dict['version'] = version
            builds_dict['name'] = name
            builds_dict['url'] = f"{base_url}{name}"
            builds_dict['os_arch'] = name.split("-")[4].split(".")[0]
            builds_dict['suffix'] = ".".join(name.split("-")[4].split(".")[1:])
            builds_dict['sha256'] = image_hash
            builds_list.append(builds_dict)

    return builds_list


def find_latest_builds(distro, version):
    if distro.lower() == 'ubuntu':
        base_url = f'https://cloud-images.ubuntu.com/releases/{version}/release/'
        return scraper_ubuntu(base_url, version)

    elif distro.lower() == 'ubuntu-minimal':
        base_url = f'https://cloud-images.ubuntu.com/minimal/releases/{version}/release/'
        if version == "16.04":
            version = "xenial"
            return scraper_ubuntu(base_url, version)
        elif version == "18.04":
            version = "bionic"
            return scraper_ubuntu(base_url, version)

    elif distro.lower() == 'centos':
        pass


class ImageObject():
    def __init__(self, os_name, os_version):
        self.os_name = os_name.lower()
        self.os_version = os_version
        self.sha256 = None
        self.archive_path = None
        self.image_format = None
        self.source_url = None
        self.build = None

    def find_latest_build(self, os_arch):
        # Handle os_arch
        if os_arch == "x86_64":
            os_arch = "amd64"
        elif os_arch == "arm":
            os_arch = "arm64"

        if self.os_name == 'ubuntu':
            self.base_url = f'https://cloud-images.ubuntu.com/releases/{self.os_version}/'
            latest_release = self.get_ubuntu_releases()
            parsed_url = urlparse(latest_release)
            self.build = parsed_url.path.split("/")[-2].split("-")[-1]
            images = self.get_ubuntu_images(url=latest_release)


            filtered_by_platform = list(filter(lambda elem: elem['os_arch'] == os_arch, images))
            filtered_by_image_format = list(filter(lambda elem: elem['image_format'] == "qcow2", filtered_by_platform))
            print(filtered_by_image_format)
            self.sha256 = filtered_by_image_format['sha256']
            self.image_format = filtered_by_image_format['image_format']
            self.source_url = filtered_by_image_format['source_url']
            self.build = filtered_by_image_format['sha256']


        elif self.os_name == 'ubuntu-minimal':
            self.base_url = f'https://cloud-images.ubuntu.com/minimal/releases/{self.os_version}/release/'
            if self.os_version == "16.04":
                version = "xenial"
                return self.get_ubuntu_releases()
            elif self.os_version == "18.04":
                version = "bionic"
                return self.get_ubuntu_releases()

        elif self.os_name == 'centos':
            pass

    def get_ubuntu_releases(self, get_latest=True):
        page = requests.get(self.base_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        pre = soup.pre  # This is the attribute i am looking for
        compile_string = 'release-'
        builds = pre.find_all(href=re.compile(compile_string))

        match_build = []
        for build in builds:
            link = f"{self.base_url}{build.string}"
            match_build.append(link)  # Remove forward slash in the strings
        # Sort Alphanumericly
        sorted_links = sorted(match_build, key=lambda item: (int(item.partition(' ')[0])
                                                             if item[0].isdigit() else float('inf'), item))
        if get_latest:
            return sorted_links[-1]
        else:
            return sorted_links

    def get_ubuntu_images(self, url):
        # Retrieve the latest image url
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        pre = soup.pre  # This is the attribute i am looking for
        links = pre.find_all("a")
        matches = []
        for link in links:
            name = link.get("href")
            pattern = re.compile("(ubuntu-.*\.img)|(ubuntu-.*\.tar\.gz)|(ubuntu-.*\.vmdk)")
            if pattern.match(name) is not None:
                # Get sha256 to compare with database
                page = requests.get(f'{url}SHA256SUMS')
                shasoup = BeautifulSoup(page.text, 'html.parser')
                hash_list = shasoup.decode().split("\n")
                hash_list.pop(-1)
                for hash in hash_list:
                    search_string = f'{name}$'
                    if re.search(search_string, hash):
                        image_hash = hash.split(' ')[0]

                # Get format from suffix
                image_format = ".".join(name.split("-")[4].split(".")[1:])
                if image_format == "img":
                    image_format = "qcow2"
                if image_format == "tar.gz":
                    image_format = "raw"

                builds_dict = {}
                builds_dict['sha256'] = image_hash
                builds_dict['image_format'] = image_format
                builds_dict['source_url'] = f"{url}{name}"
                builds_dict['os_arch'] = name.split("-")[4].split(".")[0]
                matches.append(builds_dict)

        return matches


#os_name = "Ubuntu"
#os_version = "18.04"
#os_arch = "x86_64"
#test = ImageObject(os_name, os_version)
#test.find_latest_build(os_arch=os_arch)
#print(json.dumps(test, sort_keys=True, indent=2))
#fitered_dict = list(filter(lambda elem: elem['os_arch'] == "amd64", test))
#print(json.dumps(fitered_dict, sort_keys=True, indent=2))


def download_image(image, archive_path):
    # v2: ImageObject
    url = image.source_url
    uuid_image_name = image.uuid

    # v2: Update archive_path & archive_filename
    image.archive_path = archive_path
    image.archive_filename = "{}.temp_img".format(uuid_image_name)

    print('Begin download [{}]'.format(url))
    # Define storage locations on the filesystem
    #file_destination = '{dest}tmp_images/'.format(dest=archive_path)
    temp_destination_file = '{dest}tmp_images/{img_name}'.format(dest=archive_path, img_name=image.archive_filename)
    try:
        urllib.request.urlretrieve(url, temp_destination_file)
    except Exception as e:
        raise e

    result = image
    return result
