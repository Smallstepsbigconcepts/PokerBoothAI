import cv2
import csv
import sys
import os

sys.path.append(os.path.dirname(__file__))

from hero_hand_detector_v1 import read_hero_hand
from board_detector import extract_board_state

video_path = "/content/drive/MyDrive/PokerBoothAI/Gameplay Uploads/2026-03-14 03-37-33.mp4"
boundary_csv = "/content/drive/MyDrive/PokerBoothAI/Reports/phase1_hand_boundaries_fast/clustered_hand_boundaries.csv"
output_csv = "/content/drive/MyDrive/PokerBoothAI/Reports/hand_objects_sample.csv"

def parse_time(timestamp):
    h, m, s = timestamp.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

video = cv2.VideoCapture(video_path)

with open(boundary_csv, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    boundary_rows = list(reader)

rows = []

for row in boundary_rows[:25]:

    timestamp = row["timestamp"]
    seconds = parse_time(timestamp)

    video.set(cv2.CAP_PROP_POS_MSEC, seconds * 1000)

    success, frame = video.read()

    if not success:
        continue

    hero_hand, hero_cards = read_hero_hand(frame)
    board = extract_board_state(frame)

    rows.append({
        "timestamp": timestamp,
        "hero_hand": hero_hand,
        "flop": " ".join(board["flop"]),
        "turn": board["turn"] or "",
        "river": board["river"] or "",
        "visible_board_cards": board["visible_count"],
    })

video.release()

with open(output_csv, "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "timestamp",
        "hero_hand",
        "flop",
        "turn",
        "river",
        "visible_board_cards",
    ]

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Saved:")
print(output_csv)
print("Rows:", len(rows))
