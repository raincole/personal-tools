#!/usr/bin/env bash
for f in *.flac; do ffmpeg -i "$f"  -vf "crop=((in_w/2)*2):((in_h/2)*2)" -c:a alac "${f%.flac}.m4a"; done
