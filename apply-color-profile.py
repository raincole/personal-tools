#!/usr/bin/env python

import click
import subprocess
import os.path 

COLOR_PROFILE_DIR = os.path.expanduser("~/Library/ColorSync/Profiles")

@click.command()
@click.argument("source", required=True, type=click.Path())
@click.argument("target", required=True, type=click.Path())
@click.option("--missing-profile", default="Apple iMac-1.icc", help="The name of the missing color profile")
@click.option("--srgb-profile", default="sRGB_v4_ICC_preference.icc", help="The name of sRGB color profile installed")
def apply_color_profile(source, target, missing_profile, srgb_profile):
    """Apply a color profile to an image without one and convert it to sRGB"""
    missing_profile_path = os.path.join(COLOR_PROFILE_DIR, missing_profile)
    srgb_profile_path = os.path.join(COLOR_PROFILE_DIR, srgb_profile)
    subprocess.run(["convert", source, "-profile", missing_profile_path, "-profile", srgb_profile_path, "+profile", "\"*\"", target])

if __name__ == '__main__':
    apply_color_profile()