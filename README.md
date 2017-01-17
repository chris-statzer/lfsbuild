![LFS Logo](http://www.linuxfromscratch.org/images/lfs-logo.png)

This is a WIP build framework for the awesome Linux from Scratch project. The
goal is to provide an automated way to build the initial system and get a
working bootable disk. The host target is currently Ubuntu 16.04 LTS as a known
good host.

A further goal will be to use the built Python framework to also manage packages
for BLFS too.

Building

* Mount drive
* make sure $LFS and $LFS_TGT are defined in the env
* link $LFS/tools to /tools
* add /tools/bin to the path
* fix /bin/sh symlink `sudo update-alternatives --install /bin/sh sh /bin/bash 100`
* check versions with supplied script
* install build-essential, gawk, texinfo, bison
* install python packages pyyaml, docopt
* `./bin lfsbuild bootstrap-build-system`

Additions

During the temp system install a few extras are needed to run the build system.
The list below are packages added to the temp systme built in chapter 5:

* temp-python-setuptools-33.1.1
* temp-python-docopt-0.6.2
* temp-python-pyyaml-3.12

Current issues

* Test suite fails for temp diffutils-3.5 build when bootstrapping
* Build and test suite fails for temp file-5.29 util build when bootstrapping
  (zlib related) The only way I could fix this was to add a zlib build to the
  temp system. This seems to work fine and all the libs and bins have the
  correct signatures etc.
* Test suite fails for temp gawk-4.1.4 util build when bootstrapping
  (locale related)
* Error building Util-linux-2.29 with udev support. Had to disable in the
  configure opts.
