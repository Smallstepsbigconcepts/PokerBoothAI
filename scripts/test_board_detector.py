import cv2
import sys
import os

sys.path.append(os.path.dirname(__file__))

from board_detector import extract_board_cards

image_path = "/content/drive/MyDrive/PokerBoothAI/Reports/phase1_review_frames/frame_0176_01-28-00.jpg"

frame = cv2.imread(image_path)

cards = extract_board_cards(frame)

for card in cards:
    print(card)
