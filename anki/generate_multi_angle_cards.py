#!/usr/bin/env python

import os
import sys
import base64
import requests
import shutil
from hashlib import sha256

ANKI_URL = 'http://127.0.0.1:8765'
DECK_NAME = "Drawing & Painting"
MODEL_NAME = "Basic"
MEDIA_DIR = os.path.expanduser("~/Library/Application Support/Anki2/User 1/collection.media/")

def remove_frame_number(img_dir: str):
    for f in os.listdir(img_dir):
        full_path = os.path.join(img_dir, f)
        if os.path.isfile(full_path):
            new_path = os.path.join(img_dir, f.replace('_0000', ''))
            os.rename(full_path, new_path)


def save_media(img_path: str) -> str:
    with open(img_path, "rb") as img:
        media_name = f"{sha256(img.read()).hexdigest()}.png"

    media_path = os.path.join(MEDIA_DIR, media_name)
    shutil.copyfile(img_path, media_path)

    return media_name

def generate_card(title: str, y_side: str, x_side: str, z_angle: str, subject_media: str, answer_img: str):
    answer_media = save_media(answer_img)

    y_side_name = y_side.capitalize()
    x_side_name = x_side.capitalize()
    z_angle_name = f'{z_angle}°'

    resp = requests.post(ANKI_URL, json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": DECK_NAME,
                "modelName": MODEL_NAME,
                "fields": {
                    "Front": f"{title}"
                             f"<div><br/><img src=\"{subject_media}\"/><br/><br/>"
                             f"{y_side_name} {x_side_name} {z_angle_name}</div>",
                    "Back": f"<div><img src=\"{answer_media}\"/></div>",
                },
                "tags": ["multi-angle"]
            }
        }
    })

    resp_data = resp.json()
    if resp_data["error"]:
        print(f"Error while adding note: {resp_data['error']}")
    else:
        print(f"Added a card for {y_side_name} {x_side_name} {z_angle_name}")

    return


def get_title(img_dir: str):
    subject_name = os.path.basename(os.path.dirname(img_dir)).replace("_output", "")
    return f"Multi-Angle-{subject_name.capitalize()}"

def main(img_dir: str):
    if not os.path.isdir(img_dir):
        print("The image directory should be a directory (ended with /)")
        return

    remove_frame_number(img_dir)

    subject_img = os.path.join(img_dir, "subject.png")
    subject_media = save_media(subject_img)
    for f in os.listdir(img_dir):
        cmpts = os.path.splitext(f)[0].split('_')
        if len(cmpts) == 3:
            y_side, x_side, z_angle = cmpts
            answer_img = os.path.join(img_dir, f)
            generate_card(get_title(img_dir), y_side, x_side, z_angle, subject_media, answer_img)

# Usage: generate_perspective_cards.py ./cube_output/
if __name__ == "__main__":
    main(sys.argv[1])



