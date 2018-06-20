#! /bin/bash

jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore test.keystore test.apk test_key
zipalign -f -v 4 test.apk test_aligned.apk
