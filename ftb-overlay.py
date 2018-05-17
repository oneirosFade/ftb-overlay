import json
import os
import urllib
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from shutil import copyfile
from urllib.request import urlopen


def error_callback(*_, **__):
    pass


def is_string(data):
    return isinstance(data, str)


def is_bytes(data):
    return isinstance(data, bytes)


def to_ascii(data):
    if is_string(data):
        data = data.encode('ascii', errors='ignore')
    elif is_bytes(data):
        data = data.decode('ascii', errors='ignore')
    else:
        data = str(data).encode('ascii', errors='ignore')
    return data


class Parser(HTMLParser):
    def __init__(self, url):
        self.title = None
        self.rec = False
        HTMLParser.__init__(self)
        try:
            self.feed(to_ascii(urlopen(url).read()))
        except urllib.error.HTTPError:
            return
        except urllib.error.URLError:
            return
        except ValueError:
            return

        self.rec = False
        self.error = error_callback

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.rec = True

    def handle_data(self, data):
        if self.rec:
            self.title = data

    def handle_endtag(self, tag):
        if tag == 'title':
            self.rec = False


def get_title(url):
    return Parser(url).title


def getName(projectID):
    pR = get_title("https://minecraft.curseforge.com/projects/{}".format(projectID))
    pT = pR.split(" - ")[1]
    return pT


def getVersion(projectID, fileID):
    pR = get_title("https://minecraft.curseforge.com/projects/{}/files/{}".format(projectID, fileID))
    pT = pR.split(" - ")[0]
    return pT


def mod_index(modlist, modid):
    """
    Find the first instance of the specified mod in the provided list.

    Args:
        modlist (:obj:`list` of :obj:`dict`): List of mods as defined by the FTB manifest
        modid (str): Numeric string of the mod project ID to search for

    Returns:
        (int) Index of first match, if any. Returns `None` if no match.
    """

    for i in range(0, len(modlist)):
        if modlist[i]['projectID'] == modid:
            return i
    return None


if not (os.path.isdir('base/') and os.path.exists('base/base.zip')):
    print("'Please ensure the base pack is stored in \"base/base.zip\" before running.")
    exit(1)

if not (os.path.isdir('custom/') and os.path.exists('custom/custom.json')):
    print("Please ensure customizations are stored in \"custom/custom.json\" and \"custom/overrides\" before running.")
    exit(1)

with zipfile.ZipFile('base/base.zip', 'r') as zBase:
    listContents = zBase.namelist()
    if 'manifest.json' not in listContents:
        print("Error: base.zip is not a valid FTB mod pack ZIP.")
        exit(1)
    else:
        print("Extracting base manifest.")
        zBase.extract('manifest.json', 'base/')

with open('base/manifest.json', 'r') as jsonFileBase:
    baseJsonString = jsonFileBase.read()

with open('custom/custom.json', 'r') as jsonFileCustom:
    customJsonString = jsonFileCustom.read()

baseJson = json.loads(baseJsonString)
customJson = json.loads(customJsonString)

baseModCount = len(baseJson['files'])

print("BASE PACK: {} by {}".format(baseJson['name'], baseJson['author']))
print("MINECRAFT {}".format(baseJson['minecraft']['version']))
print("LOADERS:")
for loader in baseJson['minecraft']['modLoaders']:
    print("  {}".format(loader['id']))
print("MODS: {}".format(baseModCount))
print('')
print("Merging manifest customizations...")

# Iterate over all file customizations in the manifest
for mod in customJson['files']:
    modID = mod['projectID']  # Absolutely required

    if 'fileID' in mod:  # Only required to add or update
        modVersion = mod['fileID']
    else:
        modVersion = None

    if 'state' in mod:  # Assume present
        modState = mod['state'].lower()
    else:
        modState = 'present'

    modIndex = mod_index(baseJson['files'], modID)

    if modIndex is not None:
        if modState == 'present':
            baseJson['files'][modIndex]['fileID'] = modVersion
            print(
                "Updating to {}".format(
                    getVersion(baseJson['files'][modIndex]['projectID'], baseJson['files'][modIndex]['fileID'])))
        else:  # if modState == 'absent'
            baseJson['files'].remove(baseJson['files'][modIndex])
            print("Removed {} from the manifest.".format(getName(modID)))
    else:  # if modIndex is None
        if modState == 'present':
            baseJson['files'].append(mod)
            print("Added project {}".format(getName(mod['projectID'])))
        # else not found and not wanted, so do nothing

copyfile('base/base.zip', 'final/modpack.zip')

with zipfile.ZipFile('final/modpack.zip', 'a') as zFinal:
    zFinal.writestr('manifest.json', json.dumps(baseJson))
    pathList = Path('custom/overrides/').relative_to('custom/').glob('*')
    for path in pathList:
        pathString = str(path)
        zFinal.write(pathString)

print("Final mod pack stored as \"final/modpack.zip\"")
