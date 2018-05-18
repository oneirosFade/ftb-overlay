FTB Modpack Customizing Tool
============================

Installation
------------

```
$ pip install -r requirements.txt

$ python setup.py install
```

Instructions
------------

Usage
```
ftb_overlay [-s SOURCE_PACK] [-p CUSTOM_BASEPATH] [-c CUSTOM_MANIFEST] [-o OUTPUT_PACK] [--noquery]
```

Example
```
ftb_overlay -s ./DW20.zip -o ./output/mypack.zip
```

Use `-h` for more explicit help. The `--noquery` option will prevent the tool from
converting IDs to file/mod names with queries to Curse.

By default, the tool uses `base/base.zip`, `custom/custom.json`, and `final/pack.zip`
if no command-line options are passed.

See the `examples` folder for example custom manifests.