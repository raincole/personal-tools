#!/usr/bin/env zsh

name=$1
printf $name
blender -b $name.blend -f 0
printf "\n---- Render finished. Now creating Anki cards... ----\n\n"
generate_multi_angle_cards.py ${name}_output/

