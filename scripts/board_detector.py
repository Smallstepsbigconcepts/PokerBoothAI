import cv2
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

RANK_ORDER = "AKQJT98765432"

BOARD_SLOTS = {
    "board1": (485, 365, 545, 455),
    "board2": (545, 365, 605, 455),
    "board3": (605, 365, 665, 455),
    "board4": (665, 365, 725, 455),
    "board5": (725, 365, 785, 455),
}


def normalize_rank(text):

    if text is None:
        return "?"

    text = str(text).upper()

    replacements = {
        "10": "T",
        "I0": "T",
        "IO": "T",
        "1O": "T",
        "O": "Q",
        "0": "Q",
        "S": "5",
        "B": "8",
    }

    for wrong, right in replacements.items():
        text = text.replace(wrong, right)

    for c in text:
        if c in RANK_ORDER:
            return c

    return "?"


def read_rank(card_crop):

    rank_crop = card_crop[0:45, 0:35]

    rank_crop = cv2.resize(
        rank_crop,
        None,
        fx=4,
        fy=4,
        interpolation=cv2.INTER_CUBIC
    )

    result = reader.readtext(
        rank_crop,
        detail=0,
        allowlist="AKQJT98765432"
    )

    if not result:
        return "?"

    return normalize_rank(result[0])


def extract_board_cards(frame):

    cards = []

    for slot_name in BOARD_SLOTS:

        x1, y1, x2, y2 = BOARD_SLOTS[slot_name]

        crop = frame[y1:y2, x1:x2]

        rank = read_rank(crop)

        cards.append({
            "slot": slot_name,
            "rank": rank
        })

    return cards
