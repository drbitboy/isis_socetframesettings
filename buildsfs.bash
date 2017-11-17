#!/bin/bash

### Build socetframesettings ISIS app

make clean socetframesettings ISIS3LOCAL=$ISISROOT/3rdParty  CPPFLAGS=--std=gnu++11
