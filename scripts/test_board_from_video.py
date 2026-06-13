import cv2
import sys
import os

sys.path.append(os.path.dirname(__file__))

from board_detector import extract_board_state

video_path = "/content/drive/MyDrive/PokerBoothAI/Gameplay Uploads/2026-03-14 03-37-33.mp4"

timestamps = {
    "river_reference": 88 * 60,
    "early_hand": 300,
}

video = cv2.VideoCapture(video_path)

for label, sec in timestamps.items():

    video.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)

    success, frame = video.read()

    if not success:
        print(label, "FAILED")
        continue

    board = extract_board_state(frame)

    print(label)
    print(board)
    print()

video.release()
