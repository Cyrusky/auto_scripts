# This is for in the Mac OS:
import json
import os
import platform
import shutil

import zipfile
from datetime import datetime, timedelta

import requests
from clint.textui import progress

HOME_DIR = ""
TOOL_BOX_DIR = ""

JA_NETFILTER_VERSION = "2022.1.0"
JA_PLUGIN_VERSION = "v1.2.0"

CRACKER_LIST = [
    "GoLand",
    "PyCharm",
    "IntelliJ IDEA",
    "Rider",
    "WebStorm",
    "CLion",
    "DataGrip"
]

if platform.system().lower() == "darwin":
    HOME_DIR = os.getenv("HOME")
    TOOL_BOX_DIR = os.path.join(
        HOME_DIR,
        "Library",
        "Application Support",
        "JetBrains")


def get_vm_options(root_dir: str) -> []:
    extension = ".vmoptions"
    vm_options = set()
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(extension) and file.replace(extension, "") in CRACKER_LIST:
                vm_options.add(os.path.join(root, file))

    return [*vm_options]


def get_download_link(repo):
    url = "https://api.github.com/repos/{repo}/releases/latest".format(repo=repo)
    response = requests.get(url)
    info = json.loads(response.text)
    assets = info.get("assets", [])
    if len(assets) == 0:
        return ""
    else:
        return assets[0].get("browser_download_url", None)


def get_filter():
    print("Downloading Filter...")
    url = get_download_link("ja-netfilter/ja-netfilter")
    temp_file = "/tmp/ja-netfilter.jar.zip"
    if os.path.exists(temp_file):
        os.unlink(temp_file)

    response = requests.get(url, stream=True)

    with open(temp_file, 'wb') as filter_file:
        content_size = int(response.headers['content-length'])  # file_size
        for chunk in progress.bar(
                response.iter_content(chunk_size=1024),
                expected_size=(content_size / 1024) + 1
        ):
            if chunk:
                filter_file.write(chunk)
                filter_file.flush()
    zip_file = zipfile.ZipFile(temp_file, 'r')
    filter_dir = os.path.join(TOOL_BOX_DIR, "ja-netfilter")
    if os.path.exists(filter_dir):
        shutil.rmtree(os.path.join(TOOL_BOX_DIR, "ja-netfilter"))
    for file in zip_file.namelist():
        zip_file.extract(file, TOOL_BOX_DIR)
    get_plugin()
    if os.path.exists(temp_file):
        os.unlink(temp_file)
    print("Done")


def get_plugin():
    print("Downloading Plugin...")
    url = get_download_link("zfkun/ja-netfilter-mymap-plugin")
    response = requests.get(url, stream=True)
    with open(os.path.join(TOOL_BOX_DIR, "ja-netfilter", "plugins", "mymap-plugin.jar"), 'wb') as file:
        content_size = int(response.headers.get("content-length", 100))
        for chunk in progress.bar(
                response.iter_content(chunk_size=1024),
                expected_size=(content_size / 1024) + 1
        ):
            if chunk:
                file.write(chunk)
                file.flush()
    print("Done")


def add_java_agent(option_file: str):
    file_content = []
    with open(option_file, 'r') as file:
        for line in file.readlines():
            if not line.startswith("-javaagent"):
                file_content.append(line)
    file_content.append("".join([
        '-javaagent:"',
        os.path.join(
            TOOL_BOX_DIR,
            "ja-netfilter",
            "ja-netfilter.jar"
        ),
        '"'
    ]))
    with open(option_file, 'w') as file:
        file.writelines(file_content)


def write_config():
    now = datetime.now()
    content = """
[DNS]
EQUAL,jetbrains.com

[URL]
PREFIX,https://account.jetbrains.com/lservice/rpc/validateKey.action

[MyMap]
EQUAL,licenseeName->{licenseName}
EQUAL,gracePeriodDays->{periodDays}
EQUAL,paidUpTo->{expiresAt}
""".format(
        licenseName=os.environ["USER"] or "Nobody",
        periodDays=30000,
        expiresAt=(now + timedelta(days=10000)).strftime("%Y-%m-%d")
    )
    with open(os.path.join(TOOL_BOX_DIR, 'ja-netfilter', "janf_config.txt"), 'w') as config_file:
        config_file.write(content)
    return True


def cracker(option_file: str = None):
    option_file = option_file or '/Users/ck/Library/Application Support/JetBrains/Toolbox/apps/WebStorm/ch-0/213.6461.79/WebStorm.app.vmoptions'
    print("Cracking {option}".format(option=option_file))
    add_java_agent(option_file)
    return True


if __name__ == '__main__':
    get_filter()
    write_config()
    option_list = get_vm_options(TOOL_BOX_DIR)
    for option in option_list:
        cracker(option)
