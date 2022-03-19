# This is for in the Mac OS:
import os
import platform

HOME_DIR = ""
TOOL_BOX_DIR = ""

if platform.system().lower() == "darwin":
    HOME_DIR = os.getenv("HOME")
    TOOL_BOX_DIR = os.path.join(
        HOME_DIR,
        "Library",
        "Application Support",
        "JetBrains",
        "Toolbox",
        "apps")


def get_vm_options():


if __name__ == '__main__':
    print(TOOL_BOX_DIR)
