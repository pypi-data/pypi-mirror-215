# Image Segmentation

This repository is intended to centralize and encapsulate code for image processing which currently exists within but is shared across separate broader repositories like `gcamp-extractor` and `wb-utils`. In order to promote reuse across projects and reduce dependency bloat, implementations within this repository should be limited to core algorithmic functionality; helper functionality for things like GUIfication and plotting should live within the client repository where it is needed.

## Installation and Use

If you want to install this package manually, you can just call `pip install git+https://github.com/focolab/image-processing`.

If you want to add this repo as a dependency, add it to the `install_requires` list in your client package's `setup.py`. For example:
```
    install_requires=[
          'improc @ git+https://github.com/focolab/image-processing',
      ],
```
Note that because this repo is private, you will need to authenticate when performing installation. If you would prefer to authenticate with SSH, you can change the `git+https` in either command above to `git+ssh`.

Once you have the package installed, you can import the `segfunctions` module with `from improc import segfunctions`.
