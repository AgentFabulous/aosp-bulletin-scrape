# aosp-bulletin-scrape

A simple script to scrape Android Security Bulletins into easy to parse CSVs.
You may find various outputs in this repository.

Usage:
```shell
usage: main.py [-h] --patch-level PATCH_LEVEL [--android-version ANDROID_VERSION] [--out-dir OUT_DIR]

optional arguments:
  -h, --help            show this help message and exit
  --patch-level PATCH_LEVEL
                        Specify the patch you want to scrape (Example: 2021-01-01, 2020-10-05, 2020-09, etc)
  --android-version ANDROID_VERSION
                        Android version you want to filter by
  --out-dir OUT_DIR     Directory in which files must be placed
```

Directories:
- android-9 - Patches applicable to Android 9 only
- android-10 - Patches applicable to Android 10 only
- android-11 - Patches applicable to Android 11 only
- common - Patches applicable to all platforms

**Note:** Only patches since bulletin 2020-01-01 are generated
