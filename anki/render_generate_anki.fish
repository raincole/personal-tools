#!/usr/bin/env fish

set name $argv[1]
echo $name
blender -b $name.blend  -E BLENDER_EEVEE -f 0
printf "\n---- Render finished. Now creating Anki cards... ----\n\n"
generate_multi_angle_cards.py {$name}_output/

