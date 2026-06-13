import cv2
import sys
import os

sys.path.append(os.path.dirname(__file__))

from hero_hand_detector_v1 import read_hero_hand
from board_detector import extract_board_state

video_path = "/content/drive/MyDrive/PokerBoothAI/Gameplay Uploads/2026-03-14 03-37-33.mp4"

timestamp_seconds = 300

video = cv2.VideoCapture(video_path)
video.set(cv2.CAP_PROP_POS_MSEC, timestamp_seconds * 1000)

success, frame = video.read()
video.release()

if not success:
    print("Failed to read frame.")
else:
    hero_hand, hero_cards = read_hero_hand(frame)
    board_state = extract_board_state(frame)

    hand_object = {
        "timestamp_seconds": timestamp_seconds,
        "hero_hand": hero_hand,
        "hero_cards": hero_cards,
        "board": board_state,
    }

    print(hand_object)
