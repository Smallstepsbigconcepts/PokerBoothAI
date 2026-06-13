import cv2
import csv
import sys
import os

sys.path.append(os.path.dirname(__file__))

from hero_hand_detector_v1 import read_hero_hand
from board_detector import extract_board_state

video_path = "/content/drive/MyDrive/PokerBoothAI/Gameplay Uploads/2026-03-14 03-37-33.mp4"
boundary_csv = "/content/drive/MyDrive/PokerBoothAI/Reports/phase1_hand_boundaries_fast/clustered_hand_boundaries.csv"

def parse_time(timestamp):
    h, m, s = timestamp.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

video = cv2.VideoCapture(video_path)

with open(boundary_csv, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for row in rows[:10]:

    timestamp = row["timestamp"]
    seconds = parse_time(timestamp)

    video.set(cv2.CAP_PROP_POS_MSEC, seconds * 1000)

    success, frame = video.read()

    if not success:
        continue

    hero_hand, hero_cards = read_hero_hand(frame)
    board = extract_board_state(frame)

    hand_object = {
        "timestamp": timestamp,
        "hero_hand": hero_hand,
        "board": board,
    }

    print(hand_object)

video.release()
