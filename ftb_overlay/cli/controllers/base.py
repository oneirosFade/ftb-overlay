"""ftb-overlay base controller."""

import json
import os
import zipfile
from pathlib import Path
from shutil import copyfile

from cement.ext.ext_argparse import ArgparseController, expose

from ftb_overlay.helpers import mod_index, getName, getVersion


class ftboBaseController(ArgparseController):
    class Meta:
        label = 'base'
        description = 'FTB Modpack Customizing Tool'
        arguments = [
            (['-f', '--foo'],
             dict(help='the notorious foo option', dest='foo', action='store',
                  metavar='TEXT')),
        ]

    @expose(hide=True)
    def default(self):
        if not (os.path.isdir('base/') and os.path.exists('base/base.zip')):
            print("'Please ensure the base pack is stored in \"base/base.zip\" before running.")
            exit(1)

        if not (os.path.isdir('custom/') and os.path.exists('custom/custom.json')):
            print(
                "Please ensure customizations are stored in \"custom/custom.json\" and \"custom/overrides\" before running.")
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
                            getVersion(baseJson['files'][modIndex]['projectID'],
                                       baseJson['files'][modIndex]['fileID'])))
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

        # If using an output handler such as 'mustache', you could also
        # render a data dictionary using a template.  For example:
        #
        #   data = dict(foo='bar')
        #   self.app.render(data, 'default.mustache')
        #
        #
        # The 'default.mustache' file would be loaded from
        # ``ftb_overlay.cli.templates``, or ``/var/lib/ftb_overlay/templates/``.
        #
