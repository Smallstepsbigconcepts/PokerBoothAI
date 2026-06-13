import cv2
import easyocr

RANK_ORDER = "AKQJT98765432"

reader = easyocr.Reader(['en'], gpu=False)

RANK_REGIONS = {
    "left": (610, 540, 640, 590),
    "right": (640, 530, 680, 610),
}

SUIT_REGIONS = {
    "left": (600, 580, 650, 650),
    "right": (650, 580, 700, 650),
}

TEMPLATES = {
    "spade": cv2.imread(
        "templates/spade_template.jpg",
        cv2.IMREAD_GRAYSCALE
    ),
    "diamond": cv2.imread(
        "templates/diamond_template.jpg",
        cv2.IMREAD_GRAYSCALE
    ),
    "heart": cv2.imread(
        "templates/heart_template.jpg",
        cv2.IMREAD_GRAYSCALE
    ),
    "club": cv2.imread(
        "templates/club_template.jpg",
        cv2.IMREAD_GRAYSCALE
    ),
}


def normalize_rank_text(raw):

    if raw is None:
        return "?"

    text = str(raw).upper().strip()
    text = text.replace(" ", "")
    text = text.replace("-", "")
    text = text.replace("_", "")

    replacements = {
        "10": "T",
        "1O": "T",
        "IO": "T",
        "I0": "T",
        "L0": "T",
        "O": "Q",
        "0": "Q",
        "S": "5",
        "B": "8",
    }

    for wrong, right in replacements.items():
        text = text.replace(wrong, right)

    for char in text:
        if char in RANK_ORDER:
            return char

    return "?"


def detect_suit(crop):

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    scores = {}

    for suit_name, template in TEMPLATES.items():

        resized = cv2.resize(
            template,
            (gray.shape[1], gray.shape[0])
        )

        score = cv2.matchTemplate(
            gray,
            resized,
            cv2.TM_CCOEFF_NORMED
        )[0][0]

        scores[suit_name] = float(score)

    best = max(scores, key=scores.get)

    return best, scores[best]


def hand_class(rank1, suit1, rank2, suit2):

    if "?" in [rank1, rank2]:
        return "UNKNOWN"

    if rank1 == rank2:
        return rank1 + rank2

    if RANK_ORDER.index(rank1) <= RANK_ORDER.index(rank2):
        high = rank1
        low = rank2
    else:
        high = rank2
        low = rank1

    suitedness = "s" if suit1 == suit2 else "o"

    return high + low + suitedness


def read_hero_hand(frame):

    cards = {}

    for side in ["left", "right"]:

        x1, y1, x2, y2 = RANK_REGIONS[side]

        rank_crop = frame[y1:y2, x1:x2]

        rank_raw = reader.readtext(
            rank_crop,
            detail=0
        )

        rank = normalize_rank_text(
            rank_raw[0] if rank_raw else None
        )

        x1, y1, x2, y2 = SUIT_REGIONS[side]

        suit_crop = frame[y1:y2, x1:x2]

        suit, suit_score = detect_suit(
            suit_crop
        )

        cards[side] = {
            "rank": rank,
            "suit": suit,
            "suit_score": round(
                suit_score,
                3
            )
        }

    notation = hand_class(
        cards["left"]["rank"],
        cards["left"]["suit"],
        cards["right"]["rank"],
        cards["right"]["suit"]
    )

    return notation, cards
