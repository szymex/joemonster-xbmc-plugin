#!/bin/bash

VERSION=$(perl -n -e'/^[ ]+version="(.*?)"/ && print $1' plugin.video.joemonster/addon.xml)
REPOFILE="plugin.video.joemonster-$VERSION.zip"

zip -r ${REPOFILE} plugin.video.joemonster -x@.gitignore > /dev/null