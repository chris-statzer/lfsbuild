![LFS Logo](http://www.linuxfromscratch.org/images/lfs-logo.png)

This is a WIP build framework for the awesome Linux from Scratch project. The
goal is to provide an automated way to build the initial system and get a
working bootable disk. The host target is currently Ubuntu 16.04 LTS as a known
good host.

A further goal will be to use the built Python framework to also manage packages
for BLFS too.

Building

* Mount drive
* make sure LFS and LFS_TGT are defined in the env
* link LFS to /tools
* add /tools/bin to the path
* fix /bin/sh symlink `sudo update-alternatives --install /bin/sh sh /bin/bash 100`
* check versions with supplied script
* install build-essential, gawk, texinfo, bison
* install python packages pyyaml, docopt
* `./bin lfsbuild bootstrap-build-system`

Current issues

* Test suite fails for temp diffutils build when bootstrapping
* Test suite fails for temp file util build when bootstrapping (zlib related)
* Test suite fails for temp gawk util build when bootstrapping (locale related)
