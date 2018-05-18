"""ftb-overlay base controller."""

import json
import os
import tempfile
import zipfile
from pathlib import Path
from shutil import copyfile

from cement.ext.ext_argparse import ArgparseController, expose

from ftb_overlay.helpers import index_of_mod, getName, getVersion


class ftboBaseController(ArgparseController):
    class Meta:
        label = 'base'
        description = 'FTB Modpack Customizing Tool'
        arguments = [
            (['-s', '--source'],
             dict(help="Source FTB pack", type=str, metavar='src_pack', dest='src_pack', default='base/base.zip')),
            (['-p', '--custompath'],
             dict(help="Custom overrides path", type=str, metavar='custom_path', dest='custom_path',
                  default='custom/')),
            (['-c', '--custom'],
             dict(help="Custom manifest name", type=str, metavar='custom_manifest', dest='custom_manifest',
                  default='custom.json')),
            (['-o', '--output'],
             dict(help="Final ZIP to output", type=str, metavar='final_pack', dest='final_pack',
                  default='final/pack.zip')),
            (['--noquery'],
             dict(help="Do not query Curse to resolve IDs", action='store_true')),

        ]

    @expose(hide=True,
            help="Merge custom overlay onto FTB modpack.")
    def default(self):
        # Determine source pack. Default is 'base/base.zip' but may be overridden.
        if self.app.pargs.src_pack is not None:
            base_pack = self.app.pargs.src_pack
        else:
            base_pack = 'base/base.zip'
        base_pack_path, base_pack_file = os.path.split(base_pack)
        if not (os.path.isdir(base_pack_path) and os.path.exists(base_pack)):
            print("The pack \"{}\" is not found.".format(base_pack))
            exit(1)

        # Determine customizations path. Default is 'custom/' but may be overridden.
        if self.app.pargs.custom_path is not None:
            custom_path = self.app.pargs.custom_path
        else:
            custom_path = 'custom/'
        if self.app.pargs.custom_manifest is not None:
            custom_manifest = self.app.pargs.custom_manifest
        else:
            custom_manifest = 'custom.json'
        custom_manifest_pathed = "{}{}".format(custom_path, custom_manifest)
        if not (os.path.isdir(custom_path) and os.path.exists(custom_manifest_pathed)):
            print("The custom manifest was not found at \"{}\".".format(custom_manifest_pathed))
            exit(1)

        # Determine final pack. Default is 'final/pack.zip' but may be overridden.
        if self.app.pargs.final_pack is not None:
            final_pack = self.app.pargs.final_pack
        else:
            final_pack = 'final/pack.zip'
        final_pack_path, final_pack_file = os.path.split(final_pack)
        if not os.path.isdir(final_pack_path):
            print("The output path \"{}\" is not found.".format(final_pack_path))
            exit(1)

        # Extract manifest from base pack.
        with tempfile.TemporaryDirectory(prefix="ftbo_") as work_dir:

            with zipfile.ZipFile(base_pack, 'r') as zBase:
                base_contents = zBase.namelist()
                if 'manifest.json' not in base_contents:
                    print("Error: \"{}\" is not a valid FTB mod pack ZIP.".format(base_pack))
                    exit(1)
                else:
                    print("Extracting base manifest.")
                    zBase.extract('manifest.json', work_dir)

            with open("{}/manifest.json".format(work_dir), 'r') as jsonFileBase:
                base_pack_json = jsonFileBase.read()

        with open("{}/{}".format(custom_path, custom_manifest), 'r') as jsonFileCustom:
            custom_json = jsonFileCustom.read()

        base_json_str = json.loads(base_pack_json)
        custom_json_str = json.loads(custom_json)

        base_mod_count = len(base_json_str['files'])

        print("BASE PACK: {} by {}".format(base_json_str['name'], base_json_str['author']))
        print("MINECRAFT {}".format(base_json_str['minecraft']['version']))
        print("LOADERS:")
        for loader in base_json_str['minecraft']['modLoaders']:
            print("  {}".format(loader['id']))
        print("MODS: {}".format(base_mod_count))
        print('')
        print("Merging manifest customizations...")

        # Iterate over all file customizations in the manifest
        for mod in custom_json_str['files']:
            mod_project_id = mod['projectID']  # Absolutely required
            if not self.app.pargs.noquery:
                mod_project_name = getName(mod_project_id)
            else:
                mod_project_name = mod_project_id

            if 'fileID' in mod:  # Only required to add or update
                mod_version = mod['fileID']
                if not self.app.pargs.noquery:
                    mod_file_name = getVersion(mod_project_id, mod_version)
                else:
                    mod_file_name = mod_version

            else:
                mod_version = None

            if 'state' in mod:  # Assume present
                mod_state = mod['state'].lower()
            else:
                mod_state = 'present'

            mod_index = index_of_mod(base_json_str['files'], mod_project_id)

            if mod_index is not None:
                if mod_state == 'present':
                    base_json_str['files'][mod_index]['fileID'] = mod_version
                    print("Updating to {}".format(mod_file_name))
                else:  # if mod_state == 'absent'
                    base_json_str['files'].remove(base_json_str['files'][mod_index])
                    print("Removed {} from the manifest.".format(mod_project_name))
            else:  # if mod_index is None
                if mod_state == 'present':
                    base_json_str['files'].append(mod)
                    print("Added project {}".format(mod_project_name))
                # else not found and not wanted, so do nothing

        copyfile(base_pack, final_pack)

        with zipfile.ZipFile(final_pack, 'a') as zFinal:
            zFinal.writestr('manifest.json', json.dumps(base_json_str))
            override_list = Path("{}/overrides/".format(custom_path)).relative_to(custom_path).glob('*')
            for override_file in override_list:
                override_file_str = str(override_file)
                zFinal.write(override_file_str)

        print("Final mod pack stored as \"{}\"".format(final_pack))
