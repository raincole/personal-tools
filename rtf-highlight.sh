#!/usr/bin/env bash
pbpaste | pygmentize -f rtf -l $1 -O "style=friendly,fontface=Courier Bold" | pbcopy
