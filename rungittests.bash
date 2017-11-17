#!/bin/bash

### Run tests of CUB files in gittests/ sub-directory
### - CUB files are typically extracted from gittests.zip

### Usage:  ./rungittests.bash [xyz]
###
###         - writes .set files into target sub-directory gittests/xyz/

### Build target sub-directory and create it if it does not exist

gittests=gittests
subdir="$gittests/$1"
[ -d "$subdir" ] || mkdir -pv "$subdir"

### Loop over CUBs

for cub in ${gittests}/*.cub
do

  ### Ensure file exists

  [ -f "$cub" ] || ( echo "Skipping $cub" && false ) || continue

  ### Build .set filename from CUB filename

  dotsetfn=${subdir}/$(basename ${cub%.cub}).set

  ### Process CUB file

  echo -n "Processing $cub to $dotsetfn ..."
  ./socetframesettings from=$cub to=$dotsetfn ss_project=ss_project ss_img_loc=ss_img_loc ss_input_path=ss_input_path ss_cam_calib_path=ss_cam_calib_path
  echo " done"

done
