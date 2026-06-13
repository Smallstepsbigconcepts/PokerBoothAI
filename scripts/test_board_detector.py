import cv2

from board_detector import extract_board_cards

image_path = "/content/drive/MyDrive/PokerBoothAI/Reports/phase1_review_frames/frame_0176_01-28-00.jpg"

frame = cv2.imread(image_path)

cards = extract_board_cards(frame)

print(cards)
