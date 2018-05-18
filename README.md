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

* Create the `base` directory and place your FTB pack there as `base.zip`
* Create the `custom` directory and an FTB manifest file there named `custom.json`
  * Note that the tool ignores all entries except the `files` array at present.
* Any file overrides should be placed in `custom/overrides` the same as an FTB pack.
* Create the `final` directory.
* Run the tool.
* The `final/modpack.zip` will now be your updated custom pack.
