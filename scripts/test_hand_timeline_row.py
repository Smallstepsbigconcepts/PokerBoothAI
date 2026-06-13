import cv2
import sys
import os

sys.path.append(os.path.dirname(__file__))

from hero_hand_detector_v1 import read_hero_hand
from board_detector import extract_board_state

video_path = "/content/drive/MyDrive/PokerBoothAI/Gameplay Uploads/2026-03-14 03-37-33.mp4"

timestamps = [
    300,
    5280,
]

video = cv2.VideoCapture(video_path)

for ts in timestamps:

    video.set(cv2.CAP_PROP_POS_MSEC, ts * 1000)

    success, frame = video.read()

    if not success:
        continue

    hero_hand, hero_cards = read_hero_hand(frame)

    board = extract_board_state(frame)

    row = {
        "timestamp": ts,
        "hero_hand": hero_hand,
        "flop": board["flop"],
        "turn": board["turn"],
        "river": board["river"]
    }

    print(row)

video.release()
